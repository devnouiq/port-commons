from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from commons.schemas.base import Base
import os
from commons.utils.logger import get_logger
from contextlib import contextmanager
from .scraper_metadata import ScraperMetadata
from .enums import Scraper

logger = get_logger()

# Create engines and sessions
engine = create_engine(os.getenv("DATABASE_URL"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_session():
    """Provide a transactional scope around a series of operations."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Error during session: {e}")
        raise
    finally:
        session.close()


def create_tables():
    """Create tables if they do not exist."""
    try:
        Base.metadata.create_all(engine)
        initialize_data()
        logger.info("Tables created successfully.")
    except SQLAlchemyError as e:
        logger.error(f"Error creating tables: {e}")
        raise


def initialize_data():
    """Insert initial data into the scraper_metadata table."""
    with get_session() as session:
        try:
            # Check if there are already records to avoid duplicates
            if session.query(ScraperMetadata).count() == 0:
                initial_data = [
                    ScraperMetadata(
                        scraper_friendly_name="APM Terminal Scraper",
                        scraper_id=Scraper.APM,
                        terminal_id="APM",
                        scrape_frequency_hours=24,
                        is_active=True,
                        scraper_version="1.0.0"
                    ),
                    ScraperMetadata(
                        scraper_friendly_name="MAHER Terminal Scraper",
                        scraper_id=Scraper.MAHER,
                        terminal_id="MAHER",
                        scrape_frequency_hours=12,
                        is_active=True,
                        scraper_version="1.0.0"
                    ),
                    # Add more initial rows as needed
                ]
                session.add_all(initial_data)
                session.commit()
                logger.info("Initial data inserted successfully.")
            else:
                logger.info("Data already exists. Skipping initialization.")
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Error inserting initial data: {e}")
            raise

create_tables()