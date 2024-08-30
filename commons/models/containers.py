from pydantic import BaseModel
from typing import Optional


class ContainerDataModel(BaseModel):
    date: Optional[str] = None
    port: Optional[str] = None
    terminal: Optional[str] = None
    container_number: Optional[str] = None
    available: Optional[str] = None
    usda_status: Optional[str] = None
    last_free_date: Optional[str] = None
    location: Optional[str] = None
    custom_release_status: Optional[str] = None
    carrier_release_status: Optional[str] = None
    demurrage_amount: Optional[str] = None
    vessel_name: Optional[str] = None
    yard_terminal_release_status: Optional[str] = None
    last_free_date: Optional[str] = None
    last_updated_availability: Optional[str] = None
    shipment_id: Optional[int] = None

    class Config:
        from_attributes = True
