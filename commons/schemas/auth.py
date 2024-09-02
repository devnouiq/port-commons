from sqlalchemy import Column, Integer, String
from .base import Base


class PTPAuthToken(Base):
    __tablename__ = "auth_tokens"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, nullable=False)
