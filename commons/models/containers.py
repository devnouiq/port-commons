from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from commons.utils.date import get_current_datetime_in_est


class ContainerDataModel(BaseModel):
    # Assuming date is stored as DateTime in the database
    date: Optional[datetime] = None
    port: str
    terminal: str
    container_number: str
    available: str
    usda_status: Optional[str] = None
    # Assuming last_free_date is stored as DateTime
    last_free_date: Optional[datetime] = None
    location: Optional[str] = None
    custom_release_status: Optional[str] = None
    carrier_release_status: Optional[str] = None
    demurrage_amount: Optional[str] = None
    vessel_name: Optional[str] = None
    yard_terminal_release_status: Optional[str] = None
    last_free_date: Optional[str] = None
    last_updated_availability: datetime = Field(
        default_factory=lambda: get_current_datetime_in_est())  # Assuming last_updated_availability is stored as DateTime

    class Config:
        orm_mode = True  # Enables compatibility with SQLAlchemy ORM objects
