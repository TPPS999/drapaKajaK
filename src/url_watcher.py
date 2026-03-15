#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
URL Watcher - monitoruje konkretne linki Kayak i śledzi zmiany cen.

Użycie:
    python src/url_watcher.py              # rolling mode z config/url_watchlist.json
    python src/url_watcher.py --once       # jednorazowe sprawdzenie

Dodaj linki do config/url_watchlist.json i uruchom skrypt.
Wyniki zapisywane do output/url_watcher/prices_YYYYMMDD.csv
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import csv
import json
import logging
import os
import random
import re
import time
from datetime import datetime
from typing import Optional
from urllib.parse import parse_qs, urlparse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

CONFIG_PATH = "config/url_watchlist.json"
OUTPUT_DIR = "output/url_watcher"

CSV_FIELDS = [
    "timestamp",
    "origin",
    "destination",
    "departure_date",
    "return_date",
    "passengers",
    "airline_code",
    "price_per_person",
    "total_price",
    "status",
    "error",
    "url",
]


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

def load_config() -> Optional[dict]:
    if not os.path.exists(CONFIG_PATH):
        logger.error("Config nie znaleziony: %s", CONFIG_PATH)
        logger.info("Utwórz plik na podstawie config/url_watchlist.json")
        return None
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(config: dict):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# URL parsing
# ---------------------------------------------------------------------------

def parse_kayak_url(url: str) -> dict:
    """Parsuje URL Kayak i zwraca słownik z parametrami lotu."""
    try:
        parsed = urlparse(url.strip())
        if "kayak" not in parsed.netloc:
            return {}
        parts = parsed.path.strip("/").split("/")
        if len(parts) < 5 or parts[0] != "flights":
            return {}

        route = parts[1]
        if "-" not in route:
            return {}
        origin, destination = route.split("-", 1)

        departure_date = parts[2]
        return_date = parts[3]

        pax_match = re.match(r"(\d+)", parts[4])
        passengers = int(pax_match.group(1)) if pax_match else 1

        qs = parse_qs(parsed.query)
        fs = qs.get("fs", [""])[0]

        # Wyciągnij kod linii lotniczej z parametru fs
        airline_match = re.search(r"airlines[%3D=]+([A-Z]+)", fs.upper())
        airline_code = airline_match.group(1) if airline_match else ""

        return {
            "origin": origin.upper(),
            "destination": destination.upper(),
            "departure_date": departure_date,
            "return_date": return_date,
            "passengers": passengers,
            "airline_code": airline_code,
            "airline_filter": fs,
        }
    except Exception as exc:
        logger.error("Błąd parsowania URL: %s", exc)
        return {}


# ---------------------------------------------------------------------------
# Chrome driver
# ---------------------------------------------------------------------------

def create_driver():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

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
    return webdriver.Chrome(service=service, options=options)


# ---------------------------------------------------------------------------
# Price extraction
# ---------------------------------------------------------------------------

def extract_price(text: str) -> tuple[Optional[float], Optional[float]]:
    """Wyciąga cenę za osobę i łączną z tekstu strony Kayak.pl.
    Zwraca (cena_za_osobe, cena_lacznie). Oba mogą być None.
    """
    text = text.replace("\xa0", " ")

    def clean(s: str) -> float:
        return float(re.sub(r"\s", "", s))

    # Główny wzorzec: "X zł / osoba ... Y zł łącznie"
    primary = re.search(
        r"(\d[\d ]{0,9}\d|\d{3,})\s*z[łl]\s*/\s*osoba.{0,80}?"
        r"(\d[\d ]{0,9}\d|\d{3,})\s*z[łl]\s*[łl][\u0105cC]cznie",
        text,
        re.IGNORECASE | re.DOTALL,
    )
    if primary:
        try:
            per_person = clean(primary.group(1))
            total = clean(primary.group(2))
            if 100 <= per_person <= 200_000:
                return per_person, total
        except ValueError:
            pass

    # Fallback: zbierz wszystkie kwoty w PLN i weź najmniejszą sensowną
    all_amounts = re.findall(r"(\d[\d ]{0,9}\d|\d{3,})\s*z[łl]", text, re.IGNORECASE)
    prices = []
    for raw in all_amounts:
        try:
            val = clean(raw)
            if 100 <= val <= 200_000:
                prices.append(val)
        except ValueError:
            continue

    if not prices:
        return None, None

    prices.sort()
    per_person = prices[0]
    total = next(
        (p for p in prices[1:] if 1.4 * per_person <= p <= 4.5 * per_person), None
    )
    return per_person, total


