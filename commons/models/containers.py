from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from commons.utils.date import get_current_datetime_in_est


class ContainerDataModel(BaseModel):
    date: Optional[datetime] = None
    port: Optional[str] = None
    terminal: Optional[str] = None
    container_number: Optional[str] = None
    available: Optional[str] = None
    usda_status: Optional[str] = None
    last_free_date: Optional[datetime] = None
    location: Optional[str] = None
    custom_release_status: Optional[str] = None
    carrier_release_status: Optional[str] = None
    demurrage_amount: Optional[str] = None
    vessel_name: Optional[str] = None
    yard_terminal_release_status: Optional[str] = None
    last_free_date: Optional[str] = None
    last_updated_availability: Optional[datetime] = Field(
        default_factory=get_current_datetime_in_est)

    class Config:
        from_attributes = True