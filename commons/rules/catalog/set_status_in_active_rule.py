from commons.rules.engine import BusinessRule
from typing import Dict, Any
from commons.enums import ScrapeStatus
from commons.utils.logger import get_logger

logger = get_logger()


class SetActiveStatusRule(BusinessRule):
    def apply(self, context: Dict[str, Any]) -> None:
        """
        If the shipment's status is ACTIVE, update the next_scrape_time
        to be the current time plus the shipment's frequency in hours.
        """
        shipment = context.get("shipment")
        shipment.scrape_status = ScrapeStatus.ACTIVE
        shipment.error = None
        logger.info(
            f"Shipment ID {shipment.shipment_id} status set to ACTIVE")
