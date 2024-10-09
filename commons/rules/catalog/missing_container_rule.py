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
        container_number = context.get('container_number')
        shipment_id = context.get('shipment_id')
        # Assuming the repository is passed in the context
        repository = context.get('repository')

        logger.info(
            f"Handling missing container {container_number} for shipment {shipment_id}")

        if container_number and shipment_id and repository:
            try:
                existing_record = repository.get_by_container_number_and_shipment_id(
                    container_number, shipment_id
                )
                if existing_record and (existing_record.scrape_status == ScrapeStatus.ACTIVE or existing_record.scrape_status == ScrapeStatus.IN_PROGRESS):
                    existing_record.scrape_status = ScrapeStatus.STOPPED
                    existing_record.next_scrape_time = None
                    repository.save_or_update(
                        existing_record, 'shipment_id', shipment_id)
                    logger.info(
                        f"Marked shipment {shipment_id} as STOPPED due to missing container {container_number}")
                else:
                    logger.warning(
                        f"No existing record found for container {container_number} and shipment {shipment_id}")
            except Exception as e:
                logger.error(
                    f"Failed to handle missing container {container_number} for shipment {shipment_id}: {str(e)}")
                raise ValueError(
                    f"Failed to handle missing container: {str(e)}")
        else:
            raise ValueError(
                "Missing required context data: container_number, shipment_id, or repository")
