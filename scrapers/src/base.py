import httpx
import psycopg2
import logging
from typing import Any

logger = logging.getLogger(__name__)

class BaseScraper:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.conn = psycopg2.connect(db_url)
        self.client = httpx.Client(timeout=30.0, follow_redirects=True)

    def fetch(self, url: str) -> str:
        resp = self.client.get(url)
        resp.raise_for_status()
        return resp.text

    def parse(self, html: str) -> list[dict]:
        raise NotImplementedError

    def save(self, events: list[dict]):
        cur = self.conn.cursor()
        for ev in events:
            cur.execute("""
                INSERT INTO events (circuit_id, organizer_name, organizer_url, start_date, end_date,
                    has_debutant, has_intermediaire, has_confirme, price_base, price_license,
                    booking_url, spots_available, is_active, scraped_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, true, NOW())
                ON CONFLICT DO NOTHING
            """, (
                ev["circuit_id"], ev["organizer_name"], ev["organizer_url"],
                ev["start_date"], ev["end_date"],
                ev.get("has_debutant", False), ev.get("has_intermediaire", False),
                ev.get("has_confirme", False), ev.get("price_base"),
                ev.get("price_license"), ev.get("booking_url"), ev.get("spots_available"),
            ))
        self.conn.commit()
        cur.close()
        logger.info(f"Saved {len(events)} events")

    def run(self):
        raise NotImplementedError

    def close(self):
        self.client.close()
        self.conn.close()
