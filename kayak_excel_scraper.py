#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kayak Excel Scraper - LISTA LOTOW Z EXCEL
Wczytuje liste konkretnych lotow z pliku Excel i sprawdza tylko te loty
"""

import time
import random
import os
import json
import pandas as pd
import sys
import signal
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Optional
import logging

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

@dataclass
class FlightTarget:
    """Konkretny lot do sprawdzenia"""
    origin_airport: str
    destination_airport: str
    airline_key: str
    departure_date: str
    return_date: str
    duration_days: int = None
    
    def __post_init__(self):
        if self.duration_days is None:
            dep = datetime.strptime(self.departure_date, "%Y-%m-%d")
            ret = datetime.strptime(self.return_date, "%Y-%m-%d")
            self.duration_days = (ret - dep).days

@dataclass
class ScrapingRequest:
    """Struktura zapytania"""
    target: FlightTarget
    airline_name: str
    airline_filter: str
    passengers: int

@dataclass 
class TextResult:
    """Struktura wyniku"""
    request: ScrapingRequest
    timestamp: str
    url: str
    success: bool
    error_message: Optional[str]
    text_path: Optional[str]
    page_title: Optional[str]
    text_length: int

class SimpleDriver:
    """Prosta klasa driver"""
    
    @staticmethod
    def create_driver():
        """Podstawowy ChromeDriver"""
        options = Options()
        
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        
        # Losowy User Agent
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        
        options.add_argument(f"--user-agent={random.choice(user_agents)}")
        
        return webdriver.Chrome(options=options)

class KayakExcelScraper:
    """Scraper dla listy lotow z Excel"""
    
    def __init__(self, flights_file: str = "flights_list.xlsx", config_file: str = "excel_config.json", 
                 output_dir: str = "kayak_excel_data", rolling_mode: bool = False):
        self.flights_file = flights_file
        self.config_file = config_file
        self.output_dir = output_dir
        self.rolling_mode = rolling_mode
        self.session_dir = None
        self.logger = self._setup_logger()
        self.stop_rolling = False
        
        # Handler dla Ctrl+C w trybie rolling
        if self.rolling_mode:
            signal.signal(signal.SIGINT, self._signal_handler)
        
        # Wczytaj konfiguracje
        self.config = self._load_config()
        self.airlines = self.config["airlines"]
        
        if self.rolling_mode:
            self._create_rolling_folder()
        else:
            self._create_session_folder()
    
    def _load_config(self) -> dict:
        """Wczytuje konfiguracje"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            self.logger.info(f"Config: {self.config_file}")
            return config
        except FileNotFoundError:
            self.logger.error(f"Brak config: {self.config_file}")
            self._create_default_config()
            raise
        except Exception as e:
            self.logger.error(f"Blad config: {e}")
            raise
    
    def _create_default_config(self):
        """Tworzy domyslny config"""
        default_config = {
            "_comment": "Konfiguracja dla Excel Scrapera",
            "_comment_passengers": "Liczba pasazerow (1-4)",
            "_comment_delays": "Opoznienia miedzy zapytaniami w sekundach [min, max]",
            "_comment_rolling": "rolling_break_minutes - przerwa miedzy rundami w trybie rolling (minuty)",
            "_comment_excel_file": "Plik Excel powinien miec kolumny: 'Lotnisko wylotu', 'Lotnisko docelowe', 'Filtr linii', 'Data wylotu', 'Data powrotu'",
            "_comment_excel_example": "Przyklad: WAW | ICN | Turkish | 2025-10-22 | 2025-11-10",
            
            "scraping_config": {
                "passengers": 2,
                "delay_between_requests": [20, 35],
                "randomize_order": True,
                "rolling_break_minutes": [30, 60]
            },
            
            "_comment_airlines": "Mapowanie nazw linii na filtry Kayak",
            "airlines": {
                "LOT": {"filter": "fs=airlines%3DLO%3Bbfc%3D1", "name": "LOT Polish Airlines"},
                "Lufthansa": {"filter": "fs=airlines%3DLH%2CMULT%3Bbfc%3D1", "name": "Lufthansa + Multi"},
                "KLM": {"filter": "fs=airlines%3DKL%2CMULT%3Bbfc%3D1", "name": "KLM + Multi"},
                "AirFrance": {"filter": "fs=airlines%3DAF%2CMULT%3Bbfc%3D1", "name": "Air France + Multi"},
                "Swiss": {"filter": "fs=airlines%3DLX%3Bbfc%3D1", "name": "Swiss"},
                "Austrian": {"filter": "fs=airlines%3DOS%3Bbfc%3D1", "name": "Austrian Airlines"},
                "Finnair": {"filter": "fs=airlines%3DAY%3Bbfc%3D1", "name": "Finnair"},
                "SAS": {"filter": "fs=airlines%3DSK%3Bbfc%3D1", "name": "SAS"},
                "Korean": {"filter": "fs=airlines%3DKE%3Bbfc%3D1", "name": "Korean Air"},
                "Asiana": {"filter": "fs=airlines%3DOZ%3Bbfc%3D1", "name": "Asiana Airlines"},
                "China Air": {"filter": "fs=airlines%3DCA%3Bbfc%3D1", "name": "Air China"},
                "China_Air": {"filter": "fs=airlines%3DCA%3Bbfc%3D1", "name": "Air China"},
                "Turkish": {"filter": "fs=airlines%3DTK%2CMULT%3Bbfc%3D1", "name": "Turkish Airlines + Multi"},
                "Emirates": {"filter": "fs=airlines%3DEK%3Bbfc%3D1", "name": "Emirates"},
                "Qatar": {"filter": "fs=airlines%3DQR%3Bbfc%3D1", "name": "Qatar Airways"},
                "Etihad": {"filter": "fs=airlines%3DEY%3Bbfc%3D1", "name": "Etihad Airways"}
            }
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)
        
        print(f"Utworzono config: {self.config_file}")
    
    def _setup_logger(self):
        """Logger"""
        logger = logging.getLogger('KayakExcelScraper')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _signal_handler(self, signum, frame):
        """Handler dla Ctrl+C w rolling mode"""
        self.logger.info("\nOtrzymano sygnal zatrzymania...")
        self.stop_rolling = True
    
    def _create_rolling_folder(self):
        """Tworzy folder dla rolling mode - wszystko w jednym katalogu"""
        rolling_folder = os.path.join(self.output_dir, "rolling_mode")
        os.makedirs(rolling_folder, exist_ok=True)
        self.session_dir = rolling_folder
        
        self.logger.info(f"Rolling mode - wszystkie pliki w: {self.session_dir}")
    
    def _create_session_folder(self):
        """Folder sesji"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_dir = os.path.join(self.output_dir, f"excel_session_{timestamp}")
        os.makedirs(self.session_dir, exist_ok=True)
        
        self.logger.info(f"Sesja: {self.session_dir}")
    
    def _create_sample_excel(self):
        """Tworzy przykladowy plik Excel"""
        sample_data = [
            {"Lotnisko wylotu": "WAW", "Lotnisko docelowe": "ICN", "Filtr linii": "Turkish", "Data wylotu": "2025-10-22", "Data powrotu": "2025-11-10"},
            {"Lotnisko wylotu": "WAW", "Lotnisko docelowe": "ICN", "Filtr linii": "China Air", "Data wylotu": "2025-10-17", "Data powrotu": "2025-11-09"},
            {"Lotnisko wylotu": "WAW", "Lotnisko docelowe": "ICN", "Filtr linii": "Qatar", "Data wylotu": "2025-10-21", "Data powrotu": "2025-11-12"},
            {"Lotnisko wylotu": "WAW", "Lotnisko docelowe": "ICN", "Filtr linii": "Emirates", "Data wylotu": "2025-10-05", "Data powrotu": "2025-10-24"},
            {"Lotnisko wylotu": "WAW", "Lotnisko docelowe": "ICN", "Filtr linii": "LOT", "Data wylotu": "2025-10-23", "Data powrotu": "2025-11-12"},
        ]
        
        df = pd.DataFrame(sample_data)
        df.to_excel(self.flights_file, index=False)
        
        print(f"Utworzono przykladowy Excel: {self.flights_file}")
        print("Edytuj plik i uruchom ponownie")
    
    def load_flights_from_excel(self) -> List[FlightTarget]:
        """Wczytuje loty z pliku Excel"""
        try:
            # Sprawdz czy plik istnieje
            if not os.path.exists(self.flights_file):
                self.logger.error(f"Brak pliku: {self.flights_file}")
                self._create_sample_excel()
                raise FileNotFoundError(f"Utworzono przykladowy plik {self.flights_file}")
            
            # Wczytaj Excel
            df = pd.read_excel(self.flights_file)
            self.logger.info(f"Wczytano Excel: {len(df)} wierszy")
            
            # Sprawdz kolumny
            required_columns = ['Lotnisko wylotu', 'Lotnisko docelowe', 'Filtr linii', 'Data wylotu', 'Data powrotu']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                self.logger.error(f"Brakujace kolumny: {missing_columns}")
                self.logger.error(f"Wymagane kolumny: {required_columns}")
                raise ValueError(f"Brakujace kolumny w Excel: {missing_columns}")
            
            # Konwertuj na FlightTarget
            flights = []
            
            for index, row in df.iterrows():
                try:
                    # Wyczysc dane
                    origin = str(row['Lotnisko wylotu']).strip().upper()
                    destination = str(row['Lotnisko docelowe']).strip().upper()
                    airline_key = str(row['Filtr linii']).strip()
                    
                    # Sprawdz czy dane sa kompletne
                    if pd.isna(row['Data wylotu']) or pd.isna(row['Data powrotu']) or pd.isna(row['Lotnisko wylotu']) or pd.isna(row['Lotnisko docelowe']):
                        self.logger.warning(f"Wiersz {index+2}: Puste pola, pomijam")
                        continue
                    
                    # Walidacja kodow lotnisk (3 znaki)
                    if len(origin) != 3 or len(destination) != 3:
                        self.logger.warning(f"Wiersz {index+2}: Nieprawidlowe kody lotnisk '{origin}'-'{destination}', pomijam")
                        continue
                    
                    # Konwertuj daty
                    # Obsluga roznych formatow dat
                    if isinstance(row['Data wylotu'], str):
                        dep_date = row['Data wylotu']
                    else:
                        dep_date = row['Data wylotu'].strftime('%Y-%m-%d')
                    
                    if isinstance(row['Data powrotu'], str):
                        ret_date = row['Data powrotu']
                    else:
                        ret_date = row['Data powrotu'].strftime('%Y-%m-%d')
                    
                    # Sprawdz czy linia istnieje w config
                    if airline_key not in self.airlines:
                        self.logger.warning(f"Wiersz {index+2}: Nieznana linia '{airline_key}', pomijam")
                        continue
                    
                    flight = FlightTarget(
                        origin_airport=origin,
                        destination_airport=destination,
                        airline_key=airline_key,
                        departure_date=dep_date,
                        return_date=ret_date
                    )
                    
                    flights.append(flight)
                    self.logger.debug(f"Lot: {origin}-{destination} {airline_key} {dep_date}-{ret_date} ({flight.duration_days} dni)")
                    
                except Exception as e:
                    self.logger.warning(f"Blad wiersza {index+2}: {e}")
                    continue
            
            self.logger.info(f"Zaladowano {len(flights)} lotow z Excel")
            
            # Pokaz statystyki
            airline_counts = {}
            route_counts = {}
            for flight in flights:
                # Statystyki linii
                airline_counts[flight.airline_key] = airline_counts.get(flight.airline_key, 0) + 1
                # Statystyki tras
                route = f"{flight.origin_airport}-{flight.destination_airport}"
                route_counts[route] = route_counts.get(route, 0) + 1
            
            self.logger.info("Linie w pliku:")
            for airline, count in sorted(airline_counts.items()):
                self.logger.info(f"   {airline}: {count} lotow")
            
            self.logger.info("Trasy w pliku:")
            for route, count in sorted(route_counts.items()):
                self.logger.info(f"   {route}: {count} lotow")
            
            return flights
            
        except Exception as e:
            self.logger.error(f"Blad wczytywania Excel: {e}")
            raise
    
    def generate_requests(self, flights: List[FlightTarget]) -> List[ScrapingRequest]:
        """Generuje zapytania na podstawie listy lotow"""
        requests = []
        passengers = self.config["scraping_config"]["passengers"]
        
        for flight in flights:
            if flight.airline_key not in self.airlines:
                self.logger.warning(f"Pomijam nieznana linie: {flight.airline_key}")
                continue
            
            airline_data = self.airlines[flight.airline_key]
            
            request = ScrapingRequest(
                target=flight,
                airline_name=airline_data['name'],
                airline_filter=airline_data['filter'],
                passengers=passengers
            )
            requests.append(request)
        
        # Randomizacja kolejnosci (jesli wlaczona)
        if self.config["scraping_config"].get("randomize_order", True):
            random.shuffle(requests)
            self.logger.info("Losowa kolejnosc zapytan")
        
        self.logger.info(f"{len(requests)} zapytan do wykonania")
        return requests
    
    def scrape_text_only(self, request: ScrapingRequest, round_number: int = None) -> TextResult:
        """Glowna funkcja scrapingu"""
        driver = None
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        
        # Nazwa pliku z kodami lotnisk + linia + daty + timestamp
        if round_number:
            base_name = f"R{round_number:03d}_{request.target.origin_airport}_{request.target.destination_airport}_{request.target.airline_key}_{request.target.departure_date}_{request.target.return_date}_{timestamp}"
        else:
            base_name = f"{request.target.origin_airport}_{request.target.destination_airport}_{request.target.airline_key}_{request.target.departure_date}_{request.target.return_date}_{timestamp}"
        
        try:
            self.logger.info(f"{request.airline_name} | {request.target.origin_airport}-{request.target.destination_airport} | {request.target.departure_date}-{request.target.return_date} ({request.target.duration_days}d)")
            
            # Utworz driver
            driver = SimpleDriver.create_driver()
            driver.set_page_load_timeout(45)
            
            # URL - DYNAMICZNY na podstawie lotnisk z Excel
            url = f"https://www.kayak.pl/flights/{request.target.origin_airport}-{request.target.destination_airport}/{request.target.departure_date}/{request.target.return_date}/{request.passengers}adults?sort=price_a&{request.airline_filter}"
            
            # Krotkie opoznienie
            delay = random.uniform(2, 5)
            time.sleep(delay)
            
            # Otworz strone
            self.logger.info(f"Otwieram strone...")
            driver.get(url)
            
            # DLUGIE CZEKANIE - 12s + losowy skladnik
            wait_time = 12 + random.uniform(3, 8)
            self.logger.info(f"Czekam {wait_time:.1f}s...")
            time.sleep(wait_time)
            
            # Pobierz dane
            page_title = driver.title
            body = driver.find_element(By.TAG_NAME, "body")
            page_text = body.text
            
            # Przygotuj pelny tekst
            full_text = f"""URL: {url}
