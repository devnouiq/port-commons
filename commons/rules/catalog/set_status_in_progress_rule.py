from commons.rules.engine import BusinessRule
from typing import Dict, Any
from commons.enums import ScrapeStatus
from commons.utils.date import get_current_datetime_in_est
from commons.utils.logger import get_logger
from datetime import timedelta
logger = get_logger()


class SetInProgressStatusRule(BusinessRule):
    def apply(self, context: Dict[str, Any]) -> None:
        """
        If the shipment's status is set to IN_PROGRESS, update the last_scraped_time.
        """
        shipment = context.get("shipment")
        if shipment:
            logger.info(
                f"Setting status to IN_PROGRESS and updating last_scraped_time for shipment ID {shipment.shipment_id}")

            current_time = get_current_datetime_in_est()
            next_scrape_time = current_time + \
                timedelta(hours=shipment.frequency)

            shipment.scrape_status = ScrapeStatus.IN_PROGRESS
            shipment.last_scraped_time = get_current_datetime_in_est()
            shipment.next_scrape_time = next_scrape_time

            logger.info(
                f"Shipment ID {shipment.shipment_id} status set to IN_PROGRESS and last_scraped_time updated to {shipment.last_scraped_time}")
