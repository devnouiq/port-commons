from loguru import logger as loguru_logger
from datetime import datetime
import uuid


class Logger:
    _instance = None

    def __new__(cls, scraper_name: str = None):
        if cls._instance is None:
            if scraper_name is None:
                raise ValueError(
                    "Logger needs a scraper name for the first initialization.")
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.scraper_name = scraper_name
            cls._instance.run_id = uuid.uuid4()
            cls._instance.start_time = datetime.utcnow().isoformat()

            loguru_logger.remove()
            loguru_logger.add(lambda msg: print(msg, end=''),
                              format=cls._log_format(cls._instance))

        return cls._instance

    def info(self, message):
        loguru_logger.info(message)

    def error(self, message):
        loguru_logger.error(message)

    def warning(self, message):
        loguru_logger.warning(message)

    def debug(self, message):
        loguru_logger.debug(message)

    @staticmethod
    def _log_format(instance):
        return (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            f"<cyan>{instance.scraper_name}</cyan> | "
            f"<magenta>{instance.run_id}</magenta> | "
            "<level>{message}</level>"
        )


def get_logger(scraper_name: str = None):
    if Logger._instance is None and scraper_name is None:
        raise ValueError(
            "Logger needs a scraper name for the first initialization.")
    return Logger(scraper_name=scraper_name)
