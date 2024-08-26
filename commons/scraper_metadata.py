from commons.schemas.scraper import ScraperMetadata
from sqlalchemy.orm import Session


def fetch_scraper_metadata_by_id(session: Session, scraper_id: str):
    """
    Fetch ScraperMetadata from the database by scraper ID.

    :param session: SQLAlchemy Session object.
    :param scraper_id: ID of the scraper (e.g., "APM").
    :return: ScraperMetadata object or None if not found.
    """
    metadata = session.query(ScraperMetadata).filter_by(
        scraper_id=scraper_id).first()
    if metadata:
        # Eager load all the attributes
        session.expunge(metadata)
    return metadata
