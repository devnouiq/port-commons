from commons.repository import BaseRepository
from commons.enums import ScrapeStatus
from commons.utils.date import get_current_datetime_in_est
from commons.utils.logger import get_logger
from sqlalchemy.orm import Session

logger = get_logger()


class ShipmentAvailabilityService:
    def __init__(self, session: Session, shipment_repo: BaseRepository, rules: list):
        self.session = session
        self.shipment_repo = shipment_repo
        self.rules = rules

    def process_active(self, shipment, container_availability):
        """
        Process a shipment and container availability, marking them as active before applying rules.
        """
        # Mark the shipment and container availability as ACTIVE
        shipment.scrape_status = ScrapeStatus.ACTIVE
        container_availability.scrape_status = ScrapeStatus.ACTIVE
        container_availability.last_scraped_time = get_current_datetime_in_est()
        container_availability.next_scrape_time = get_current_datetime_in_est()

        # Call the process method to apply rules and save the data
        self.process(shipment, container_availability)

    def process(self, shipment, container_availability):
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

        # Since we have a FK relationship, save or update the ContainerAvailability as well
        container_availability.shipment_id = shipment.shipment_id
        self.shipment_repo.save_or_update(
            container_availability, "container_number", container_availability.container_number)
