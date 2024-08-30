import os
from commons.rules.engine import BusinessRule
from commons.enums import ScrapeStatus
from commons.utils.date import get_current_datetime_in_est
from sqlalchemy import func, or_
from commons.schemas.shipment import Shipment
from typing import Dict, Any
from commons.utils.logger import get_logger

logger = get_logger()


class FetchShipmentsRule(BusinessRule):
    def apply(self, context: Dict[str, Any]) -> None:
        """
        Apply the rule to fetch shipments based on the provided terminal ID and other criteria.

        :param context: The context dictionary containing the SQLAlchemy session and scraper metadata.
        """
        session = context.get('session')
        scraper_metadata = context.get('scraper_metadata')

        if not session or not scraper_metadata:
            raise ValueError(
                "Session and scraper_metadata must be provided in the context.")

        terminal_id = scraper_metadata.terminal_id
        current_time_est = get_current_datetime_in_est()

        # Check if a specific shipment ID is provided in the environment variable
        shipment_id = os.getenv("SHIPMENT_ID")

        if shipment_id:
            logger.info(
                F"Fetching shipment with ID {shipment_id} for trigger use case")
            # Fetch only the specific shipment if shipment_id is provided
            shipment = session.query(Shipment).filter(
                Shipment.terminal_id == terminal_id,
                Shipment.shipment_id == shipment_id
            ).first()

            if shipment:
                context['shipments'] = [shipment]
            else:
                context['shipments'] = []
            return
        else:
            # ORM-based query using the Shipment model for all matching shipments
            shipments = session.query(Shipment).filter(
                Shipment.terminal_id == terminal_id,
                or_(
                    Shipment.scrape_status == ScrapeStatus.ASSIGNED.name,
                    Shipment.scrape_status == ScrapeStatus.ACTIVE.name
                ),
                Shipment.start_scrape_time <= current_time_est,
                (func.extract('epoch', current_time_est -
                 Shipment.last_scraped_time) / 3600) >= Shipment.frequency,
            ).all()

            # Store the fetched shipments in the context for further processing
            context['shipments'] = shipments
