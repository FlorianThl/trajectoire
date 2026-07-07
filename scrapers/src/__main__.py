import logging
from src.config import settings
from src.scrapers.m2r import M2RScraper
from src.scrapers.rs_trackdays import RSTrackdaysScraper

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting scrapers")
    scrapers = [
        M2RScraper(settings.database_url),
        RSTrackdaysScraper(settings.database_url),
    ]
    for scraper in scrapers:
        try:
            scraper.run()
        except Exception as e:
            logger.error(f"Scraper {type(scraper).__name__} failed: {e}")
        finally:
            scraper.close()
    logger.info("Scrapers finished")

if __name__ == "__main__":
    main()
