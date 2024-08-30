from commons.repository import BaseRepository
from commons.enums import ScrapeStatus
from commons.utils.date import get_current_datetime_in_est
from commons.utils.logger import get_logger
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from ..rules.catalog.set_status_in_active_rule import SetActiveStatusRule
from ..rules.catalog.set_status_in_failed_rule import SetFailedStatusRule
from ..rules.catalog.set_status_in_progress_rule import SetInProgressStatusRule

logger = get_logger()


class ShipmentService:
    def __init__(self, session: Session, shipment_repo: BaseRepository, container_repo: Optional[BaseRepository] = None):
        self.session = session
        self.shipment_repo = shipment_repo
        self.container_repo = container_repo

    def process_in_progress(self, context: Dict[str, Any], rules: Optional[list] = []):
        """
        Mark a shipment as in progress and apply any associated rules.
        """
        shipment = context.get('shipment')

        rules.append(SetInProgressStatusRule())

        # Apply any provided rules
        if rules:
            for rule in rules:
                rule.apply(context)

        # Save or update the shipment
        self.shipment_repo.save_or_update(
            shipment, "shipment_id", shipment.shipment_id)

    def process_failed(self, context: Dict[str, Any], rules: Optional[list] = []):
        """
        Mark a shipment as failed and apply any associated rules.
        """
        shipment = context.get('shipment')
        error_message = context.get('error_message')

        # Mark the shipment as FAILED
        shipment.scrape_status = ScrapeStatus.FAILED
        shipment.error = error_message

        # Apply any provided rules
        if rules:
            for rule in rules:
                rule.apply(context)

        # Save or update the shipment
        self.shipment_repo.save_or_update(
            shipment, "shipment_id", shipment.shipment_id)

    def process_active(self, context: Dict[str, Any], rules: Optional[list] = []):
        """
        Process a shipment and optionally container availability, marking them as active before applying rules.
        """
        shipment = context.get('shipment')
        existing_container = context.get('container')
        container_availability = context.get('container_availability')

        rules.append(SetActiveStatusRule())

        # Apply any provided rules
        if rules:
            for rule in rules:
                rule.apply(context)

        # Save or update the shipment
        self.shipment_repo.save_or_update(
            shipment, "shipment_id", shipment.shipment_id)

        # Save or update the ContainerAvailability if provided
        if container_availability and self.container_repo:
            container_availability.shipment_id = shipment.shipment_id
            self.container_repo.save_or_update(
                container_availability, "container_number", container_availability.container_number)
