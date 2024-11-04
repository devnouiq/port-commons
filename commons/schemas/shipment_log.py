from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from commons.enums import ScrapeStatus


class ShipmentLog(Base):
    __tablename__ = "shipment_logs"

    log_id = Column(Integer, primary_key=True, autoincrement=True)
    shipment_id = Column(UUID(as_uuid=True), ForeignKey(
        "shipments.shipment_id"), nullable=False)
    # Status at the time of logging
    scrape_status = Column(Enum(ScrapeStatus), nullable=True)
    # Timestamp for the event, default to current time
    scraped_at = Column(DateTime, nullable=False)
    # (Optional) Snapshot of data before update
    previous_data = Column(JSON, nullable=True)
    # (Optional) Snapshot of data after update
    new_data = Column(JSON, nullable=True)

    retry_count = Column(Integer, nullable=True)

    # Establish relationship with Shipment
    shipment = relationship("Shipment", back_populates="logs")

    def __repr__(self):
        return (f"<ShipmentLog(log_id={self.log_id}, shipment_id={self.shipment_id}, "
                f"event_type='{self.event_type}', scrape_status='{self.scrape_status}')>")