Title: {page_title}
Timestamp: {timestamp}
Round: {round_number if round_number else "Single"}
Route: {request.target.origin_airport} - {request.target.destination_airport}
Flight: {request.airline_name} | {request.target.departure_date} - {request.target.return_date} | {request.passengers} pax
Duration: {request.target.duration_days} days
Airline Filter: {request.airline_filter}
{'='*80}

{page_text}
"""
            
            # Zapisz do pliku
            text_path = os.path.join(self.session_dir, f"{base_name}.txt")
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(full_text)
            
            text_length = len(page_text)
            self.logger.info(f"Zapisano: {text_length} znakow - {os.path.basename(text_path)}")
            
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
    
    def save_session_summary(self, flights: List[FlightTarget], requests: List[ScrapingRequest], results: List[TextResult]):
        """Zapisz podsumowanie sesji"""
        try:
            summary = {
                "session_timestamp": datetime.now().isoformat(),
                "flights_file": self.flights_file,
                "config_used": self.config,
                "total_flights_in_excel": len(flights),
                "total_requests": len(requests),
                "successful": len([r for r in results if r.success]),
                "failed": len([r for r in results if not r.success]),
                "airlines_processed": list(set([r.request.target.airline_key for r in results])),
                "total_text_length": sum([r.text_length for r in results if r.success]),
                "results": [asdict(res) for res in results]
            }
            
            summary_path = os.path.join(self.session_dir, "session_summary.json")
            with open(summary_path, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Podsumowanie: {summary_path}")
            
        except Exception as e:
            self.logger.error(f"Blad zapisu podsumowania: {e}")
    
    def save_round_summary(self, round_number: int, flights: List[FlightTarget], requests: List[ScrapingRequest], results: List[TextResult]):
        """Zapisz podsumowanie rundy"""
        try:
            summary = {
                "round_number": round_number,
                "round_timestamp": datetime.now().isoformat(),
                "flights_file": self.flights_file,
                "total_flights_in_excel": len(flights),
                "total_requests": len(requests),
                "successful": len([r for r in results if r.success]),
                "failed": len([r for r in results if not r.success]),
                "airlines_processed": list(set([r.request.target.airline_key for r in results])),
                "total_text_length": sum([r.text_length for r in results if r.success]),
                "results": [asdict(res) for res in results]
            }
            
            summary_path = os.path.join(self.session_dir, f"round_{round_number:03d}_summary.json")
            with open(summary_path, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Podsumowanie rundy: {summary_path}")
            
        except Exception as e:
            self.logger.error(f"Blad zapisu podsumowania rundy: {e}")
    
    def run_scraping_session(self):
        """Wykonuje sesje scrapingu na podstawie Excel"""
        
        self.logger.info("="*60)
        self.logger.info("KAYAK EXCEL SCRAPER - SESJA ROZPOCZETA")
        self.logger.info(f"Plik lotow: {self.flights_file}")
        self.logger.info(f"Pasazerowie: {self.config['scraping_config']['passengers']}")
        self.logger.info(f"Dane: {self.session_dir}")
        self.logger.info("="*60)
        
        try:
            # Wczytaj loty z Excel
            flights = self.load_flights_from_excel()
            
            if not flights:
                self.logger.error("Brak lotow do sprawdzenia!")
                return
            
            # Generuj zapytania
            requests = self.generate_requests(flights)
            
            if not requests:
                self.logger.error("Brak zapytan do wykonania!")
                return
            
            results = []
            delay_range = self.config["scraping_config"]["delay_between_requests"]
            
            for i, request in enumerate(requests, 1):
                self.logger.info(f"\n[{i}/{len(requests)}] {request.target.origin_airport}-{request.target.destination_airport} | {request.airline_name} | {request.target.departure_date}-{request.target.return_date}")
                
                # Wykonaj zapytanie
                result = self.scrape_text_only(request)
                results.append(result)
                
                # Statystyki na biezaco
                successful = len([r for r in results if r.success])
                failed = len([r for r in results if not r.success])
                
                self.logger.info(f"Progress: {successful} sukces | {failed} bledy | {len(requests)-i} pozostalo")
                
                # Opoznienie miedzy zapytaniami
                if i < len(requests):
                    delay = random.uniform(delay_range[0], delay_range[1])
                    self.logger.info(f"Opoznienie: {delay:.1f}s")
                    time.sleep(delay)
            
            # Zapisz podsumowanie
            self.save_session_summary(flights, requests, results)
            
            # Podsumowanie koncowe
            successful = len([r for r in results if r.success])
            failed = len([r for r in results if not r.success])
            total_chars = sum([r.text_length for r in results if r.success])
            
            self.logger.info("\n" + "="*60)
            self.logger.info("SESJA ZAKONCZONA!")
            self.logger.info(f"WYNIKI:")
            self.logger.info(f"   Loty w Excel: {len(flights)}")
            self.logger.info(f"   Zapytania: {len(requests)}")
            self.logger.info(f"   Sukces: {successful}")
            self.logger.info(f"   Bledy: {failed}")
            self.logger.info(f"   Skutecznosc: {(successful/len(results)*100):.1f}%")
            self.logger.info(f"   Zebranych znakow: {total_chars:,}")
            self.logger.info(f"Dane: {self.session_dir}")
            self.logger.info("="*60)
            
            return results
            
        except Exception as e:
            self.logger.error(f"Blad sesji: {e}")
            return None
    
    def run_rolling_mode(self):
        """Uruchamia rolling mode - dziala w kolko"""
        
        self.logger.info("="*60)
        self.logger.info("KAYAK ROLLING MODE - URUCHOMIONY")
        self.logger.info(f"Plik lotow: {self.flights_file}")
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
                    break_range = self.config["scraping_config"].get("rolling_break_minutes", [30, 60])
                    break_minutes = random.uniform(break_range[0], break_range[1])
                    
                    self.logger.info(f"Przerwa miedzy rundami: {break_minutes:.1f} minut")
                    self.logger.info(f"Nastepna runda okolo: {(datetime.now() + timedelta(minutes=break_minutes)).strftime('%H:%M:%S')}")
                    
                    # Czekaj w malych kawalach zeby moc przerwac
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
            # Wczytaj loty z Excel
            flights = self.load_flights_from_excel()
            
            if not flights:
                self.logger.error("Brak lotow do sprawdzenia!")
                return None
            
            # Generuj zapytania
            requests = self.generate_requests(flights)
            
            if not requests:
                self.logger.error("Brak zapytan do wykonania!")
                return None
            
            results = []
            delay_range = self.config["scraping_config"]["delay_between_requests"]
            
            for i, request in enumerate(requests, 1):
                if self.stop_rolling:
                    self.logger.info("Zatrzymano podczas rundy")
                    break
                
                self.logger.info(f"R{round_number} [{i}/{len(requests)}] {request.target.origin_airport}-{request.target.destination_airport} | {request.airline_name}")
                
                # Wykonaj zapytanie
                result = self.scrape_text_only(request, round_number)
                results.append(result)
                
                # Statystyki na biezaco (co 10 zapytan)
                if i % 10 == 0:
                    successful = len([r for r in results if r.success])
                    failed = len([r for r in results if not r.success])
                    self.logger.info(f"R{round_number} Progress: {successful} sukces | {failed} bledy | {len(requests)-i} pozostalo")
                
                # Opoznienie miedzy zapytaniami
                if i < len(requests) and not self.stop_rolling:
                    delay = random.uniform(delay_range[0], delay_range[1])
                    time.sleep(delay)
            
            # Zapisz podsumowanie rundy
            self.save_round_summary(round_number, flights, requests, results)
            
            return results
            
        except Exception as e:
            self.logger.error(f"Blad rundy {round_number}: {e}")
            return None

def main():
    """Glowna funkcja"""
    print("Kayak Excel Scraper")
    print("="*50)
    
    try:
        # Test ChromeDriver
        print("Test ChromeDriver...")
        driver = SimpleDriver.create_driver()
        driver.get("about:blank")
        driver.quit()
        print("ChromeDriver dziala!")
        
        # Uruchom scraper
        scraper = KayakExcelScraper()
        results = scraper.run_scraping_session()
        
        if results:
            print(f"\nSesja zakonczona! Sprawdz folder: {scraper.session_dir}")
        
    except KeyboardInterrupt:
        print("\nPrzerwano przez uzytkownika")
    except Exception as e:
        print(f"Blad krytyczny: {e}")

if __name__ == "__main__":
    main()