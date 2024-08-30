from commons.rules.engine import BusinessRule
from typing import Dict, Any
from commons.enums import ScrapeStatus
from commons.utils.date import get_current_datetime_in_est
from commons.utils.logger import get_logger
from datetime import timedelta

logger = get_logger()


class SetActiveStatusRule(BusinessRule):
    def apply(self, context: Dict[str, Any]) -> None:
        """
        If the shipment's status is ACTIVE, update the next_scrape_time
        to be the current time plus the shipment's frequency in hours.
        """
        shipment = context.get("shipment")
        if shipment and shipment.scrape_status == ScrapeStatus.ACTIVE:
            logger.info(
                f"Setting next_scrape_time for shipment ID {shipment.shipment_id}")

            current_time = get_current_datetime_in_est()
            next_scrape_time = current_time + \
                timedelta(hours=shipment.frequency)

            shipment.last_scrape_time = current_time
            shipment.next_scrape_time = next_scrape_time

            logger.info(
                f"Next scrape time set to {shipment.next_scrape_time} for shipment ID {shipment.shipment_id}")
