from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Any, Dict, List
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

    def update(self, entity: Any, updates: Any):
        try:
            logger.info(f"Updating entity: {entity}")
            for key, value in updates.__dict__.items():
                if key != '_sa_instance_state':  # Skip internal SQLAlchemy state
                    setattr(entity, key, value)
            self.session.commit()  # Commit after update
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Failed to update entity: {str(e)}")

    def save_or_update(self, entity: Any, unique_field: str, unique_value: Any):
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

    def handle_missing_container(self, container_number: str, shipment_id: int):
        try:
            existing_record = self.get_by_container_number_and_shipment_id(
                container_number, shipment_id)
            if existing_record:
                existing_record.scrape_status = ScrapeStatus.STOPPED
                existing_record.next_scrape_time = None
                self.save_or_update(
                    existing_record, 'shipment_id', shipment_id)
            else:
                raise ValueError(
                    f"No existing record found for container {container_number} and shipment {shipment_id}")
        except SQLAlchemyError as e:
            raise ValueError(f"Failed to handle missing container: {str(e)}")
