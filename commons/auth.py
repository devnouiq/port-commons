from sqlalchemy.orm import Session
from commons.schemas.auth import PTPAuthToken
from commons.utils.logger import get_logger
from commons.repository import BaseRepository
from typing import Any

logger = get_logger()


def get_latest_token(session: Session, filter_field: str, filter_value: Any):
    # Initialize the repository
    auth_repo = BaseRepository(session, PTPAuthToken)

    # Fetch the latest token based on the provided filter
    latest_token = auth_repo.get_latest_by_field(filter_field, filter_value)

    if latest_token:
        logger.info(
            f"Fetched the latest token from the database for {filter_field}={filter_value}: {latest_token.token}")
        return latest_token.token
    else:
        logger.error(f"No token found for {filter_field}={filter_value}.")
        raise Exception(f"No token found for {filter_field}={filter_value}.")
