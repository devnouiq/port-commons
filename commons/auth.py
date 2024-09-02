from sqlalchemy.orm import Session
from commons.schemas.auth import PTPAuthToken
from commons.utils.logger import get_logger
from commons.repository import BaseRepository
logger = get_logger()


def get_latest_token(session: Session):
    try:
        auth_repo = BaseRepository(session, PTPAuthToken)
        latest_token = auth_repo.get_latest("id")

        if latest_token:
            logger.info(
                f"Fetched the latest token from the database: {latest_token.token}")
            return latest_token.token
        else:
            logger.error("No token found in the database.")
            return None
    except Exception as e:
        logger.error(f"Failed to fetch the latest token: {e}")
        return None
