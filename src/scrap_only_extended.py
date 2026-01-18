#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Simple console fix
import os
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

"""
Kayak Simple Text Scraper - z konfigurowalnymi lotniskami i rolling
Tylko otwiera stronę, czeka 12s+random, kopiuje tekst - bez kombinowania z cookies
Konfiguracja w config_extended.json
ZAKTUALIZOWANY: Nazwy plików zawierają teraz kody lotnisk podobnie jak w kayak_excel_scraper
"""

import time
import random
import os
import json
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Optional
import logging

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

@dataclass
class ScrapingRequest:
    """Struktura pojedynczego zapytania"""
    departure_date: str
    return_date: str
    airline_key: str
    airline_name: str
    airline_filter: str
    passengers: int
    duration_days: int
    origin: str
    destination: str

@dataclass
class TextResult:
    """Struktura wyniku - tylko tekst"""
    request: ScrapingRequest
    timestamp: str
    url: str
    success: bool
    error_message: Optional[str]
    text_path: Optional[str]
    page_title: Optional[str]
    text_length: int

class SimpleDriver:
    """Prosta klasa driver bez fajerwerków"""

    @staticmethod
    def create_driver():
        """Podstawowy ChromeDriver z headless"""
        options = Options()

        # Tylko podstawowe opcje
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        # Jeden losowy User Agent
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]

        options.add_argument(f"--user-agent={random.choice(user_agents)}")

        # Use webdriver-manager to get correct ChromeDriver
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

