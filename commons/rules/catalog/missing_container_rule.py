from commons.rules.engine import BusinessRule
from typing import Dict, Any
from commons.enums import ScrapeStatus
from commons.utils.logger import get_logger

logger = get_logger()

class HandleMissingContainerRule(BusinessRule):
    def apply(self, context: Dict[str, Any]) -> None:
        """
        Handle the scenario where a container is not found in the scraped results.
        """
        shipment = context.get("shipment")
        shipment.scrape_status = ScrapeStatus.STOPPED
        
        shipment.error = None
        logger.info(
            f"Shipment ID {shipment.shipment_id} status set to STOPPED")
