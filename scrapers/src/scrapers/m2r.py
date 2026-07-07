from bs4 import BeautifulSoup
from src.base import BaseScraper
import logging

logger = logging.getLogger(__name__)

class M2RScraper(BaseScraper):
    BASE_URL = "https://m2r-trackdays.fr"

    def parse(self, html: str) -> list[dict]:
        soup = BeautifulSoup(html, "lxml")
        events = []
        logger.info(f"Parsed {len(events)} events from M2R")
        return events

    def run(self):
        html = self.fetch(self.BASE_URL + "/calendrier")
        events = self.parse(html)
        self.save(events)
