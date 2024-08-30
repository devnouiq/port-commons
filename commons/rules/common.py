from commons.rules import BusinessRule
from typing import Dict, Any
from commons.enums import ScrapeStatus
from commons.utils.date import get_current_datetime_in_est
from commons.utils.logger import get_logger

logger = get_logger()


class SetActiveStatusRule(BusinessRule):
    def apply(self, context: Dict[str, Any]) -> None:
        """
        If the container availability's status is ACTIVE, update the next_scrape_time.
        Also, update the associated shipment status to ACTIVE.
        """
        container_availability = context.get("container_availability")
        if container_availability.scrape_status == ScrapeStatus.ACTIVE:
            logger.info(
                f"Setting next_scrape_time for container {container_availability.container_number}")
            container_availability.next_scrape_time = get_current_datetime_in_est()
