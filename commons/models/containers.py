from pydantic import BaseModel, Field
from ..utils.date import get_current_datetime_in_est
from typing import Optional


class ContainerDataModel(BaseModel):
    date: str
    port: str
    terminal: str
    container_number: str
    available: str
    usda_status: Optional[str] = None
    last_free_date: Optional[str] = None
    location: Optional[str] = None
    custom_release_status: Optional[str] = None
    carrier_release_status: Optional[str] = None
    demurrage_amount: Optional[str] = None
    yard_terminal_release_status: Optional[str] = None
    last_updated_availability: str = Field(
        default_factory=lambda: get_current_datetime_in_est()
