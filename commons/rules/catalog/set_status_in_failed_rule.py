from commons.rules.engine import BusinessRule
from typing import Dict, Any
from commons.enums import ScrapeStatus
from commons.utils.logger import get_logger
from commons.utils.date import get_current_datetime_in_est
from datetime import timedelta

logger = get_logger()


class SetFailedStatusRule(BusinessRule):
    def apply(self, context: Dict[str, Any]) -> None:
        """
        If the shipment's status is set to IN_PROGRESS, update the last_scraped_time.
        """
        shipment = context.get("shipment")
        if shipment:
            logger.info(
                f"Setting status to FAILED and updating last_scraped_time for shipment ID {shipment.shipment_id}")

            shipment.scrape_status = ScrapeStatus.ACTIVE
            shipment.last_scraped_time = get_current_datetime_in_est() - timedelta(days=1)
            shipment.next_scrape_time = shipment.last_scraped_time + \
                timedelta(hours=shipment.frequency)

            logger.info(
                f"Shipment ID {shipment.shipment_id} status set to FAILED and last_scraped_time updated to {shipment.last_scraped_time}")
