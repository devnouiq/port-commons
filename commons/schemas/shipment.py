from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from commons.enums import ScrapeStatus
from .base import Base
from sqlalchemy.sql import func


class ContainerAvailability(Base):
    __tablename__ = "container_status_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    shipment_id = Column(Integer, ForeignKey("shipments.shipment_id"))
    date = Column(DateTime, nullable=True)
    port = Column(String, nullable=False)
    terminal = Column(String, nullable=False)
    container_number = Column(String, nullable=False, unique=True)
    available = Column(String, nullable=False)
    usda_status = Column(String, nullable=True)
    last_free_date = Column(String, nullable=True)
    location = Column(String, nullable=True)
    custom_release_status = Column(String, nullable=True)
    carrier_release_status = Column(String, nullable=True)
    demurrage_amount = Column(String, nullable=True)
    yard_terminal_release_status = Column(String, nullable=True)
    last_updated_availability = Column(
        DateTime, nullable=False, default=func.current_timestamp())

    # Use string reference here
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
    run_date = Column(DateTime, nullable=True)
    vessel_name = Column(String(25), nullable=True)
    voyage_id = Column(Integer, nullable=True)
    terminal_id = Column(String(10), nullable=True)
    status = Column(String(20), nullable=True)
    error = Column(Text, nullable=True)
    scrape_status = Column(Enum(ScrapeStatus),
                           default=ScrapeStatus.ASSIGNED, nullable=False)
    submitted_at = Column(DateTime, nullable=True)
    frequency = Column(Integer, nullable=True, default=4)
    last_scraped_time = Column(DateTime, nullable=True)
    next_scrape_time = Column(DateTime, nullable=True)
    start_scrape_time = Column(DateTime, nullable=True)

    # Use string reference here
    containers = relationship("ContainerAvailability",
                              back_populates="shipment")

    def __repr__(self):
        return (f"<Shipment(shipment_id={self.shipment_id}, "
                f"container_number='{self.container_number}', "
                f"status='{self.status}', "
                f"scrape_status='{self.scrape_status.value}')>")
