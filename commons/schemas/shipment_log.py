import uuid
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from commons.enums import ScrapeStatus

class ShipmentLog(Base):
    __tablename__ = "shipment_logs"

    log_id = Column(UUID(as_uuid=True), primary_key=True,
                         default=uuid.uuid4, unique=True, nullable=False)
    shipment_id = Column(UUID(as_uuid=True), ForeignKey(
        "shipments.shipment_id"), nullable=False)
    # Status at the time of logging
    scrape_status = Column(Enum(ScrapeStatus), nullable=True)
    # Timestamp for the event, default to current time
    scraped_at = Column(DateTime, nullable=False)
    # (Optional) Snapshot of data after update
    new_data = Column(JSON, nullable=True)

    # Establish relationship with Shipment
    shipment = relationship("Shipment", back_populates="logs")

    def __repr__(self):
        return (f"<ShipmentLog(log_id={self.log_id}, shipment_id={self.shipment_id}, "
                f"scrape_status='{self.scrape_status}')>")