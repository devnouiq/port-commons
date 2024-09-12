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
        Based on the scrape_status of the shipment, it will call process_active, process_failed, or other methods.
        """
        shipment = context.get('shipment')
        # Assuming the shipment has a 'scrape_status' attribute
        scrape_status = shipment.scrape_status
        logger.info(
            f"Processing shipment ID {shipment.shipment_id} with scrape status '{scrape_status}'")

        # Call appropriate method based on shipment scrape_status
        if scrape_status == ScrapeStatus.ACTIVE:
            self.process_active(context, rules)
        elif scrape_status == ScrapeStatus.FAILED:
            self.process_failed(context, rules)
        elif scrape_status == ScrapeStatus.IN_PROGRESS:
            self.process_in_progress(context, rules)
        elif scrape_status == ScrapeStatus.STOPPED:
            self.process_stopped(context, rules)
        else:
            logger.warning(
                f"Unknown scrape status '{scrape_status}' for shipment ID {shipment.shipment_id}")

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
        existing_container = context.get('container')
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
                self.process(context)
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

    def fetch_existing_shipment_and_container(self, container_availability):
        """
        Fetch existing shipments by shipment_ids.
        """
        try:
            # Fetch existing record by container number and shipment ID
            existing_shipment = self.shipment_repo.get_by_container_number_and_shipment_id(
                container_number=container_availability.container_number,
                shipment_id=container_availability.shipment_id
            )

            # Fetch existing container availability record
            existing_container = self.container_repo.get_by_container_number_and_shipment_id(
                container_number=container_availability.container_number,
                shipment_id=container_availability.shipment_id
            )

            return existing_shipment, existing_container

        except Exception as e:
            logger.error(
                f"Error fetching shipment and container: {str(e)}", exc_info=True)
            raise
