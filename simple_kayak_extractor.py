#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Kayak Data Extractor
Wyciaga pierwsza (najtansza) oferte z kazdego pliku .txt i zapisuje do Excel
"""

import os
import re
import pandas as pd
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List
import sys

# Fix dla Windows - ustaw kodowanie UTF-8 dla stdout
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

@dataclass
class SimpleOffer:
    """Rozszerzona struktura oferty z detalami przesiadek"""
    filename: str
    airline_filter: str
    departure_date: str
    return_date: str
    total_price: float
    price_per_person: float
    
    # Loty
    airlines_outbound: str
    airlines_return: str
    
    # Lotniska
    departure_airport: str  # Lotnisko wylotu (WAW)
    destination_airport: str  # Lotnisko docelowe (ICN)
    
    # Czasy lotow
    departure_time: str
    arrival_time: str
    return_departure_time: str
    return_arrival_time: str
    
    # Czasy podrozy i lotow
    total_travel_time_outbound: str  # Calkowity czas podrozy tam
    total_travel_time_return: str    # Calkowity czas podrozy powrot
    actual_flight_time_outbound: str # Czas lotu bez przesiadek tam
    actual_flight_time_return: str   # Czas lotu bez przesiadek powrot
    
    # Przesiadki tam (max 3)
    stops_outbound: int
    stop1_outbound_airport: str
    stop1_outbound_duration: str
    stop2_outbound_airport: str
    stop2_outbound_duration: str
    stop3_outbound_airport: str
    stop3_outbound_duration: str
    
    # Przesiadki powrot (max 3)
    stops_return: int
    stop1_return_airport: str
    stop1_return_duration: str
    stop2_return_airport: str
    stop2_return_duration: str
    stop3_return_airport: str
    stop3_return_duration: str

class SimpleKayakExtractor:
    def __init__(self):
        pass
    
    def parse_filename(self, filename: str) -> dict:
        """Parsuje nazwe pliku dla pewnych danych - obsługuje standard i rolling mode"""
        
        # Standard mode: WAW_ICN_Turkish_2025-10-22_2025-11-10_20250623_143022_123.txt
        standard_pattern = r'([A-Z]{3})_([A-Z]{3})_([A-Za-z_]+)_(\d{4}-\d{2}-\d{2})_(\d{4}-\d{2}-\d{2})_(\d{8})_(\d{6})_(\d+)\.txt'
        
        # Rolling mode: R001_WAW_ICN_Turkish_2025-10-22_2025-11-10_20250623_143022_123.txt
        rolling_pattern = r'R\d+_([A-Z]{3})_([A-Z]{3})_([A-Za-z_]+)_(\d{4}-\d{2}-\d{2})_(\d{4}-\d{2}-\d{2})_(\d{8})_(\d{6})_(\d+)\.txt'
        
        # Spróbuj wzorzec rolling mode
        match = re.match(rolling_pattern, filename)
        mode = "rolling"
        
        if not match:
            # Spróbuj wzorzec standard mode
            match = re.match(standard_pattern, filename)
            mode = "standard"
        
        if match:
            if mode == "rolling":
                # Rolling mode: R001_WAW_ICN_Turkish_...
                departure_airport = match.group(1)  # WAW
                destination_airport = match.group(2)  # ICN
                airline_name = match.group(3).replace('_', ' ')  # Turkish
                departure_date = match.group(4)  # 2025-10-22
                return_date = match.group(5)  # 2025-11-10
                session_date = match.group(6)  # 20250623
                session_time = match.group(7)  # 143022
                sequence = match.group(8)  # 123
            else:
                # Standard mode: WAW_ICN_Turkish_...
                departure_airport = match.group(1)  # WAW
                destination_airport = match.group(2)  # ICN
                airline_name = match.group(3).replace('_', ' ')  # Turkish
                departure_date = match.group(4)  # 2025-10-22
                return_date = match.group(5)  # 2025-11-10
                session_date = match.group(6)  # 20250623
                session_time = match.group(7)  # 143022
                sequence = match.group(8)  # 123
            
            print(f"Parsowanie ({mode}): {departure_airport} -> {destination_airport}, {airline_name}")
            
            return {
                'airline_filter': airline_name,
                'departure_date': departure_date,
                'return_date': return_date,
                'session_date': session_date,
                'session_time': session_time,
                'sequence': sequence,
                'departure_airport': departure_airport,
                'destination_airport': destination_airport,
                'mode': mode
            }
        
        print(f"Nie rozpoznano formatu nazwy pliku: {filename}")
        return {
            'airline_filter': 'UNKNOWN', 
            'departure_date': '', 
            'return_date': '',
            'session_date': '',
            'session_time': '',
            'sequence': '',
            'departure_airport': 'WAW',  # domyślne
            'destination_airport': 'ICN',  # domyślne
            'mode': 'unknown'
        }

    def parse_airports(self, text: str, departure_from_filename: str = "", destination_from_filename: str = "") -> tuple:
        """Wyciaga lotniska wylotu i docelowe - priorytet ma nazwa pliku"""
        
        # Jeśli mamy kody z nazwy pliku, użyj ich
        if departure_from_filename and destination_from_filename:
            print(f"Lotniska z nazwy pliku: {departure_from_filename} -> {destination_from_filename}")
            return departure_from_filename, destination_from_filename
        
        # Fallback - szukaj w tekście (stara logika)
        departure_airport = "WAW"  # Domyślnie WAW (Warszawa)
        destination_airport = "ICN"  # Domyślnie ICN (Inczhon)
        
        # Sprawdz kierunek lotu w tekście
        if "WAW" in text and "ICN" in text:
            waw_pos = text.find("WAW")
            icn_pos = text.find("ICN")
            
            # Pierwszy wystepujacy to prawdopodobnie wylot
            if waw_pos < icn_pos:
                departure_airport = "WAW"
                destination_airport = "ICN"
            else:
                departure_airport = "ICN" 
                destination_airport = "WAW"
        
        print(f"Lotniska z tekstu (fallback): {departure_airport} -> {destination_airport}")
        return departure_airport, destination_airport
    
    def extract_first_offer_simple(self, content: str) -> Optional[dict]:
        """Wyciaga pierwsza oferte z tekstu Kayak"""
        try:
            # Poprawione wzorce cen dla formatu z pliku
            price_patterns = [
                r'(\d+(?:\s+\d{3})*)\s*zł\s*/\s*osoba\s+(\d+(?:\s+\d{3})*)\s*zł\s*łącznie',  # Oryginalny
                r'(\d+(?:\s+\d{3})*)\s*zł\s*/\s*osoba.*?(\d+(?:\s+\d{3})*)\s*zł\s*łącznie',  # Z dowolnym tekstem między
                r'(\d+(?:\s+\d{3})*)\s*zł.*?osoba.*?(\d+(?:\s+\d{3})*)\s*zł.*?łącznie',  # Bardzo elastyczny
            ]
            
            price_match = None
            pattern_used = ""
            
            for i, pattern in enumerate(price_patterns):
                price_match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
                if price_match:
                    pattern_used = f"Pattern {i+1}"
                    print(f"Znaleziono ceny uzywajac {pattern_used}")
                    break
            
            if not price_match:
                print(f"DEBUG: Nie znaleziono standardowych wzorcow, sprawdzam zawartosc...")
                
                # Znajdz wszystkie wystapienia z "zl"
                zl_pattern = r'(\d+(?:\s+\d{3})*)\s*zl'
                zl_matches = list(re.finditer(zl_pattern, content))
                
                if zl_matches:
                    print(f"Znaleziono {len(zl_matches)} cen w zl:")
                    for j, match in enumerate(zl_matches[:8]):  # Pokaz pierwsze 8
                        price_value = match.group(1).replace(' ', '')
                        context_start = max(0, match.start() - 30)
                        context_end = min(len(content), match.end() + 30)
                        context = content[context_start:context_end].replace('\n', ' ').replace('\r', ' ')
                        print(f"    {j+1}. {price_value} zl - ...{context}...")
                    
                    # Sprobuj znalezc pare cen (na osobe + lacznie)
                    prices = []
                    for match in zl_matches:
                        price_str = match.group(1).replace(' ', '')
                        try:
                            price_val = int(price_str)
                            if 1000 <= price_val <= 50000:  # Rozsadny zakres cen
                                prices.append((price_val, match.start(), match.end()))
                        except:
                            continue
                    
                    print(f"Ceny w rozsadnym zakresie: {[p[0] for p in prices]}")
                    
                    # Jesli mamy dokladnie 2 ceny, sprawdz czy jedna to polowa drugiej
                    if len(prices) >= 2:
                        for i in range(len(prices)-1):
                            price1, pos1, end1 = prices[i]
                            price2, pos2, end2 = prices[i+1]
                            
                            # Sprawdz czy jedna cena to okolo polowa drugiej (na osobe vs lacznie)
                            if abs(price2 - price1 * 2) < 100:  # Tolerancja 100 zl
                                print(f"Znaleziono pare cen: {price1} i {price2} (2 osoby)")
                                per_person = float(price1)
                                total = float(price2)
                                
                                # Znajdz tekst oferty
                                offer_start = max(0, pos1 - 1000)  # 1000 znakow przed pierwsza cena
                                offer_end = end2
                                offer_text = content[offer_start:offer_end]
                                
                                return offer_text, per_person, total
                
                print(f"Nie znaleziono odpowiednich cen")
                return None
            
            # Standardowe parsowanie gdy znaleziono wzorzec
            per_person_str = price_match.group(1).replace(' ', '')
            total_str = price_match.group(2).replace(' ', '')
            
            per_person = float(per_person_str)
            total = float(total_str)
            
            print(f"Ceny: {per_person} PLN/os -> {total} PLN lacznie ({pattern_used})")
            
            # Znajdz tekst oferty
            price_pos = price_match.start()
            offer_start = max(0, price_pos - 1000)
            offer_text = content[offer_start:price_match.end()]
            
            return offer_text, per_person, total
            
        except Exception as e:
            print(f"Blad parsowania: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def parse_offer_from_text(self, offer_text: str, per_person: float, total: float, file_info: dict) -> dict:
        """Parsuje szczegolowe dane oferty z tekstu - używa danych z nazwy pliku"""
        try:
            print(f"Parsowanie oferty ({len(offer_text)} znakow)")
            print(f"Linia z nazwy pliku: {file_info['airline_filter']}")
            print(f"Trasa z nazwy pliku: {file_info['departure_airport']} -> {file_info['destination_airport']}")
            
            # Uzyj nazwy linii z pliku jako glownej
            airlines_outbound = file_info['airline_filter']
            airlines_return = file_info['airline_filter']
            
            # Uzyj lotnisk z nazwy pliku (priorytet)
            departure_airport = file_info['departure_airport']
            destination_airport = file_info['destination_airport']
            
            # Znajdz czasy lotow
            time_matches = re.findall(r'(\d{2}:\d{2})\s*[–-]\s*(\d{2}:\d{2}(?:\+\d)?)', offer_text)
            
            dep_time = arr_time = ret_dep_time = ret_arr_time = ""
            if len(time_matches) >= 1:
                dep_time, arr_time = time_matches[0]
                print(f"Lot tam: {dep_time} -> {arr_time}")
            if len(time_matches) >= 2:
                ret_dep_time, ret_arr_time = time_matches[1]
                print(f"Lot powrot: {ret_dep_time} -> {ret_arr_time}")
            
            # Znajdz czasy podrozy (najdluzsze czasy w sekcjach)
            duration_matches = re.findall(r'(\d+\s*h\s*\d+\s*min)', offer_text)
            total_travel_outbound = duration_matches[0] if len(duration_matches) >= 1 else ""
            total_travel_return = duration_matches[1] if len(duration_matches) >= 2 else ""
            
            print(f"Czasy podrozy: tam {total_travel_outbound}, powrot {total_travel_return}")
            
            # Podziel tekst na sekcje (tam i powrot) - uzywamy nowej funkcji
            outbound_section, return_section = self.split_offer_sections(offer_text)
            
            # DEBUG: Pokaz fragmenty sekcji
            print(f"Sekcja TAM: {outbound_section[:100]}...")
            print(f"Sekcja POWROT: {return_section[:100]}...")
            
            # Parsuj przesiadki dla lotu tam
            outbound_stops = self.parse_stopovers_detailed(outbound_section, "TAM")
            
            # Parsuj przesiadki dla lotu powrot  
            return_stops = self.parse_stopovers_detailed(return_section, "POWROT")
            
            # Oblicz rzeczywiste czasy lotow (bez przesiadek)
            actual_flight_outbound = self.calculate_flight_times(total_travel_outbound, outbound_stops)
            actual_flight_return = self.calculate_flight_times(total_travel_return, return_stops)
            
            print(f"Rzeczywiste czasy lotow: tam {actual_flight_outbound}, powrot {actual_flight_return}")
            
            return {
                'total_price': total,
                'price_per_person': per_person,
                'airlines_outbound': airlines_outbound,
                'airlines_return': airlines_return,
                'departure_airport': departure_airport,
                'destination_airport': destination_airport,
                'departure_time': dep_time,
                'arrival_time': arr_time,
                'return_departure_time': ret_dep_time,
                'return_arrival_time': ret_arr_time,
                'total_travel_time_outbound': total_travel_outbound,
                'total_travel_time_return': total_travel_return,
                'actual_flight_time_outbound': actual_flight_outbound,
                'actual_flight_time_return': actual_flight_return,
                'stops_outbound': outbound_stops['stops_count'],
                'stop1_outbound_airport': outbound_stops['stop1_airport'],
                'stop1_outbound_duration': outbound_stops['stop1_duration'],
                'stop2_outbound_airport': outbound_stops['stop2_airport'],
                'stop2_outbound_duration': outbound_stops['stop2_duration'],
                'stop3_outbound_airport': outbound_stops['stop3_airport'],
                'stop3_outbound_duration': outbound_stops['stop3_duration'],
                'stops_return': return_stops['stops_count'],
                'stop1_return_airport': return_stops['stop1_airport'],
                'stop1_return_duration': return_stops['stop1_duration'],
                'stop2_return_airport': return_stops['stop2_airport'],
                'stop2_return_duration': return_stops['stop2_duration'],
                'stop3_return_airport': return_stops['stop3_airport'],
                'stop3_return_duration': return_stops['stop3_duration']
            }
            
        except Exception as e:
            print(f"Blad parsowania szczegolow: {e}")
            import traceback
            traceback.print_exc()
            return {
                'total_price': total,
                'price_per_person': per_person,
                'airlines_outbound': file_info.get('airline_filter', 'UNKNOWN'),
                'airlines_return': file_info.get('airline_filter', 'UNKNOWN'),
                'departure_airport': file_info.get('departure_airport', 'WAW'),
                'destination_airport': file_info.get('destination_airport', 'ICN'),
                'departure_time': "",
                'arrival_time': "",
                'return_departure_time': "",
                'return_arrival_time': "",
                'total_travel_time_outbound': "",
                'total_travel_time_return': "",
                'actual_flight_time_outbound': "",
                'actual_flight_time_return': "",
                'stops_outbound': 0,
                'stop1_outbound_airport': "", 'stop1_outbound_duration': "",
                'stop2_outbound_airport': "", 'stop2_outbound_duration': "",
                'stop3_outbound_airport': "", 'stop3_outbound_duration': "",
                'stops_return': 0,
                'stop1_return_airport': "", 'stop1_return_duration': "",
                'stop2_return_airport': "", 'stop2_return_duration': "",
                'stop3_return_airport': "", 'stop3_return_duration': ""
            }
    
    def split_offer_sections(self, offer_text: str) -> tuple:
        """Dzieli tekst oferty na sekcje tam i powrot"""
        try:
            # Znajdz wszystkie czasy lotow, zeby okreslic podzial
            time_matches = list(re.finditer(r'(\d{2}:\d{2})\s*[–-]\s*(\d{2}:\d{2}(?:\+\d)?)', offer_text))
            
            if len(time_matches) < 2:
                print(f"Znaleziono tylko {len(time_matches)} czasow lotow")
                return offer_text, ""
            
            # Pierwszy czas to lot tam, drugi to lot powrot
            first_time_end = time_matches[0].end()
            second_time_start = time_matches[1].start()
            
            # Znajdz punkt podzialu miedzy lotami
            # Szukamy pustej linii lub charakterystycznego wzorca miedzy czasami
            middle_text = offer_text[first_time_end:second_time_start]
            
            # Znajdz najlepszy punkt podzialu
            split_point = first_time_end
            
            # Szukaj wzorcow ktore moga oznaczac koniec pierwszego lotu
            patterns = [
                r'\n\s*\n',  # Pusta linia
                r'\d+\s*h\s*\d+\s*min\s*\n',  # Czas trwania + nowa linia
                r'Air\s+China\s*\n',  # Nazwa linii na poczatku powrotu
                r'\n[A-Z]{3}\s*\n'  # Kod lotniska na nowej linii
            ]
            
            for pattern in patterns:
                matches = list(re.finditer(pattern, middle_text))
                if matches:
                    # Wez ostatnie dopasowanie jako punkt podzialu
                    last_match = matches[-1]
                    split_point = first_time_end + last_match.end()
                    break
            
            outbound_section = offer_text[:split_point]
            return_section = offer_text[split_point:]
            
            print(f"Podzial sekcji: tam ({len(outbound_section)} znakow), powrot ({len(return_section)} znakow)")
            
            return outbound_section, return_section
            
        except Exception as e:
            print(f"Blad podzialu sekcji: {e}")
            # Fallback - podziel po polowie
            mid = len(offer_text) // 2
            return offer_text[:mid], offer_text[mid:]
    
    def parse_stopovers_detailed(self, text: str, section_name: str = "") -> dict:
        """Parsuje szczegolowe informacje o przesiadkach"""
        # Wzorzec: PEK Przesiadka 4 h 15 min, lub VIE Przesiadka 1 h 50 min,
        stopover_pattern = r'([A-Z]{3})\s*Przesiadka\s*(\d+\s*h\s*\d+\s*min)'
        stopovers = re.findall(stopover_pattern, text)
        
        result = {
            'stops_count': len(stopovers),
            'stop1_airport': '', 'stop1_duration': '',
            'stop2_airport': '', 'stop2_duration': '',
            'stop3_airport': '', 'stop3_duration': ''
        }
        
        if section_name:
            print(f"Przesiadki {section_name}: {len(stopovers)}")
        
        for i, (airport, duration) in enumerate(stopovers[:3]):  # Max 3 przesiadki
            result[f'stop{i+1}_airport'] = airport
            result[f'stop{i+1}_duration'] = duration.strip()
            if section_name:
                print(f"      {i+1}. {airport} ({duration.strip()})")
        
        return result
    
    def calculate_flight_times(self, total_time: str, stopovers: dict) -> str:
        """Oblicza rzeczywisty czas lotu (bez przesiadek)"""
        if not total_time:
            return ""
        
        try:
            # Parsuj calkowity czas (np. "15 h 05 min")
            total_match = re.match(r'(\d+)\s*h\s*(\d+)\s*min', total_time)
            if not total_match:
                return ""
            
            total_hours = int(total_match.group(1))
            total_minutes = int(total_match.group(2))
            total_time_minutes = total_hours * 60 + total_minutes
            
            # Odejmij czasy przesiadek
            stopover_minutes = 0
            for i in range(1, 4):  # stop1, stop2, stop3
                duration = stopovers.get(f'stop{i}_duration', '')
                if duration:
                    stop_match = re.match(r'(\d+)\s*h\s*(\d+)\s*min', duration)
                    if stop_match:
                        stop_hours = int(stop_match.group(1))
                        stop_mins = int(stop_match.group(2))
                        stopover_minutes += stop_hours * 60 + stop_mins
            
            # Oblicz rzeczywisty czas lotu
            flight_time_minutes = total_time_minutes - stopover_minutes
            
            if flight_time_minutes <= 0:
                return total_time  # Jesli cos poszlo nie tak, zwroc oryginalny czas
            
            flight_hours = flight_time_minutes // 60
            flight_mins = flight_time_minutes % 60
            
            return f"{flight_hours} h {flight_mins:02d} min"
            
        except Exception as e:
            print(f"Blad obliczania czasu lotu: {e}")
            return total_time
    
    def parse_airports(self, text: str) -> tuple:
        """Wyciaga lotniska wylotu i docelowe"""
        # Szukaj WAW i ICN w tekscie
        departure_airport = "WAW"  # Domyslnie WAW (Warszawa)
        destination_airport = "ICN"  # Domyslnie ICN (Inczhon)
        
        # Sprawdz kierunek lotu w tekscie
        if "WAW" in text and "ICN" in text:
            waw_pos = text.find("WAW")
            icn_pos = text.find("ICN")
            
            # Pierwszy wystepujacy to prawdopodobnie wylot
            if waw_pos < icn_pos:
                departure_airport = "WAW"
                destination_airport = "ICN"
            else:
                departure_airport = "ICN" 
                destination_airport = "WAW"
        
        return departure_airport, destination_airport
    
    def process_session_folder(self, session_folder: str) -> List[SimpleOffer]:
        """Przetwarza wszystkie pliki w folderze sesji"""
        folder_path = Path(session_folder)
        
        if not folder_path.exists():
            print(f"Folder nie istnieje: {session_folder}")
            return []
        
        txt_files = list(folder_path.glob("*.txt"))
        print(f"Znaleziono {len(txt_files)} plikow .txt")
        
        offers = []
        
        for txt_file in txt_files:
            print(f"\nPrzetwarzanie: {txt_file.name}")
            
            try:
                with open(txt_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                file_info = self.parse_filename(txt_file.name)
                print(f"Z nazwy pliku: {file_info['airline_filter']} | {file_info['departure_airport']}->{file_info['destination_airport']} | {file_info['departure_date']} -> {file_info['return_date']}")
                
                result = self.extract_first_offer_simple(content)
                
                if result and len(result) == 3:  # offer_text, per_person, total
                    offer_text, per_person, total = result
                    offer_data = self.parse_offer_from_text(offer_text, per_person, total, file_info)
                    
                    if offer_data:
                        offer = SimpleOffer(
                            filename=txt_file.name,
                            airline_filter=file_info['airline_filter'],
                            departure_date=file_info['departure_date'],
                            return_date=file_info['return_date'],
                            **offer_data
                        )
                        offers.append(offer)
                        # Użyj normalnych znaków zamiast emoji
                        print(f"OK {offer.total_price:,.0f} PLN - {offer.airlines_outbound} ({offer.departure_airport}->{offer.destination_airport})")
                    else:
                        print(f"BLAD Blad parsowania szczegolow oferty")
                else:
                    print(f"BLAD Nie znaleziono oferty")
                    
            except Exception as e:
                print(f"BLAD: {e}")
        
        return offers
    
    def export_to_excel(self, offers: List[SimpleOffer], output_file: str = None) -> str:
        """Eksportuje oferty do Excel"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"kayak_offers_{timestamp}.xlsx"
        
        # Konwertuj na DataFrame
        data = []
        for offer in offers:
            data.append({
                # PODSTAWOWE INFORMACJE
                'Plik': offer.filename,
                'Filtr linii': offer.airline_filter,
                'Data wylotu': offer.departure_date,
                'Data powrotu': offer.return_date,
                'Cena łączna (PLN)': offer.total_price,
                'Cena za osobę (PLN)': offer.price_per_person,
                
                # LOTNISKA (NOWE/POPRAWIONE KOLUMNY)
                'Lotnisko wylotu': offer.departure_airport,
                'Lotnisko docelowe': offer.destination_airport,
                'Trasa': f"{offer.departure_airport} → {offer.destination_airport}",
                
                # LINIE LOTNICZE
                'Linie lotnicze tam': offer.airlines_outbound,
                'Linie lotnicze powrót': offer.airlines_return,
                
                # CZASY LOTÓW
                'Wylot tam': offer.departure_time,
                'Przylot tam': offer.arrival_time,
                'Wylot powrót': offer.return_departure_time,
                'Przylot powrót': offer.return_arrival_time,
                
                # CZASY PODRÓŻY
                'Czas podróży tam (total)': offer.total_travel_time_outbound,
                'Czas podróży powrót (total)': offer.total_travel_time_return,
                'Czas lotu tam (bez przesiadek)': offer.actual_flight_time_outbound,
                'Czas lotu powrót (bez przesiadek)': offer.actual_flight_time_return,
                
                # PRZESIADKI TAM
                'Przesiadki tam': offer.stops_outbound,
                'Przesiadka 1 tam - lotnisko': offer.stop1_outbound_airport,
                'Przesiadka 1 tam - czas': offer.stop1_outbound_duration,
                'Przesiadka 2 tam - lotnisko': offer.stop2_outbound_airport,
                'Przesiadka 2 tam - czas': offer.stop2_outbound_duration,
                'Przesiadka 3 tam - lotnisko': offer.stop3_outbound_airport,
                'Przesiadka 3 tam - czas': offer.stop3_outbound_duration,
                
                # PRZESIADKI POWRÓT
                'Przesiadki powrót': offer.stops_return,
                'Przesiadka 1 powrót - lotnisko': offer.stop1_return_airport,
                'Przesiadka 1 powrót - czas': offer.stop1_return_duration,
                'Przesiadka 2 powrót - lotnisko': offer.stop2_return_airport,
                'Przesiadka 2 powrót - czas': offer.stop2_return_duration,
                'Przesiadka 3 powrót - lotnisko': offer.stop3_return_airport,
                'Przesiadka 3 powrót - czas': offer.stop3_return_duration
            })
        
        df = pd.DataFrame(data)
        
        # Sortuj po cenie
        df = df.sort_values('Cena łączna (PLN)', ascending=True)
        
        # Zapisz do Excel z wieloma arkuszami
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Główny arkusz - wszystkie oferty
            df.to_excel(writer, sheet_name='Wszystkie oferty', index=False)
            
            # Najlepsze oferty per linia
            if len(offers) > 0:
                best_per_airline = df.groupby('Filtr linii').first().reset_index()
                best_per_airline = best_per_airline.sort_values('Cena łączna (PLN)', ascending=True)
                best_per_airline.to_excel(writer, sheet_name='Najlepsze per linia', index=False)
                
                # Statystyki tras
                route_stats = df.groupby('Trasa').agg({
                    'Cena łączna (PLN)': ['count', 'min', 'max', 'mean'],
                    'Przesiadki tam': 'mean',
                    'Przesiadki powrót': 'mean'
                }).round(0)
                route_stats.columns = ['Liczba ofert', 'Min cena', 'Max cena', 'Średnia cena', 'Śr. przesiadki tam', 'Śr. przesiadki powrót']
                route_stats.to_excel(writer, sheet_name='Statystyki tras')
            
            # Podsumowanie
            if offers:
                summary_data = {
                    'Metryka': [
                        'Liczba plików przetworzonych',
                        'Liczba znalezionych ofert', 
                        'Najniższa cena (PLN)',
                        'Najwyższa cena (PLN)',
                        'Średnia cena (PLN)',
                        'Mediana ceny (PLN)',
                        'Unikalne trasy',
                        'Unikalne linie lotnicze'
                    ],
                    'Wartość': [
                        len(offers),
                        len([o for o in offers if o.total_price > 0]),
                        f"{min(o.total_price for o in offers if o.total_price > 0):,.0f}",
                        f"{max(o.total_price for o in offers if o.total_price > 0):,.0f}",
                        f"{sum(o.total_price for o in offers if o.total_price > 0) / len([o for o in offers if o.total_price > 0]):,.0f}",
                        f"{sorted([o.total_price for o in offers if o.total_price > 0])[len([o for o in offers if o.total_price > 0])//2]:,.0f}",
                        len(df['Trasa'].unique()),
                        len(df['Filtr linii'].unique())
                    ]
                }
                
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Podsumowanie', index=False)
        
        print(f"\nEksport zakończony: {output_file}")
        print(f"Wyeksportowano {len(offers)} ofert")
        
        if offers:
            valid_prices = [offer.total_price for offer in offers if offer.total_price > 0]
            if valid_prices:
                print(f"Najniższa cena: {min(valid_prices):,.0f} PLN")
                print(f"Najwyższa cena: {max(valid_prices):,.0f} PLN")
                print(f"Średnia cena: {sum(valid_prices)/len(valid_prices):,.0f} PLN")
                
                # Pokaż najlepsze trasy
                routes = {}
                for offer in offers:
                    if offer.total_price > 0:
                        route = f"{offer.departure_airport}→{offer.destination_airport}"
                        if route not in routes or offer.total_price < routes[route]:
                            routes[route] = offer.total_price
                
                print(f"\nNajlepsze ceny per trasa:")
                for route, price in sorted(routes.items(), key=lambda x: x[1])[:5]:
                    print(f"   {route}: {price:,.0f} PLN")
        
        return output_file

