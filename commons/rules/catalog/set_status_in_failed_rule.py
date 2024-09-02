from commons.rules.engine import BusinessRule
from typing import Dict, Any
from commons.enums import ScrapeStatus
from commons.utils.logger import get_logger

logger = get_logger()


class SetFailedStatusRule(BusinessRule):
    def apply(self, context: Dict[str, Any]) -> None:

        shipment = context.get('shipment')
        error_message = context.get('error_message')

        shipment.scrape_status = ScrapeStatus.FAILED
        shipment.error = error_message
        if shipment:
            logger.info(
                f"Setting status to FAILED and updating last_scraped_time for shipment ID {shipment.shipment_id}")
