from typing import Dict, Any, List, Optional
from commons.repository import BaseRepository
from commons.utils.logger import get_logger
from sqlalchemy.orm import Session
from ..rules.catalog.set_status_in_active_rule import SetActiveStatusRule
from ..rules.catalog.set_status_in_failed_rule import SetFailedStatusRule
from ..rules.catalog.set_status_in_progress_rule import SetInProgressStatusRule
# Assuming ScrapeStatus is in commons.enums
from commons.enums import ScrapeStatus

logger = get_logger()


class ShipmentService:
    def __init__(self, session: Session, shipment_repo: BaseRepository, container_repo: Optional[BaseRepository] = None):
        self.session = session
        self.shipment_repo = shipment_repo
        self.container_repo = container_repo

    def process(self, context: Dict[str, Any], rules: Optional[List[Any]] = []):
        """
        Generalized process method that handles shipment processing based on shipment status.
        After all rules are applied, if the shipment's status is still 'IN_PROGRESS', it will be marked 'ACTIVE'.
        """
        shipment = context.get('shipment')
        container_availability = context.get('container_availability')

        try:
            # Assign run_id to the shipment
            logger_instance = get_logger()  # Fetch the logger instance
            shipment.run_id = logger_instance.run_id

            # Apply any business rules
            for rule in rules:
                rule.apply(context)

            # Check if the status is still 'IN_PROGRESS'
            if shipment.scrape_status == ScrapeStatus.IN_PROGRESS:
                # No errors or special conditions occurred, mark as ACTIVE
                shipment.scrape_status = ScrapeStatus.ACTIVE
                logger.info(
                    f"Setting shipment ID {shipment.shipment_id} to ACTIVE after successful processing")

            # Save the updated shipment status
            self.shipment_repo.save_or_update(
                shipment, "shipment_id", shipment.shipment_id)

            # If container availability data is present, save it
            if container_availability and self.container_repo:
                container_availability.shipment_id = shipment.shipment_id
                self.container_repo.save_or_update(
                    container_availability, "container_number", container_availability.container_number)

        except Exception as e:
            logger.error(
                f"Error processing shipment ID {shipment.shipment_id}: {str(e)}", exc_info=True)
            shipment.scrape_status = ScrapeStatus.FAILED
            self.shipment_repo.save_or_update(
                shipment, "shipment_id", shipment.shipment_id)
            raise

    def process_in_progress(self, context: Dict[str, Any], rules: Optional[List[Any]] = []):
        """
        Mark a shipment as 'in progress' and apply any associated rules.
        """
        shipment = context.get('shipment')
        rules.append(SetInProgressStatusRule())

        try:
            for rule in rules:
                rule.apply(context)

            # Set scrape status to IN_PROGRESS
            shipment.scrape_status = ScrapeStatus.IN_PROGRESS
            self.shipment_repo.save_or_update(
                shipment, "shipment_id", shipment.shipment_id)
        except Exception as e:
            logger.error(
                f"Error processing in-progress shipment: {str(e)}", exc_info=True)
            raise

    def process_failed(self, context: Dict[str, Any], rules: Optional[List[Any]] = []):
        """
        Mark a shipment as 'failed' and apply any associated rules.
        """
        shipment = context.get('shipment')
        rules.append(SetFailedStatusRule())

        try:
            for rule in rules:
                rule.apply(context)

            shipment.scrape_status = ScrapeStatus.FAILED  # Set scrape status to FAILED
            self.shipment_repo.save_or_update(
                shipment, "shipment_id", shipment.shipment_id)
        except Exception as e:
            logger.error(
                f"Error processing failed shipment: {str(e)}", exc_info=True)
            raise

    def process_active(self, context: Dict[str, Any], rules: Optional[List[Any]] = []):
        """
        Process a shipment and optionally container availability, marking them as 'active' before applying rules.
        """
        shipment = context.get('shipment')
        container_availability = context.get('container_availability')

        rules.append(SetActiveStatusRule())

        try:
            for rule in rules:
                rule.apply(context)

            shipment.scrape_status = ScrapeStatus.ACTIVE  # Set scrape status to ACTIVE
            self.shipment_repo.save_or_update(
                shipment, "shipment_id", shipment.shipment_id)

            if container_availability and self.container_repo:
                container_availability.shipment_id = shipment.shipment_id
                self.container_repo.save_or_update(
                    container_availability, "container_number", container_availability.container_number)

        except Exception as e:
            logger.error(
                f"Error processing active shipment: {str(e)}", exc_info=True)
            raise

    def process_stopped(self, context: Dict[str, Any], rules: Optional[List[Any]] = []):
        """
        Process a shipment marked as 'stopped'. This method can be extended with custom logic.
        """
        shipment = context.get('shipment')
        logger.info(f"Processing stopped shipment ID {shipment.shipment_id}")

        try:
            shipment.scrape_status = ScrapeStatus.STOPPED  # Set scrape status to STOPPED
            self.shipment_repo.save_or_update(
                shipment, "shipment_id", shipment.shipment_id)
        except Exception as e:
            logger.error(
                f"Error processing stopped shipment: {str(e)}", exc_info=True)
            raise

    def mark_shipments_in_progress(self, shipments):
        """
        Mark shipments in progress.
        """
        for shipment in shipments:
            try:
                logger.info(
                    f"Marking shipment ID {shipment.shipment_id} and container {shipment.container_number} 'In Progress'")
                context = {"shipment": shipment}
                self.process_in_progress(context)
                logger.info(
                    f"Updated status to 'In Progress' for shipment ID {shipment.shipment_id}")
            except Exception as e:
                logger.error(
                    f"Failed to update status to 'In Progress' for shipment ID {shipment.shipment_id} : {str(e)}", exc_info=True)
                context = {"shipment": shipment, "error_message": str(e)}
                self.process_failed(context)

    def mark_shipments_in_error(self, shipments, error_message):
        """
        Log errors for each shipment in the current batch.
        """
        for shipment in shipments:
            try:
                context = {"shipment": shipment,
                           "error_message": error_message}
                self.process_failed(context)
            except Exception as e:
                logger.error(
                    f"Failed to log error for shipment ID {shipment.shipment_id}: {str(e)}", exc_info=True)
