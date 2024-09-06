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
        repository = context.get('repository')

        # Debug logs to check context data
        logger.debug(f"Context data: {context}")

        # Validate required context data
        if not container_number:
            logger.error("Missing 'container_number' in context")
            raise ValueError("Missing required context data: 'container_number'")
        if not shipment_id:
            logger.error("Missing 'shipment_id' in context")
            raise ValueError("Missing required context data: 'shipment_id'")
        if not repository:
            logger.error("Missing 'repository' in context")
            raise ValueError("Missing required context data: 'repository'")

        logger.info(
            f"Handling missing container {container_number} for shipment {shipment_id}"
        )

        try:
            # Attempt to retrieve existing record
            existing_record = repository.get_by_container_number_and_shipment_id(
                container_number, shipment_id
            )
            logger.debug(f"Existing record: {existing_record}")

            if existing_record:
                if existing_record.scrape_status == ScrapeStatus.ACTIVE:
                    existing_record.scrape_status = ScrapeStatus.STOPPED
                    existing_record.next_scrape_time = None
                    # Save or update the existing record
                    repository.save_or_update(
                        existing_record, 'shipment_id', shipment_id
                    )
                    logger.info(
                        f"Marked shipment {shipment_id} as STOPPED due to missing container {container_number}"
                    )
                else:
                    logger.info(
                        f"Container {container_number} for shipment {shipment_id} is already in {existing_record.scrape_status} status."
                    )
            else:
                logger.warning(
                    f"No existing record found for container {container_number} and shipment {shipment_id}"
                )

        except Exception as e:
            logger.error(
                f"Failed to handle missing container {container_number} for shipment {shipment_id}: {str(e)}",
                exc_info=True
            )
            raise ValueError(
                f"Failed to handle missing container: {str(e)}"
            ) from e
