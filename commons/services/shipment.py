from commons.repository import BaseRepository
from commons.enums import ScrapeStatus
from commons.utils.date import get_current_datetime_in_est
from commons.utils.logger import get_logger
from sqlalchemy.orm import Session

logger = get_logger()


class ShipmentService:
    def __init__(self, session: Session, shipment_repo: BaseRepository, container_repo: BaseRepository, rules: list):
        self.session = session
        self.shipment_repo = shipment_repo
        self.container_repo = container_repo
        self.rules = rules

    def process_active(self, shipment, existing_container, container_availability):
        """
        Process a shipment and container availability, marking them as active before applying rules.
        """
        # Mark the shipment and container availability as ACTIVE
        shipment.scrape_status = ScrapeStatus.ACTIVE
        shipment.last_scraped_time = get_current_datetime_in_est()

        # Call the process method to apply rules and save the data
        self.process(shipment, existing_container, container_availability)

    def process(self, shipment, existing_container, container_availability):
        """
        Apply the business rules and save the updated shipment and container availability.
        """
        # Apply rules to shipment and container availability
        for rule in self.rules:
            rule.apply(
                {"shipment": shipment, "container_availability": container_availability})

        # Save or update the shipment
        self.shipment_repo.save_or_update(
            shipment, "shipment_id", shipment.shipment_id)

        # Save or update the ContainerAvailability
        container_availability.shipment_id = shipment.shipment_id
        self.container_repo.save_or_update(
            container_availability, "container_number", container_availability.container_number)
