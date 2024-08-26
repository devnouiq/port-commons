from sqlalchemy import Column, String, Integer, Boolean, DateTime, Enum, func
from ..enums import Scraper
from .base import Base


class ScraperMetadata(Base):
    __tablename__ = "scraper_metadata"

    id = Column(Integer, primary_key=True, autoincrement=True)
    scraper_friendly_name = Column(
        String, nullable=False, comment="A human-friendly name for the scraper")
    scraper_id = Column(Enum(Scraper), nullable=True,
                        comment="Unique identifier for the scraper")
    terminal_id = Column(String, nullable=False,
                         comment="Terminal ID associated with the scraper")
    scrape_frequency_hours = Column(
        Integer, nullable=False, comment="Frequency of scraping in hours")
    last_scraped_time = Column(DateTime(
        timezone=True), nullable=True, comment="The last time the scraper was run, in UTC")
    is_active = Column(Boolean, default=True, nullable=False,
                       comment="Indicates whether the scraper is currently active")
    scraper_version = Column(String, nullable=True,
                             comment="Version of the scraper")
    created_at = Column(DateTime(timezone=True), server_default=func.now(
    ), nullable=False, comment="Timestamp when the scraper was created, in UTC")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(
    ), nullable=True, comment="Timestamp when the scraper was last updated, in UTC")

    def __repr__(self):
        """
        Return a string representation of the ScraperMetadata instance with all attributes.
        """
        return (
            f"<ScraperMetadata(id={self.id}, "
            f"scraper_friendly_name='{self.scraper_friendly_name}', "
            f"scraper_id='{self.scraper_id}', "
            f"terminal_id='{self.terminal_id}', "
            f"scrape_frequency_hours={self.scrape_frequency_hours}, "
            f"last_scraped_time={self.last_scraped_time}, "
            f"is_active={self.is_active}, "
            f"scraper_version='{self.scraper_version}', "
            f"created_at={self.created_at}, "
            f"updated_at={self.updated_at})>"
        )
