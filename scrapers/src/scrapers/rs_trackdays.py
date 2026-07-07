from bs4 import BeautifulSoup
from src.base import BaseScraper
import logging

logger = logging.getLogger(__name__)

class RSTrackdaysScraper(BaseScraper):
    BASE_URL = "https://rs-trackdays.com"

    def parse(self, html: str) -> list[dict]:
        soup = BeautifulSoup(html, "lxml")
        events = []
        logger.info(f"Parsed {len(events)} events from RS Trackdays")
        return events

    def run(self):
        html = self.fetch(self.BASE_URL + "/calendrier")
        events = self.parse(html)
        self.save(events)
