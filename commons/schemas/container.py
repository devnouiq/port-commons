from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from commons.database import Base
from sqlalchemy.sql import func
from commons.schemas.shipment import Shipment  # Import the related class


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
