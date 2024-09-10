from sqlalchemy import Column, Integer, String, DateTime
from .base import Base
from ..utils.date import get_current_datetime_in_est


class PTPAuthToken(Base):
    __tablename__ = "auth_tokens"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, nullable=False)
    updated_at = Column(DateTime, nullable=False,
                        default=get_current_datetime_in_est)
    terminal_id = Column(String(40), nullable=True)