class KayakTextScraper:
    """ULTRA-PROSTY scraper - tylko tekst"""

    def __init__(self, config_path: str = "config/config_extended.json", output_dir: str = "output/kayak_text_data"):
        self.output_dir = output_dir
        self.session_dir = None
        self.logger = self._setup_logger()

        # Wczytaj konfiguracje
        self.config = self._load_config(config_path)
        
        # Sprawdź czy istnieje airlines_config, jeśli nie - dodaj
        if "airlines_config" not in self.config:
            self._add_missing_airlines_config()
        
        # Airlines config jest w airlines_config (słownik z filtrami)
        self.airlines = self.config.get("airlines_config", {})

        self._create_session_folder()

    def _load_config(self, config_path: str) -> dict:
        """Wczytuje konfiguracje z JSON"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            self.logger.info(f"Wczytano config: {config_path}")
            return config
        except FileNotFoundError:
            self.logger.error(f"Nie znaleziono pliku config: {config_path}")
            self._create_default_config(config_path)
            raise
        except Exception as e:
            self.logger.error(f"Blad wczytywania config: {e}")
            raise

    def _create_default_config(self, config_path: str):
        """Tworzy domyślny config_extended.json"""
        default_config = {
            "_comment_scraping": "Konfiguracja scrapingu lotów",
            "_comment_route": "origin/destination - kody IATA lotnisk", 
            "_comment_dates": "earliest_departure - najwcześniejszy dzień wylotu (YYYY-MM-DD)",
            "_comment_dates2": "latest_return - najpóźniejszy dzień powrotu (YYYY-MM-DD)",
            "_comment_duration": "min_days/max_days - długość pobytu w dniach",
            "_comment_passengers": "passengers - liczba pasażerów (1-4)",
            "_comment_airlines": "selected_airlines - lista kluczy linii lotniczych do sprawdzenia",
            "_comment_delays": "delay_between_requests - opóźnienie między zapytaniami w sekundach [min, max]",
            "_comment_rolling": "rolling_mode - true: działa w kółko sprawdzając wszystkie kombinacje w każdej rundzie, false: jedna sesja",
            "_comment_rolling_break": "rolling_break_minutes - przerwa między rundami w rolling mode [min, max]",

            "scraping_config": {
                "origin": "WAW",
                "destination": "ICN",
                "earliest_departure": "2025-10-20",
                "latest_return": "2025-11-15",
                "departure_start": "2025-10-20",
                "departure_end": "2025-10-25",
                "return_start": "2025-11-10",
                "return_end": "2025-11-15",
                "min_days": 19,
                "max_days": 24,
                "passengers": 2,
                "selected_airlines": ["LOT", "Turkish", "Emirates", "Qatar", "China_Air"],
                "delay_between_requests": [30, 45],
                "rolling_mode": False,
                "rolling_break_minutes": [45, 90]
            },
            
            "route": {
                "origin": "WAW",
                "destination": "ICN"
            },
            
            "date_range": {
                "departure_start": "2025-10-20",
                "departure_end": "2025-10-25",
                "return_start": "2025-11-10",
                "return_end": "2025-11-15"
            },
            
            "duration_range": {
                "min_days": 19,
                "max_days": 24
            },
            
            "airlines": ["LOT", "Turkish", "Emirates", "Qatar", "China_Air"],
            "passengers": 2,
            "delay_between_requests": [30, 45],
            "rolling_mode": False,
            "rolling_break_minutes": [45, 90],
            "save_mode": "extended",

            "_comment_airlines_filters": "Filtry linii lotniczych dla Kayak - NIE ZMIENIAJ bez wiedzy o URL encoding",
            "airlines_config": {
                "LOT": {"filter": "fs=airlines%3DLO%3Bbfc%3D1", "name": "LOT Polish Airlines"},
                "Lufthansa": {"filter": "fs=airlines%3DLH%2CMULT%3Bbfc%3D1", "name": "Lufthansa + Multi"},
                "KLM": {"filter": "fs=airlines%3DKL%2CMULT%3Bbfc%3D1", "name": "KLM + Multi"},
                "Air_France": {"filter": "fs=airlines%3DAF%2CMULT%3Bbfc%3D1", "name": "Air France + Multi"},
                "Swiss": {"filter": "fs=airlines%3DLX%3Bbfc%3D1", "name": "Swiss"},
                "Austrian": {"filter": "fs=airlines%3DOS%3Bbfc%3D1", "name": "Austrian Airlines"},
                "Finnair": {"filter": "fs=airlines%3DAY%3Bbfc%3D1", "name": "Finnair"},
                "SAS": {"filter": "fs=airlines%3DSK%3Bbfc%3D1", "name": "SAS"},
                "Korean_Air": {"filter": "fs=airlines%3DKE%3Bbfc%3D1", "name": "Korean Air"},
                "All_Nippon": {"filter": "fs=airlines%3DNH%3Bbfc%3D1", "name": "All Nippon Airways"},
                "Singapore": {"filter": "fs=airlines%3DSQ%3Bbfc%3D1", "name": "Singapore Airlines"},
                "Cathay_Pacific": {"filter": "fs=airlines%3DCX%3Bbfc%3D1", "name": "Cathay Pacific"},
                "Asiana": {"filter": "fs=airlines%3DOZ%3Bbfc%3D1", "name": "Asiana Airlines"},
                "Air_China": {"filter": "fs=airlines%3DCA%3Bbfc%3D1", "name": "Air China"},
                "China_Air": {"filter": "fs=airlines%3DCA%3Bbfc%3D1", "name": "Air China"},
                "Turkish": {"filter": "fs=airlines%3DTK%2CMULT%3Bbfc%3D1", "name": "Turkish Airlines + Multi"},
                "Emirates": {"filter": "fs=airlines%3DEK%3Bbfc%3D1", "name": "Emirates"},
                "Qatar": {"filter": "fs=airlines%3DQR%3Bbfc%3D1", "name": "Qatar Airways"},
                "Etihad": {"filter": "fs=airlines%3DEY%3Bbfc%3D1", "name": "Etihad Airways"},
                "British_Airways": {"filter": "fs=airlines%3DBA%3Bbfc%3D1", "name": "British Airways"}
            }
        }

        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)

        print(f"Utworzono domyslny config: {config_path}")
        print("Edytuj plik config_extended.json i uruchom ponownie")
    
    def _add_missing_airlines_config(self):
        """Dodaje brakującą sekcję airlines_config do istniejącej konfiguracji"""
        airlines_config = {
            "LOT": {"filter": "fs=airlines%3DLO%3Bbfc%3D1", "name": "LOT Polish Airlines"},
            "Lufthansa": {"filter": "fs=airlines%3DLH%2CMULT%3Bbfc%3D1", "name": "Lufthansa + Multi"},
            "KLM": {"filter": "fs=airlines%3DKL%2CMULT%3Bbfc%3D1", "name": "KLM + Multi"},
            "Air_France": {"filter": "fs=airlines%3DAF%2CMULT%3Bbfc%3D1", "name": "Air France + Multi"},
            "Swiss": {"filter": "fs=airlines%3DLX%3Bbfc%3D1", "name": "Swiss"},
            "Austrian": {"filter": "fs=airlines%3DOS%3Bbfc%3D1", "name": "Austrian Airlines"},
            "Finnair": {"filter": "fs=airlines%3DAY%3Bbfc%3D1", "name": "Finnair"},
            "SAS": {"filter": "fs=airlines%3DSK%3Bbfc%3D1", "name": "SAS"},
            "Korean_Air": {"filter": "fs=airlines%3DKE%3Bbfc%3D1", "name": "Korean Air"},
            "All_Nippon": {"filter": "fs=airlines%3DNH%3Bbfc%3D1", "name": "All Nippon Airways"},
            "Singapore": {"filter": "fs=airlines%3DSQ%3Bbfc%3D1", "name": "Singapore Airlines"},
            "Cathay_Pacific": {"filter": "fs=airlines%3DCX%3Bbfc%3D1", "name": "Cathay Pacific"},
            "Asiana": {"filter": "fs=airlines%3DOZ%3Bbfc%3D1", "name": "Asiana Airlines"},
            "Air_China": {"filter": "fs=airlines%3DCA%3Bbfc%3D1", "name": "Air China"},
            "China_Air": {"filter": "fs=airlines%3DCA%3Bbfc%3D1", "name": "Air China"},
            "Turkish": {"filter": "fs=airlines%3DTK%2CMULT%3Bbfc%3D1", "name": "Turkish Airlines + Multi"},
            "Emirates": {"filter": "fs=airlines%3DEK%3Bbfc%3D1", "name": "Emirates"},
            "Qatar": {"filter": "fs=airlines%3DQR%3Bbfc%3D1", "name": "Qatar Airways"},
            "Etihad": {"filter": "fs=airlines%3DEY%3Bbfc%3D1", "name": "Etihad Airways"},
            "British_Airways": {"filter": "fs=airlines%3DBA%3Bbfc%3D1", "name": "British Airways"}
        }
        
        self.config["airlines_config"] = airlines_config
        
        # Zapisz zaktualizowaną konfigurację
        try:
            with open("config/config_extended.json", 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            self.logger.info("Dodano brakujaca sekcje airlines_config do konfiguracji")
        except Exception as e:
            self.logger.error(f"Blad zapisu konfiguracji: {e}")

    def _setup_logger(self):
        """Logger"""
        logger = logging.getLogger('KayakTextScraper')
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _create_session_folder(self):
        """Folder sesji"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Sprawdź czy rolling mode
        if self.config and self.config.get("scraping_config", {}).get("rolling_mode", False):
            # Rolling mode - wszystko w jednym katalogu
            self.session_dir = os.path.join(self.output_dir, "rolling_mode")
            os.makedirs(self.session_dir, exist_ok=True)
            self.logger.info(f"Rolling mode - wszystkie pliki w: {self.session_dir}")
        else:
            # Standard mode - katalog z timestamp
            self.session_dir = os.path.join(self.output_dir, f"txt_session_{timestamp}")
            os.makedirs(self.session_dir, exist_ok=True)
            self.logger.info(f"Sesja: {self.session_dir}")

    def generate_date_combinations_rolling(self, earliest_departure: str, latest_return: str,
                                         min_days: int, max_days: int) -> List[tuple]:
        """Generuje kombinacje dat w trybie rolling (przesuwające się okno)"""
        try:
            earliest_dep = datetime.strptime(earliest_departure, "%Y-%m-%d").date()
            latest_ret = datetime.strptime(latest_return, "%Y-%m-%d").date()

            combinations = []

            # W trybie rolling: dla każdego dnia w zakresie, sprawdź wszystkie długości pobytu
            current_departure = earliest_dep

            while current_departure <= latest_ret:
                for duration in range(min_days, max_days + 1):
                    return_date = current_departure + timedelta(days=duration)

                    # Sprawdź czy data powrotu mieści się w zakresie
                    if return_date <= latest_ret:
                        combinations.append((
                            current_departure.strftime("%Y-%m-%d"),
                            return_date.strftime("%Y-%m-%d"),
                            duration
                        ))

                current_departure += timedelta(days=1)

            self.logger.info(f"{len(combinations)} kombinacji dat (rolling mode)")
            return combinations

        except Exception as e:
            self.logger.error(f"Blad dat rolling: {e}")
            return []

    def generate_date_combinations_standard(self, earliest_departure: str, latest_return: str,
                                          min_days: int, max_days: int) -> List[tuple]:
        """Generuje kombinacje dat w trybie standardowym"""
        try:
            earliest_dep = datetime.strptime(earliest_departure, "%Y-%m-%d").date()
            latest_ret = datetime.strptime(latest_return, "%Y-%m-%d").date()

            combinations = []

            for duration in range(min_days, max_days + 1):
                latest_possible_departure = latest_ret - timedelta(days=duration)

                if latest_possible_departure < earliest_dep:
                    continue

                current_departure = earliest_dep
                while current_departure <= latest_possible_departure:
                    return_date = current_departure + timedelta(days=duration)

                    if return_date <= latest_ret:
                        combinations.append((
                            current_departure.strftime("%Y-%m-%d"),
                            return_date.strftime("%Y-%m-%d"),
                            duration
                        ))

                    current_departure += timedelta(days=1)

            self.logger.info(f"{len(combinations)} kombinacji dat (standard mode)")
            return combinations

        except Exception as e:
            self.logger.error(f"Blad dat standard: {e}")
            return []

    def generate_requests(self) -> List[ScrapingRequest]:
        """Generuje zapytania na podstawie config - obsługuje obie struktury"""
        cfg = self.config["scraping_config"]
        
        # Obsługa różnych struktur dat w config
        if "departure_start" in cfg and "departure_end" in cfg:
            # Nowa struktura GUI - użyj departure_start/end i return_start/end
            earliest_departure = cfg["departure_start"]
            latest_return = cfg["return_end"]
        else:
            # Stara struktura - użyj earliest_departure/latest_return
            earliest_departure = cfg.get("earliest_departure", "2025-10-20")
            latest_return = cfg.get("latest_return", "2025-11-15")

        # Generuj kombinacje dat
        date_combinations = self.generate_date_combinations_standard(
            earliest_departure, latest_return,
            cfg["min_days"], cfg["max_days"]
        )

        requests = []
        origin = cfg["origin"]
        destination = cfg["destination"]

        for dep_date, ret_date, duration in date_combinations:
            for airline_key in cfg["selected_airlines"]:
                if airline_key not in self.airlines:
                    self.logger.warning(f"Nieznana linia: {airline_key}")
                    continue

                airline_data = self.airlines[airline_key]

                request = ScrapingRequest(
                    departure_date=dep_date,
                    return_date=ret_date,
                    airline_key=airline_key,
                    airline_name=airline_data['name'],
                    airline_filter=airline_data['filter'],
                    passengers=cfg["passengers"],
                    duration_days=duration,
                    origin=origin,
                    destination=destination
                )
                requests.append(request)

        # Randomizuj kolejność
        random.shuffle(requests)

        self.logger.info(f"{len(requests)} zapytan dla trasy {origin}->{destination} (wszystkie kombinacje)")
        return requests

    def build_kayak_url(self, request: ScrapingRequest) -> str:
        """Buduje URL Kayak"""
        base_url = "https://www.kayak.pl/flights"
        route = f"{request.origin}-{request.destination}"
        dates = f"{request.departure_date}/{request.return_date}"
        passengers = f"{request.passengers}adults"

        url = f"{base_url}/{route}/{dates}/{passengers}?sort=price_a&{request.airline_filter}"
        return url

    def scrape_text_only(self, request: ScrapingRequest, round_number: int = None) -> TextResult:
        """GLOWNA FUNKCJA - tylko otworz i skopiuj tekst"""
        driver = None
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]

        # NOWY FORMAT NAZWY PLIKU: podobnie jak w kayak_excel_scraper
        # Zawiera teraz kody lotnisk na początku nazwy
        if round_number:
            base_name = f"R{round_number:03d}_{request.origin}_{request.destination}_{request.airline_key}_{request.departure_date}_{request.return_date}_{timestamp}"
        else:
            base_name = f"{request.origin}_{request.destination}_{request.airline_key}_{request.departure_date}_{request.return_date}_{timestamp}"

        try:
            self.logger.info(f"{request.airline_name} | {request.origin}->{request.destination} | {request.departure_date}->{request.return_date}")

            # Utworz driver
            driver = SimpleDriver.create_driver()
            driver.set_page_load_timeout(45)

            # URL
            url = self.build_kayak_url(request)

            # Krotkie opoznienie przed otwarciem
            delay = random.uniform(2, 5)
            time.sleep(delay)

            # Otworz strone
            self.logger.info(f"Otwieram strone...")
            driver.get(url)

            # DLUGIE CZEKANIE - 12s + losowy skladnik (3-8s)
            wait_time = 12 + random.uniform(3, 8)
            self.logger.info(f"Czekam {wait_time:.1f}s na zaladowanie...")
            time.sleep(wait_time)

            # Pobierz tytul
            page_title = driver.title

            # Pobierz CALY tekst ze strony
            self.logger.info(f"Kopiuje tekst...")
            body = driver.find_element(By.TAG_NAME, "body")
            page_text = body.text

            # Dodatkowe informacje na gorze (NOWY FORMAT jak w kayak_excel_scraper)
            full_text = f"""URL: {url}
Title: {page_title}
Timestamp: {timestamp}
Round: {round_number if round_number else "Single"}
Route: {request.origin} - {request.destination}
Flight: {request.airline_name} | {request.departure_date} - {request.return_date} | {request.passengers} pax
Duration: {request.duration_days} days
Airline Filter: {request.airline_filter}
{'='*80}

{page_text}
"""

            # Zapisz do pliku
            text_path = os.path.join(self.session_dir, f"{base_name}.txt")
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(full_text)

            text_length = len(page_text)
            self.logger.info(f"Zapisano: {text_length} znakow -> {os.path.basename(text_path)}")

            return TextResult(
                request=request,
                timestamp=timestamp,
                url=url,
                success=True,
                error_message=None,
                text_path=text_path,
                page_title=page_title,
                text_length=text_length
            )

        except Exception as e:
            self.logger.error(f"Blad: {str(e)}")

            return TextResult(
                request=request,
                timestamp=timestamp,
                url=url if 'url' in locals() else "N/A",
                success=False,
                error_message=str(e),
                text_path=None,
                page_title=None,
                text_length=0
            )

        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass

    def save_session_summary(self, requests: List[ScrapingRequest], results: List[TextResult]):
        """Zapisz podsumowanie sesji"""
        try:
            summary = {
                "session_timestamp": datetime.now().isoformat(),
                "config_used": self.config,
                "total_requests": len(requests),
                "successful": len([r for r in results if r.success]),
                "failed": len([r for r in results if not r.success]),
                "airlines": list(set([r.request.airline_key for r in results])),
                "route": f"{self.config['scraping_config']['origin']}->{self.config['scraping_config']['destination']}",
                "rolling_mode": self.config['scraping_config'].get('rolling_mode', False),
                "total_text_length": sum([r.text_length for r in results if r.success]),
                "results": [asdict(res) for res in results]
            }

            summary_path = os.path.join(self.session_dir, "session_summary.json")
            with open(summary_path, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)

            self.logger.info(f"Podsumowanie: {summary_path}")

        except Exception as e:
            self.logger.error(f"Blad zapisu podsumowania: {e}")

    def run_scraping_session(self):
        """Wykonuje kompletna sesje scrapingu na podstawie config"""

        cfg = self.config["scraping_config"]

        # Sprawdz czy rolling mode
        if cfg.get("rolling_mode", False):
            return self.run_rolling_mode()

        # Tryb standardowy - jedna sesja
        self.logger.info("" + "="*60)
        self.logger.info("KAYAK TEXT SCRAPER - SESJA ROZPOCZETA")
        self.logger.info(f"Trasa: {cfg['origin']} -> {cfg['destination']}")
        
        # Obsługa różnych struktur dat w config
        if "departure_start" in cfg and "departure_end" in cfg:
            self.logger.info(f"Zakres dat: {cfg['departure_start']} -> {cfg['return_end']}")
        else:
            self.logger.info(f"Zakres dat: {cfg['earliest_departure']} -> {cfg['latest_return']}")
            
        self.logger.info(f"Dlugosc pobytu: {cfg['min_days']}-{cfg['max_days']} dni")
        self.logger.info(f"Pasazerowie: {cfg['passengers']}")
        self.logger.info(f"Linie: {cfg['selected_airlines']}")
        self.logger.info(f"Tryb: Standard")
        self.logger.info(f"Dane: {self.session_dir}")
        self.logger.info("="*60)

        # Generuj zapytania
        requests = self.generate_requests()

        if not requests:
            self.logger.error("Brak zapytan do wykonania!")
            return

        results = []
        delay_range = cfg["delay_between_requests"]

        for i, request in enumerate(requests, 1):
            self.logger.info(f"\n[{i}/{len(requests)}] {request.airline_name} | {request.departure_date}->{request.return_date}")

            # Wykonaj zapytanie
            result = self.scrape_text_only(request)
            results.append(result)

            # Statystyki na biezaco
            successful = len([r for r in results if r.success])
            failed = len([r for r in results if not r.success])

            self.logger.info(f"Progress: {successful} sukces | {failed} bledow | {len(requests)-i} pozostalo")

            # Opoznienie miedzy zapytaniami (wazne!)
            if i < len(requests):
                delay = random.uniform(delay_range[0], delay_range[1])
                self.logger.info(f"Opoznienie: {delay:.1f}s")
                time.sleep(delay)

        # Zapisz podsumowanie sesji
        self.save_session_summary(requests, results)

        # Podsumowanie
        successful = len([r for r in results if r.success])
        failed = len([r for r in results if not r.success])
        total_chars = sum([r.text_length for r in results if r.success])

        self.logger.info("\n" + "="*60)
        self.logger.info("SESJA ZAKONCZONA!")
        self.logger.info(f"WYNIKI:")
        self.logger.info(f"   Sukces: {successful}")
        self.logger.info(f"   Bledy: {failed}")
        self.logger.info(f"   Skutecznosc: {(successful/len(results)*100):.1f}%")
        self.logger.info(f"   Zebranych znakow: {total_chars:,}")
        self.logger.info(f"Trasa: {cfg['origin']}->{cfg['destination']}")
        self.logger.info(f"Dane zapisane w: {self.session_dir}")
        self.logger.info("="*60)

        return results

    def run_rolling_mode(self):
        """Uruchamia rolling mode - dziala w kolko"""
        import signal

        self.stop_rolling = False

        # Handler dla Ctrl+C
        def signal_handler(signum, frame):
            self.logger.info("\nOtrzymano sygnal zatrzymania...")
            self.stop_rolling = True

        signal.signal(signal.SIGINT, signal_handler)

        cfg = self.config["scraping_config"]

        self.logger.info("" + "="*60)
        self.logger.info("KAYAK ROLLING MODE - URUCHOMIONY")
        self.logger.info(f"Trasa: {cfg['origin']} -> {cfg['destination']}")
        self.logger.info(f"Wszystkie pliki w: {self.session_dir}")
        self.logger.info(f"Zatrzymanie: Ctrl+C")
        self.logger.info("="*60)

        round_number = 1
        total_successful = 0
        total_failed = 0
        start_time = datetime.now()

        try:
            while not self.stop_rolling:
                self.logger.info(f"\nRUNDA {round_number} - {datetime.now().strftime('%H:%M:%S')}")

                # Wykonaj jedna runde scrapingu
                results = self.run_single_round(round_number)

                if results:
                    successful = len([r for r in results if r.success])
                    failed = len([r for r in results if not r.success])

                    total_successful += successful
                    total_failed += failed

                    self.logger.info(f"Runda {round_number}: {successful} sukces, {failed} bledow")
                    self.logger.info(f"RAZEM: {total_successful} sukces, {total_failed} bledow")
                else:
                    self.logger.error(f"Runda {round_number} nieudana")

                round_number += 1

                # Przerwa miedzy rundami (jesli nie zatrzymano)
                if not self.stop_rolling:
                    break_range = cfg.get("rolling_break_minutes", [30, 60])
                    break_minutes = random.uniform(break_range[0], break_range[1])

                    self.logger.info(f"Przerwa miedzy rundami: {break_minutes:.1f} minut")
                    self.logger.info(f"Nastepna runda okolo: {(datetime.now() + timedelta(minutes=break_minutes)).strftime('%H:%M:%S')}")

                    # Czekaj w malych kawalkach zeby moc przerwac
                    for _ in range(int(break_minutes * 60)):
                        if self.stop_rolling:
                            break
                        time.sleep(1)

            # Podsumowanie koncowe
            total_time = datetime.now() - start_time

            self.logger.info("\n" + "="*60)
            self.logger.info("ROLLING MODE ZAKONCZONY!")
            self.logger.info(f"STATYSTYKI KONCOWE:")
            self.logger.info(f"   Rundy: {round_number - 1}")
            self.logger.info(f"   Sukces: {total_successful}")
            self.logger.info(f"   Bledy: {total_failed}")
            self.logger.info(f"   Czas dzialania: {total_time}")
            self.logger.info(f"Wszystkie pliki w: {self.session_dir}")
            self.logger.info("="*60)

        except Exception as e:
            self.logger.error(f"Blad rolling mode: {e}")

    def run_single_round(self, round_number: int):
        """Wykonuje jedna runde scrapingu"""
        try:
            # Generuj zapytania
            requests = self.generate_requests()

            if not requests:
                self.logger.error("Brak zapytan do wykonania!")
                return None

            results = []
            delay_range = self.config["scraping_config"]["delay_between_requests"]

            for i, request in enumerate(requests, 1):
                if hasattr(self, 'stop_rolling') and self.stop_rolling:
                    self.logger.info("Zatrzymano podczas rundy")
                    break

                self.logger.info(f"R{round_number} [{i}/{len(requests)}] {request.airline_name} | {request.departure_date}->{request.return_date}")

                # Wykonaj zapytanie
                result = self.scrape_text_only(request, round_number)
                results.append(result)

                # Statystyki na biezaco (co 5 zapytan)
                if i % 5 == 0:
                    successful = len([r for r in results if r.success])
                    failed = len([r for r in results if not r.success])
                    self.logger.info(f"R{round_number} Progress: {successful} sukces | {failed} bledow | {len(requests)-i} pozostalo")

                # Opoznienie miedzy zapytaniami
                if i < len(requests) and not (hasattr(self, 'stop_rolling') and self.stop_rolling):
                    delay = random.uniform(delay_range[0], delay_range[1])
                    time.sleep(delay)

            # Zapisz podsumowanie rundy
            self.save_round_summary(round_number, requests, results)

            return results

        except Exception as e:
            self.logger.error(f"Blad rundy {round_number}: {e}")
            return None

    def save_round_summary(self, round_number: int, requests: List[ScrapingRequest], results: List[TextResult]):
        """Zapisuje podsumowanie pojedynczej rundy"""
        try:
            summary = {
                "round_number": round_number,
                "round_timestamp": datetime.now().isoformat(),
                "config_used": self.config,
                "total_requests": len(requests),
                "successful": len([r for r in results if r.success]),
                "failed": len([r for r in results if not r.success]),
                "airlines": list(set([r.request.airline_key for r in results])),
                "route": f"{self.config['scraping_config']['origin']}->{self.config['scraping_config']['destination']}",
                "total_text_length": sum([r.text_length for r in results if r.success]),
                "results": [asdict(res) for res in results]
            }

            summary_path = os.path.join(self.session_dir, f"round_{round_number:03d}_summary.json")
            with open(summary_path, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)

            self.logger.info(f"Podsumowanie rundy {round_number}: {summary_path}")

        except Exception as e:
            self.logger.error(f"Blad zapisu podsumowania rundy {round_number}: {e}")

def main():
    """Glowna funkcja"""
    print("Kayak Simple Text Scraper")
    print("="*50)

    try:
        # Test ChromeDriver
        print("Test ChromeDriver...")
        driver = SimpleDriver.create_driver()
        driver.get("about:blank")
        driver.quit()
        print("ChromeDriver dziala!")

        # Uruchom scraper
        scraper = KayakTextScraper()
        results = scraper.run_scraping_session()

        print(f"\nSesja zakonczona! Sprawdz folder: {scraper.session_dir}")

    except KeyboardInterrupt:
        print("\nPrzerwano przez uzytkownika")
    except Exception as e:
        print(f"Blad krytyczny: {e}")

if __name__ == "__main__":
    main()