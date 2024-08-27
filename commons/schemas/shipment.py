from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey
from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from commons.enums import ScrapeStatus
from .base import Base


class ContainerAvailability(Base):
    __tablename__ = "container_status_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    shipment_id = Column(Integer, ForeignKey("shipments.shipment_id"))
    date = Column(String, nullable=True)  # Store as ISO 8601 string
    port = Column(String, nullable=False)
    terminal = Column(String, nullable=False)
    container_number = Column(String, nullable=False, unique=True)
    available = Column(String, nullable=False)
    usda_status = Column(String, nullable=True)
    last_free_date = Column(String, nullable=True)  # Store as ISO 8601 string
    location = Column(String, nullable=True)
    custom_release_status = Column(String, nullable=True)
    carrier_release_status = Column(String, nullable=True)
    demurrage_amount = Column(String, nullable=True)
    yard_terminal_release_status = Column(String, nullable=True)
    last_updated_availability = Column(
        String, nullable=False)  # Store as ISO 8601 string

    shipment = relationship("Shipment", back_populates="containers")

    def __repr__(self):
        return (f"<ContainerAvailability(container_number='{self.container_number}', "
                f"available='{self.available}', "
                f"last_updated_availability='{self.last_updated_availability}')>")


class Shipment(Base):
    __tablename__ = 'shipments'

    shipment_id = Column(Integer, primary_key=True)
    container_number = Column(String(30), nullable=True)
    master_bol_number = Column(String(30), nullable=True)
    house_bol_number = Column(String(30), nullable=True)
    run_date = Column(String, nullable=True)  # Store as ISO 8601 string
    vessel_name = Column(String(25), nullable=True)
    voyage_id = Column(Integer, nullable=True)
    terminal_id = Column(String(10), nullable=True)
    error = Column(Text, nullable=True)
    scrape_status = Column(Enum(ScrapeStatus),
                           default=ScrapeStatus.ASSIGNED.name, nullable=False)
    submitted_at = Column(String, nullable=True)  # Store as ISO 8601 string
    frequency = Column(Integer, nullable=True, default=4)
    # Store as ISO 8601 string
    last_scraped_time = Column(String, nullable=True)
    # Store as ISO 8601 string
    next_scrape_time = Column(String, nullable=True)
    # Store as ISO 8601 string
    start_scrape_time = Column(String, nullable=True)

    containers = relationship("ContainerAvailability",
                              back_populates="shipment")

    def __repr__(self):
        return (f"<Shipment(shipment_id={self.shipment_id}, "
                f"container_number='{self.container_number}', "
                f"scrape_status='{self.scrape_status.value}')>")