def main():
    """Glowna funkcja"""
    import sys
    
    if len(sys.argv) < 2:
        print("SIMPLE KAYAK DATA EXTRACTOR")
        print("=" * 40)
        print("Uzycie:")
        print(f"  python {sys.argv[0]} <folder_sesji>")
        print()
        print("Przyklad:")
        print(f"  python {sys.argv[0]} kayak_text_data/txt_session_20250616_194500")
        print()
        
        # Pokaz dostepne foldery
        base_dir = Path("kayak_text_data")
        if base_dir.exists():
            sessions = [d for d in base_dir.iterdir() if d.is_dir() and d.name.startswith('txt_session_')]
            if sessions:
                print("Dostepne sesje:")
                for session in sorted(sessions, reverse=True):
                    txt_count = len(list(session.glob("*.txt")))
                    print(f"  {session.name} ({txt_count} plikow)")
        
        # Sprawdź też excel_session
        excel_base_dir = Path("kayak_excel_data")
        if excel_base_dir.exists():
            excel_sessions = [d for d in excel_base_dir.iterdir() if d.is_dir() and d.name.startswith('excel_session_')]
            if excel_sessions:
                print("\nDostepne sesje Excel:")
                for session in sorted(excel_sessions, reverse=True):
                    txt_count = len(list(session.glob("*.txt")))
                    print(f"  {session.name} ({txt_count} plikow)")
        
        return 1
    
    session_folder = sys.argv[1]
    
    print(f"Przetwarzanie sesji: {session_folder}")
    
    # Sprawdź czy folder istnieje
    if not os.path.exists(session_folder):
        print(f"Folder nie istnieje: {session_folder}")
        return 1
    
    extractor = SimpleKayakExtractor()
    offers = extractor.process_session_folder(session_folder)
    
    if offers:
        output_file = extractor.export_to_excel(offers)
        print(f"Gotowe! Sprawdz plik: {output_file}")
    else:
        print("Brak ofert do eksportu")
    
    return 0

if __name__ == "__main__":
    exit(main())