# ---------------------------------------------------------------------------
# Single URL scrape
# ---------------------------------------------------------------------------

def scrape_url(url: str, wait_min: int = 12, wait_max: int = 18) -> dict:
    """Otwiera URL i zwraca słownik z ceną i metadanymi."""
    driver = None
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    info = parse_kayak_url(url)

    result = {
        "timestamp": timestamp,
        "url": url,
        "origin": info.get("origin", ""),
        "destination": info.get("destination", ""),
        "departure_date": info.get("departure_date", ""),
        "return_date": info.get("return_date", ""),
        "passengers": info.get("passengers", ""),
        "airline_code": info.get("airline_code", ""),
        "price_per_person": None,
        "total_price": None,
        "status": "error",
        "error": None,
    }

    try:
        driver = create_driver()

        label = (
            f"{info.get('origin','?')}-{info.get('destination','?')} "
            f"{info.get('departure_date','')} [{info.get('airline_code','ANY')}]"
        )
        logger.info("Otwieram: %s", label)
        driver.get(url)

        wait = wait_min + random.uniform(0, wait_max - wait_min)
        logger.info("Czekam %.0fs na załadowanie cen...", wait)
        time.sleep(wait)

        page_text = driver.execute_script("return document.body.innerText") or ""
        per_person, total = extract_price(page_text)

        if per_person is not None:
            result["price_per_person"] = per_person
            result["total_price"] = total
            result["status"] = "ok"
            if total:
                logger.info("  Cena: %.0f PLN/os  (łącznie: %.0f PLN)", per_person, total)
            else:
                logger.info("  Cena: %.0f PLN/os", per_person)
        else:
            result["error"] = "Cena nie znaleziona"
            logger.warning("  Nie znaleziono ceny")

    except Exception as exc:
        result["error"] = str(exc)
        logger.error("  Błąd scrapingu: %s", exc)
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass

    return result


# ---------------------------------------------------------------------------
# CSV output
# ---------------------------------------------------------------------------

def save_result(result: dict, output_dir: str = OUTPUT_DIR):
    os.makedirs(output_dir, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    csv_path = os.path.join(output_dir, f"prices_{date_str}.csv")

    write_header = not os.path.exists(csv_path)
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction="ignore")
        if write_header:
            writer.writeheader()
        writer.writerow(result)

    logger.debug("Zapisano do: %s", csv_path)


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def run_watcher(config: dict, once: bool = False):
    urls_raw = config.get("urls", [])
    urls = [u.strip() for u in urls_raw if u.strip() and not u.strip().startswith("#")]

    if not urls:
        logger.error("Brak URLi w watchlistcie. Dodaj linki do %s", CONFIG_PATH)
        return

    delay_cfg = config.get("delay_between_urls_seconds", [20, 35])
    delay_min, delay_max = delay_cfg[0], delay_cfg[1]
    interval_min = config.get("check_interval_minutes", 60)
    rolling = not once and config.get("rolling_mode", True)

    logger.info("Watchlist: %d URLi | interwał: %dmin | rolling: %s",
                len(urls), interval_min, rolling)
    logger.info("=" * 60)

    round_num = 1
    while True:
        logger.info("\n%s", "=" * 60)
        logger.info("RUNDA %d — %s", round_num, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        logger.info("%s\n", "=" * 60)

        for i, url in enumerate(urls, 1):
            logger.info("[%d/%d]", i, len(urls))
            result = scrape_url(url, wait_min=12, wait_max=18)
            save_result(result)

            if i < len(urls):
                delay = delay_min + random.uniform(0, delay_max - delay_min)
                logger.info("Czekam %.0fs przed kolejnym URLem...\n", delay)
                time.sleep(delay)

        logger.info("\nRunda %d zakończona.", round_num)

        if not rolling:
            break

        logger.info("Następne sprawdzenie za %d minut...", interval_min)
        time.sleep(interval_min * 60)
        round_num += 1


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    once_mode = "--once" in sys.argv
    cfg = load_config()
    if cfg:
        run_watcher(cfg, once=once_mode)
