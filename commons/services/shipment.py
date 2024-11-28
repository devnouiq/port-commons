from typing import Dict, Any, List, Optional
from commons.repository import BaseRepository
from commons.utils.logger import get_logger
from sqlalchemy.orm import Session
from ..rules.catalog.set_status_in_active_rule import SetActiveStatusRule
from ..rules.catalog.set_status_in_failed_rule import SetFailedStatusRule
from ..rules.catalog.set_status_in_progress_rule import SetInProgressStatusRule
# Assuming ScrapeStatus is in commons.enums
from commons.enums import ScrapeStatus
from ..schemas.shipment_log import ShipmentLog
import datetime
from commons.utils.date import get_current_datetime_in_est
from enum import Enum
import uuid


logger = get_logger()

class ShipmentService:
    def __init__(self, session: Session, shipment_repo: BaseRepository, container_repo: Optional[BaseRepository] = None, shipment_log_repo: Optional[BaseRepository] = None):
        self.session = session
        self.shipment_repo = shipment_repo
        self.container_repo = container_repo
        self.shipment_log_repo = shipment_log_repo

    def get_model_data(self, model):
        data = {k: v for k, v in model.__dict__.items() if not k.startswith('_')}
        json_data = self.make_json_serializable(data)
        return json_data
    
    def make_json_serializable(self, data):
        if isinstance(data, dict):
            return {k: self.make_json_serializable(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.make_json_serializable(v) for v in data]
        elif isinstance(data, datetime.datetime):
            return data.isoformat()
        elif isinstance(data, datetime.date):
            return data.isoformat()
        elif isinstance(data, Enum):
            return data.value
        elif isinstance(data, uuid.UUID):  # Add this condition
            return str(data)
        else:
            return data

    def create_shipment_log(self, shipment, previous_data, new_data):
        shipment_log = ShipmentLog(
            shipment_id=shipment.shipment_id,
            scrape_status=shipment.scrape_status,
            scraped_at=shipment.last_scraped_time,
            new_data=new_data
        )
        self.shipment_log_repo.save(shipment_log)

    def process(self, context: Dict[str, Any], rules: Optional[List[Any]] = []):
        shipment = context.get('shipment')
        container_availability = context.get('container_availability')
        previous_data = None
        new_data = None

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
            
            if container_availability:
                new_data = self.make_json_serializable({
                    'shipment': self.make_json_serializable(shipment),
                    'container_availability': self.make_json_serializable(container_availability)
                })
            else:
                new_data = self.make_json_serializable(shipment),
            logger.info(f"New data for shipment {shipment.shipment_id}: {new_data}")

            # Save the updated shipment status
            self.shipment_repo.save_or_update(
                shipment, "shipment_id", shipment.shipment_id)

            # Create ShipmentLog entry
            self.create_shipment_log(shipment, previous_data, new_data)

            logger.info(f"Setting shipment ID {shipment.shipment_id} logs")

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

            # Store new data for logging
            new_data = self.get_model_data(shipment)

            # Create ShipmentLog entry
            self.create_shipment_log(shipment, previous_data, new_data)
            raise

    def process_in_progress(self, context: Dict[str, Any], rules: Optional[List[Any]] = []):
        """
        Mark a shipment as 'IN_PROGRESS' and apply any associated rules.
        """
        shipment = context.get('shipment')
        previous_data = None
        new_data = None

        try:

            rules.append(SetInProgressStatusRule())

            # Apply rules
            for rule in rules:
                rule.apply(context)

            # Set scrape status to IN_PROGRESS
            shipment.scrape_status = ScrapeStatus.IN_PROGRESS

            new_data = self.get_model_data(shipment)
            logger.debug(f"New data for shipment {shipment.shipment_id}: {new_data}")

            # Save the updated shipment
            self.shipment_repo.save_or_update(
                shipment, "shipment_id", shipment.shipment_id)

            # Create ShipmentLog entry
            self.create_shipment_log(shipment, previous_data, new_data)

        except Exception as e:
            logger.error(
                f"Error processing in-progress shipment ID {shipment.shipment_id}: {str(e)}")
            raise


    def process_failed(self, context: Dict[str, Any], rules: Optional[List[Any]] = []):
        """
        Mark a shipment as 'FAILED' and apply any associated rules.
        """
        shipment = context.get('shipment')
        previous_data = None
        new_data = None

        try:

            rules.append(SetFailedStatusRule())

            # Apply rules
            for rule in rules:
                rule.apply(context)

            # Set scrape status to FAILED
            shipment.scrape_status = ScrapeStatus.FAILED
            new_data = self.get_model_data(shipment)
            logger.debug(f"New data for shipment {shipment.shipment_id}: {new_data}")

            # Save the updated shipment
            self.shipment_repo.save_or_update(
                shipment, "shipment_id", shipment.shipment_id)

            # Create ShipmentLog entry
            self.create_shipment_log(shipment, previous_data, new_data)

        except Exception as e:
            logger.error(
                f"Error processing failed shipment ID {shipment.shipment_id}: {str(e)}")
            raise

    def process_active(self, context: Dict[str, Any], rules: Optional[List[Any]] = []):
        """
        Process a shipment and optionally container availability, marking them as 'ACTIVE' before applying rules.
        """
        shipment = context.get('shipment')
        container_availability = context.get('container_availability')
        previous_data = None
        new_data = None

        try:
            # Capture previous data
            # previous_data = self.get_model_data(shipment)
            # logger.debug(f"Previous data for shipment {shipment.shipment_id}: {previous_data}")

            rules.append(SetActiveStatusRule())

            # Apply rules
            for rule in rules:
                rule.apply(context)

            # Set scrape status to ACTIVE
            shipment.scrape_status = ScrapeStatus.ACTIVE
            
            if container_availability:
                new_data = self.make_json_serializable({
                    'shipment': self.make_json_serializable(shipment),
                    'container_availability': self.make_json_serializable(container_availability)
                })
            else:
                new_data = self.make_json_serializable(shipment),
            logger.info(f"New data for shipment {shipment.shipment_id}: {new_data}")

            # Save the updated shipment
            self.shipment_repo.save_or_update(
                shipment, "shipment_id", shipment.shipment_id)

            # Save container availability if present
            if container_availability and self.container_repo:
                container_availability.shipment_id = shipment.shipment_id
                self.container_repo.save_or_update(
                    container_availability, "container_number", container_availability.container_number)

            # Create ShipmentLog entry
            self.create_shipment_log(shipment, previous_data, new_data)

        except Exception as e:
            logger.error(
                f"Error processing active shipment ID {shipment.shipment_id}: {str(e)}")
            raise

    def process_stopped(self, context: Dict[str, Any], rules: Optional[List[Any]] = []):
        """
        Process a shipment marked as 'STOPPED'. This method can be extended with custom logic.
        """
        shipment = context.get('shipment')
        previous_data = None
        new_data = None

        try:
            # Set scrape status to STOPPED
            shipment.scrape_status = ScrapeStatus.STOPPED
            new_data = self.get_model_data(shipment)
            logger.debug(f"New data for shipment {shipment.shipment_id}: {new_data}")

            # Save the updated shipment
            self.shipment_repo.save_or_update(
                shipment, "shipment_id", shipment.shipment_id)
            
            # Create ShipmentLog entry
            self.create_shipment_log(shipment, previous_data, new_data)

            logger.info(f"Processed stopped shipment ID {shipment.shipment_id}")

        except Exception as e:
            logger.error(
                f"Error processing stopped shipment ID {shipment.shipment_id}: {str(e)}")
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
