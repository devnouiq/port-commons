from enum import Enum


class ScrapeStatus(Enum):
    ASSIGNED = "ASSIGNED"  # Assigned for Scraping - StartsScrapeDate is in FUTURE
    ACTIVE = "ACTIVE"  # StartsScrapeDate is NOT FUTURE and less than current time
    IN_PROGRESS = "IN_PROGRESS"  # Job is running
    INELIGIBLE = "INELIGIBLE"  # If StartsScrapeDate is not PROVIDED
    STOPPED = "STOPPED"  # WAS Available and is not found NOW
    FAILED = "FAILED"  # Scraper Failed


class Scraper(Enum):
    APM = "APM"
    MAHER = "MAHER"
    NYCT = "NYCT"
    PNCT = "PNCT"
