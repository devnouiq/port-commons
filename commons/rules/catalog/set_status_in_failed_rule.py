from commons.rules.engine import BusinessRule
from typing import Dict, Any
from commons.enums import ScrapeStatus
from commons.utils.date import get_current_datetime_in_est
from commons.utils.logger import get_logger
from datetime import timedelta

logger = get_logger()


class SetFailedStatusRule(BusinessRule):
    def apply(self, context: Dict[str, Any]) -> None:

        shipment = context.get('shipment')
        error_message = context.get('error_message')

        current_time = get_current_datetime_in_est()
        next_scrape_time = current_time + timedelta(hours=shipment.frequency)
         
        shipment.scrape_status = ScrapeStatus.FAILED
        shipment.next_scrape_time = next_scrape_time
        shipment.error = error_message
        if shipment:
            logger.info(
                f"Setting status to FAILED and updating last_scraped_time for shipment ID {shipment.shipment_id}")
