from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Any, Dict, List
from commons.enums import ScrapeStatus
from commons.utils.date import get_current_datetime_in_est
from commons.utils.logger import get_logger


logger = get_logger()


class BaseRepository:
    def __init__(self, session: Session, model: Any):
        self.session = session
        self.model = model

    def save(self, entity: Any):
        try:
            logger.info(f"Saving entity: {entity}")
            self.session.add(entity)
            self.session.commit()  # Commit after save
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Failed to save entity: {str(e)}")

    def bulk_save_objects(self, entities: List[Any]):
        """Bulk save a list of entities."""
        try:
            self.session.bulk_save_objects(entities)
            self.session.commit()  # Commit after bulk save
        except SQLAlchemyError as e:
            self.session.rollback()  # Rollback on error
            raise ValueError(f"Failed to bulk save entities: {str(e)}")

    def update(self, entity: Any, updates: Any):
        try:
            logger.info(f"Updating entity: {entity}")
            # Iterate over the attributes of the updates object
            for key, value in updates.__dict__.items():
                if key != '_sa_instance_state':  # Skip internal SQLAlchemy state
                    setattr(entity, key, value)
            self.session.commit()  # Commit after update
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Failed to update entity: {str(e)}")

    def delete(self, entity: Any):
        try:
            self.session.delete(entity)
            self.session.commit()  # Commit after delete
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Failed to delete entity: {str(e)}")

    def get_by_id(self, entity_id: int) -> Any:
        try:
            return self.session.query(self.model).get(entity_id)
        except SQLAlchemyError as e:
            raise ValueError(f"Failed to get entity by ID: {str(e)}")

    def get_by_container_number_and_shipment_id(self, container_number: str, shipment_id: int) -> Any:
        try:
            return self.session.query(self.model).filter_by(
                container_number=container_number, shipment_id=shipment_id).first()
        except SQLAlchemyError as e:
            raise ValueError(
                f"Failed to get entity by container number and shipment ID: {str(e)}")

    def _update_by_id(self, entity_id: int, updates: Dict[str, Any]):
        try:
            self.session.query(self.model).filter_by(
                id=entity_id).update(updates)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Failed to update entity: {str(e)}")

    def prepare_and_update_in_progress(self, entity_id: int):
        updates = {
            'scrape_status': ScrapeStatus.IN_PROGRESS,
            'last_scraped_time': get_current_datetime_in_est()
        }
        self._update_by_id(entity_id, updates)

    def prepare_and_update_failed(self, entity_id: int, error_message: str):
        updates = {
            'scrape_status': ScrapeStatus.FAILED,
            'error': error_message
        }
        self._update_by_id(entity_id, updates)

    def prepare_and_update_active(self, entity_id: int):
        updates = {
            'scrape_status': ScrapeStatus.ACTIVE,
            'next_scrape_time': get_current_datetime_in_est()
        }
        self._update_by_id(entity_id, updates)

    def prepare_and_update_stopped(self, entity_id: int):
        updates = {
            'scrape_status': ScrapeStatus.STOPPED,
            'next_scrape_time': None
        }
        self._update_by_id(entity_id, updates)

    def save_or_update(self, entity: Any, unique_field: str, unique_value: Any):
        """Save a new entity or update an existing one based on a unique field."""
        try:
            existing_entity = self.session.query(self.model).filter_by(
                **{unique_field: unique_value}).first()
            if existing_entity:
                self.update(existing_entity, entity)
            else:
                self.save(entity)
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Failed to save or update entity: {str(e)}")

    def handle_missing_container(self, container_number: str, shipment_id: int):
        """
        Handle the scenario where a container is not found in the scraped results.

        :param container_number: The container number that was not found.
        :param shipment_id: The shipment ID associated with the container.
        """
        try:
            existing_record = self.get_by_container_number_and_shipment_id(
                container_number, shipment_id)
            if existing_record and existing_record.scrape_status == ScrapeStatus.ACTIVE:
                self.prepare_and_update_stopped(shipment_id)
            else:
                self.prepare_and_update_failed(
                    shipment_id, "Scraping failed: Container number not found in results.")
        except SQLAlchemyError as e:
            raise ValueError(f"Failed to handle missing container: {str(e)}")
