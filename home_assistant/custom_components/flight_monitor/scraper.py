"""Kayak flight price scraper using headless Chrome."""
from __future__ import annotations

import logging
import random
import re
import time
from dataclasses import dataclass
from typing import Optional
from urllib.parse import parse_qs, urlparse

_LOGGER = logging.getLogger(__name__)


@dataclass
class FlightInfo:
    """Parsed flight parameters from a Kayak URL."""
    origin: str
    destination: str
    departure_date: str
    return_date: str
    passengers: int
    url: str
    airline_filter: str = ""

    @property
    def route(self) -> str:
        return f"{self.origin} → {self.destination}"


@dataclass
class ScrapeResult:
    """Result of a scraping attempt."""
    success: bool
    price_per_person: Optional[float] = None
    total_price: Optional[float] = None
    error: Optional[str] = None


def parse_kayak_url(url: str) -> Optional[FlightInfo]:
    """Parse a Kayak URL and extract flight parameters.

    Supports formats like:
    https://www.kayak.pl/flights/WAW-ICN/2025-10-22/2025-11-10/2adults?sort=price_a&fs=...
    https://www.kayak.com/flights/WAW-ICN/2025-10-22/2025-11-10/2adults?...
    """
    try:
        parsed = urlparse(url.strip())

        if "kayak" not in parsed.netloc:
            return None

        # Strip leading slash and split path
        parts = parsed.path.strip("/").split("/")
        # Expected: ['flights', 'WAW-ICN', '2025-10-22', '2025-11-10', '2adults']
        if len(parts) < 5 or parts[0] != "flights":
            return None

        route = parts[1]
        if "-" not in route:
            return None
        origin, destination = route.split("-", 1)
        if len(origin) != 3 or len(destination) != 3:
            return None

        departure_date = parts[2]
        return_date = parts[3]

        # Validate date format YYYY-MM-DD
        if not re.match(r"\d{4}-\d{2}-\d{2}", departure_date):
            return None
        if not re.match(r"\d{4}-\d{2}-\d{2}", return_date):
            return None

        passengers_str = parts[4]
        pax_match = re.match(r"(\d+)adults?", passengers_str, re.IGNORECASE)
        passengers = int(pax_match.group(1)) if pax_match else 1

        # Extract airline filter from query string
        airline_filter = ""
        if parsed.query:
            qs = parse_qs(parsed.query, keep_blank_values=True)
            if "fs" in qs:
                airline_filter = f"fs={qs['fs'][0]}"

        return FlightInfo(
            origin=origin.upper(),
            destination=destination.upper(),
            departure_date=departure_date,
            return_date=return_date,
            passengers=passengers,
            url=url,
            airline_filter=airline_filter,
        )

    except Exception as exc:
        _LOGGER.error("Failed to parse Kayak URL '%s': %s", url, exc)
        return None


def extract_price(text: str) -> tuple[Optional[float], Optional[float]]:
    """Extract per-person and total price from Kayak page text.

    Returns (price_per_person, total_price). Both may be None if not found.
    Kayak.pl formats:
      '1 234 zł / osoba   2 468 zł łącznie'
      '3 500 zł / osoba\n7 000 zł łącznie'
    Thousands separator on Kayak.pl is a regular space or non-breaking space (\xa0).
    """
    # Normalize non-breaking spaces to regular spaces for easier matching
    text = text.replace("\xa0", " ")

    def parse_num(s: str) -> float:
        return float(re.sub(r"[\s]", "", s))

    # Primary: "X zł / osoba ... Y zł łącznie"
    # Allow up to 60 chars between "osoba" and the total (newlines, other text)
    primary = re.search(
        r"(\d[\d ]{0,9}\d|\d)\s*z[łl]\s*/\s*osoba.{0,60}?"
        r"(\d[\d ]{0,9}\d|\d)\s*z[łl]\s*[łl][\u0105cC]cznie",
        text,
        re.IGNORECASE | re.DOTALL,
    )
    if primary:
        try:
            per_person = parse_num(primary.group(1))
            total = parse_num(primary.group(2))
            if 100 <= per_person <= 200_000:
                return per_person, total
        except ValueError:
            pass

    # Fallback: collect all currency amounts and take the smallest reasonable one
    all_amounts = re.findall(r"(\d[\d ]{0,9}\d|\d{3,})\s*z[łl]", text, re.IGNORECASE)
    prices = []
    for raw in all_amounts:
        try:
            val = parse_num(raw)
            if 100 <= val <= 200_000:
                prices.append(val)
        except ValueError:
            continue

    if not prices:
        return None, None

    prices.sort()
    per_person = prices[0]
    # Try to find a matching total (roughly 1.5x–4x per-person for 1–4 passengers)
    total = None
    for p in prices[1:]:
        if 1.4 * per_person <= p <= 4.5 * per_person:
            total = p
            break

    return per_person, total


def scrape_price(url: str) -> ScrapeResult:
    """Open Kayak URL with headless Chrome and extract the cheapest price.

    This is a blocking function — call via hass.async_add_executor_job().
    """
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
    except ImportError as exc:
        return ScrapeResult(success=False, error=f"Missing dependency: {exc}")

    driver = None
    try:
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        _LOGGER.debug("Opening URL: %s", url)
        driver.get(url)

        # Kayak needs time for JS to load and render prices
        wait = 12 + random.uniform(2, 5)
        _LOGGER.debug("Waiting %.1f seconds for prices to load...", wait)
        time.sleep(wait)

        page_text = driver.execute_script("return document.body.innerText") or ""

        per_person, total = extract_price(page_text)

        if per_person is not None:
            _LOGGER.info(
                "Scraped price: %.0f PLN/person (total: %s PLN) from %s",
                per_person,
                f"{total:.0f}" if total else "?",
                url,
            )
            return ScrapeResult(
                success=True,
                price_per_person=per_person,
                total_price=total,
            )
        else:
            _LOGGER.warning("No price found on page: %s", url)
            return ScrapeResult(success=False, error="Price not found on page")

    except Exception as exc:
        _LOGGER.error("Scraping error for %s: %s", url, exc)
        return ScrapeResult(success=False, error=str(exc))
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass
