from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, PrimaryKeyConstraint, Text, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from commons.utils.date import get_current_datetime_in_est
from commons.enums import ScrapeStatus
import uuid


class ContainerAvailability(Base):
    __tablename__ = "container_status_table"

    shipment_id = Column(UUID(as_uuid=True), ForeignKey(
        "shipments.shipment_id"), nullable=False)
    container_number = Column(String, nullable=False)
    vessel_eta = Column(String, nullable=True)
    port = Column(String, nullable=False)
    terminal = Column(String, nullable=False)
    available = Column(String, nullable=False)
    last_free_day = Column(String, nullable=True)
    location = Column(String, nullable=True)
    custom_release_status = Column(String, nullable=True)
    carrier_release_status = Column(String, nullable=True)
    demurrage_amount = Column(String, nullable=True)
    yard_terminal_release_status = Column(String, nullable=True)
    type_code = Column(String, nullable=True)
    departed_terminal = Column(String, nullable=True)
    holds = Column(String, nullable=True)
    charges = Column(String, nullable=True)
    demurage = Column(String, nullable=True)
    line = Column(String, nullable=True)
    additional_info = Column(JSON, nullable=True)

    shipment = relationship("Shipment", back_populates="containers")

    def __repr__(self):
        return (f"<ContainerAvailability(container_number='{self.container_number}', "
                f"available='{self.available}")

    # Define composite primary key
    __table_args__ = (
        PrimaryKeyConstraint('shipment_id', 'container_number'),
    )


class Shipment(Base):
    __tablename__ = 'shipments'

    shipment_id = Column(UUID(as_uuid=True), primary_key=True,
                         default=uuid.uuid4, unique=True, nullable=False)
    container_number = Column(String(30), nullable=True)
    master_bol_number = Column(String(30), nullable=True)
    house_bol_number = Column(String(30), nullable=True)
    run_date = Column(DateTime, nullable=True)  # Store as DateTime
    voyage_id = Column(Integer, nullable=True)
    terminal_id = Column(String(40), nullable=True)
    vessel_name = Column(String(25), nullable=True)
    error = Column(Text, nullable=True)
    scrape_status = Column(Enum(ScrapeStatus),
                           default=ScrapeStatus.ASSIGNED.name, nullable=False)
    submitted_at = Column(DateTime, nullable=True,
                          default=get_current_datetime_in_est())  # Store as DateTime
    frequency = Column(Integer, nullable=True, default=4)
    last_scraped_time = Column(DateTime, nullable=True)  # Store as DateTime
    next_scrape_time = Column(
        DateTime, nullable=True, default=get_current_datetime_in_est())  # Store as DateTime
    start_scrape_time = Column(DateTime, nullable=True)  # Store as DateTime
    reference_id = Column(String, nullable=True)
    company_code = Column(String, nullable=True)
    vessel_orig_eta = Column(DateTime, nullable=True)  # Store as DateTime
    run_id = Column(UUID(as_uuid=True), nullable=True)

    containers = relationship("ContainerAvailability",
                              back_populates="shipment")

    def __repr__(self):
        return (f"<Shipment(shipment_id={self.shipment_id}, "
                f"container_number='{self.container_number}', "
                f"scrape_status='{self.scrape_status.value}')>")
