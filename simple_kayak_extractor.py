#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Kayak Data Extractor
Wyciąga pierwszą (najtańszą) ofertę z każdego pliku .txt i zapisuje do Excel
"""

import os
import re
import pandas as pd
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List

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
    
    # Czasy lotów
    departure_time: str
    arrival_time: str
    return_departure_time: str
    return_arrival_time: str
    
    # Czasy podróży i lotów
    total_travel_time_outbound: str  # Całkowity czas podróży tam
    total_travel_time_return: str    # Całkowity czas podróży powrót
    actual_flight_time_outbound: str # Czas lotu bez przesiadek tam
    actual_flight_time_return: str   # Czas lotu bez przesiadek powrót
    
    # Przesiadki tam (max 3)
    stops_outbound: int
    stop1_outbound_airport: str
    stop1_outbound_duration: str
    stop2_outbound_airport: str
    stop2_outbound_duration: str
    stop3_outbound_airport: str
    stop3_outbound_duration: str
    
    # Przesiadki powrót (max 3)
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
        """Parsuje nazwę pliku dla pewnych danych"""
        # China_Air_2025-10-06_2025-10-27_20250616_192540_948.txt
        # LOT_2025-10-05_2025-10-25_20250616_194501_123.txt  
        # Qatar_2025-10-23_2025-11-15_20250616_192648_481.txt
        
        pattern = r'([A-Za-z_]+)_(\d{4}-\d{2}-\d{2})_(\d{4}-\d{2}-\d{2})_(\d{8})_(\d{6})_(\d+)\.txt'
        match = re.match(pattern, filename)
        
        if match:
            airline_name = match.group(1).replace('_', ' ')  # China_Air -> China Air
            return {
                'airline_filter': airline_name,
                'departure_date': match.group(2),
                'return_date': match.group(3),
                'session_date': match.group(4),
                'session_time': match.group(5),
                'sequence': match.group(6)
            }
        
        print(f"  ⚠️  Nie rozpoznano formatu nazwy pliku: {filename}")
        return {
            'airline_filter': 'UNKNOWN', 
            'departure_date': '', 
            'return_date': '',
            'session_date': '',
            'session_time': '',
            'sequence': ''
        }
    
    def extract_first_offer_simple(self, content: str) -> Optional[dict]:
        """Wyciąga pierwszą ofertę z tekstu Kayak"""
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
                    print(f"  🎯 Znaleziono ceny używając {pattern_used}")
                    break
            
            if not price_match:
                print(f"  🔍 DEBUG: Nie znaleziono standardowych wzorców, sprawdzam zawartość...")
                
                # Znajdź wszystkie wystąpienia z "zł"
                zl_pattern = r'(\d+(?:\s+\d{3})*)\s*zł'
                zl_matches = list(re.finditer(zl_pattern, content))
                
                if zl_matches:
                    print(f"  💰 Znaleziono {len(zl_matches)} cen w zł:")
                    for j, match in enumerate(zl_matches[:8]):  # Pokaż pierwsze 8
                        price_value = match.group(1).replace(' ', '')
                        context_start = max(0, match.start() - 30)
                        context_end = min(len(content), match.end() + 30)
                        context = content[context_start:context_end].replace('\n', ' ').replace('\r', ' ')
                        print(f"    {j+1}. {price_value} zł - ...{context}...")
                    
                    # Spróbuj znaleźć parę cen (na osobę + łącznie)
                    prices = []
                    for match in zl_matches:
                        price_str = match.group(1).replace(' ', '')
                        try:
                            price_val = int(price_str)
                            if 1000 <= price_val <= 50000:  # Rozsądny zakres cen
                                prices.append((price_val, match.start(), match.end()))
                        except:
                            continue
                    
                    print(f"  🎯 Ceny w rozsądnym zakresie: {[p[0] for p in prices]}")
                    
                    # Jeśli mamy dokładnie 2 ceny, sprawdź czy jedna to połowa drugiej
                    if len(prices) >= 2:
                        for i in range(len(prices)-1):
                            price1, pos1, end1 = prices[i]
                            price2, pos2, end2 = prices[i+1]
                            
                            # Sprawdź czy jedna cena to około połowa drugiej (na osobę vs łącznie)
                            if abs(price2 - price1 * 2) < 100:  # Tolerancja 100 zł
                                print(f"  ✅ Znaleziono parę cen: {price1} i {price2} (2 osoby)")
                                per_person = float(price1)
                                total = float(price2)
                                
                                # Znajdź tekst oferty
                                offer_start = max(0, pos1 - 1000)  # 1000 znaków przed pierwszą ceną
                                offer_end = end2
                                offer_text = content[offer_start:offer_end]
                                
                                return offer_text, per_person, total
                
                print(f"  ❌ Nie znaleziono odpowiednich cen")
                return None
            
            # Standardowe parsowanie gdy znaleziono wzorzec
            per_person_str = price_match.group(1).replace(' ', '')
            total_str = price_match.group(2).replace(' ', '')
            
            per_person = float(per_person_str)
            total = float(total_str)
            
            print(f"  💰 Ceny: {per_person} PLN/os → {total} PLN łącznie ({pattern_used})")
            
            # Znajdź tekst oferty
            price_pos = price_match.start()
            offer_start = max(0, price_pos - 1000)
            offer_text = content[offer_start:price_match.end()]
            
            return offer_text, per_person, total
            
        except Exception as e:
            print(f"❌ Błąd parsowania: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def parse_offer_from_text(self, offer_text: str, per_person: float, total: float, airline_from_filename: str) -> dict:
        """Parsuje szczegółowe dane oferty z tekstu"""
        try:
            print(f"  📄 Parsowanie oferty ({len(offer_text)} znaków)")
            print(f"  ✈️  Linia z nazwy pliku: {airline_from_filename}")
            
            # Użyj nazwy linii z pliku jako głównej
            airlines_outbound = airline_from_filename
            airlines_return = airline_from_filename
            
            # Znajdź lotniska
            departure_airport, destination_airport = self.parse_airports(offer_text)
            print(f"  🛫 Trasa: {departure_airport} → {destination_airport}")
            
            # Znajdź czasy lotów
            time_matches = re.findall(r'(\d{2}:\d{2})\s*[–-]\s*(\d{2}:\d{2}(?:\+\d)?)', offer_text)
            
            dep_time = arr_time = ret_dep_time = ret_arr_time = ""
            if len(time_matches) >= 1:
                dep_time, arr_time = time_matches[0]
                print(f"  🕐 Lot tam: {dep_time} → {arr_time}")
            if len(time_matches) >= 2:
                ret_dep_time, ret_arr_time = time_matches[1]
                print(f"  🕐 Lot powrót: {ret_dep_time} → {ret_arr_time}")
            
            # Znajdź czasy podróży (najdłuższe czasy w sekcjach)
            duration_matches = re.findall(r'(\d+\s*h\s*\d+\s*min)', offer_text)
            total_travel_outbound = duration_matches[0] if len(duration_matches) >= 1 else ""
            total_travel_return = duration_matches[1] if len(duration_matches) >= 2 else ""
            
            print(f"  ⏱️  Czasy podróży: tam {total_travel_outbound}, powrót {total_travel_return}")
            
            # Podziel tekst na sekcje (tam i powrót) - używamy nowej funkcji
            outbound_section, return_section = self.split_offer_sections(offer_text)
            
            # DEBUG: Pokaż fragmenty sekcji
            print(f"    📄 Sekcja TAM: {outbound_section[:100]}...")
            print(f"    📄 Sekcja POWRÓT: {return_section[:100]}...")
            
            # Parsuj przesiadki dla lotu tam
            outbound_stops = self.parse_stopovers_detailed(outbound_section, "TAM")
            
            # Parsuj przesiadki dla lotu powrót  
            return_stops = self.parse_stopovers_detailed(return_section, "POWRÓT")
            
            # Oblicz rzeczywiste czasy lotów (bez przesiadek)
            actual_flight_outbound = self.calculate_flight_times(total_travel_outbound, outbound_stops)
            actual_flight_return = self.calculate_flight_times(total_travel_return, return_stops)
            
            print(f"  ✈️  Rzeczywiste czasy lotów: tam {actual_flight_outbound}, powrót {actual_flight_return}")
            
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
            print(f"❌ Błąd parsowania szczegółów: {e}")
            import traceback
            traceback.print_exc()
            return {
                'total_price': total,
                'price_per_person': per_person,
                'airlines_outbound': airline_from_filename,
                'airlines_return': airline_from_filename,
                'departure_airport': "WAW",
                'destination_airport': "ICN",
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
        """Dzieli tekst oferty na sekcje tam i powrót"""
        try:
            # Znajdź wszystkie czasy lotów, żeby określić podział
            time_matches = list(re.finditer(r'(\d{2}:\d{2})\s*[–-]\s*(\d{2}:\d{2}(?:\+\d)?)', offer_text))
            
            if len(time_matches) < 2:
                print(f"    ⚠️  Znaleziono tylko {len(time_matches)} czasów lotów")
                return offer_text, ""
            
            # Pierwszy czas to lot tam, drugi to lot powrót
            first_time_end = time_matches[0].end()
            second_time_start = time_matches[1].start()
            
            # Znajdź punkt podziału między lotami
            # Szukamy pustej linii lub charakterystycznego wzorca między czasami
            middle_text = offer_text[first_time_end:second_time_start]
            
            # Znajdź najlepszy punkt podziału
            split_point = first_time_end
            
            # Szukaj wzorców które mogą oznaczać koniec pierwszego lotu
            patterns = [
                r'\n\s*\n',  # Pusta linia
                r'\d+\s*h\s*\d+\s*min\s*\n',  # Czas trwania + nowa linia
                r'Air\s+China\s*\n',  # Nazwa linii na początku powrotu
                r'\n[A-Z]{3}\s*\n'  # Kod lotniska na nowej linii
            ]
            
            for pattern in patterns:
                matches = list(re.finditer(pattern, middle_text))
                if matches:
                    # Weź ostatnie dopasowanie jako punkt podziału
                    last_match = matches[-1]
                    split_point = first_time_end + last_match.end()
                    break
            
            outbound_section = offer_text[:split_point]
            return_section = offer_text[split_point:]
            
            print(f"    📦 Podział sekcji: tam ({len(outbound_section)} znaków), powrót ({len(return_section)} znaków)")
            
            return outbound_section, return_section
            
        except Exception as e:
            print(f"    ⚠️  Błąd podziału sekcji: {e}")
            # Fallback - podziel po połowie
            mid = len(offer_text) // 2
            return offer_text[:mid], offer_text[mid:]
    
    def parse_stopovers_detailed(self, text: str, section_name: str = "") -> dict:
        """Parsuje szczegółowe informacje o przesiadkach"""
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
            print(f"    🔄 Przesiadki {section_name}: {len(stopovers)}")
        
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
            # Parsuj całkowity czas (np. "15 h 05 min")
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
                return total_time  # Jeśli coś poszło nie tak, zwróć oryginalny czas
            
            flight_hours = flight_time_minutes // 60
            flight_mins = flight_time_minutes % 60
            
            return f"{flight_hours} h {flight_mins:02d} min"
            
        except Exception as e:
            print(f"    ⚠️  Błąd obliczania czasu lotu: {e}")
            return total_time
    
    def parse_airports(self, text: str) -> tuple:
        """Wyciąga lotniska wylotu i docelowe"""
        # Szukaj WAW i ICN w tekście
        departure_airport = "WAW"  # Domyślnie WAW (Warszawa)
        destination_airport = "ICN"  # Domyślnie ICN (Inczhon)
        
        # Sprawdź kierunek lotu w tekście
        if "WAW" in text and "ICN" in text:
            waw_pos = text.find("WAW")
            icn_pos = text.find("ICN")
            
            # Pierwszy występujący to prawdopodobnie wylot
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
            print(f"❌ Folder nie istnieje: {session_folder}")
            return []
        
        txt_files = list(folder_path.glob("*.txt"))
        print(f"🔍 Znaleziono {len(txt_files)} plików .txt")
        
        offers = []
        
        for txt_file in txt_files:
            print(f"📄 Przetwarzanie: {txt_file.name}")
            
            try:
                with open(txt_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                file_info = self.parse_filename(txt_file.name)
                print(f"  📋 Z nazwy pliku: {file_info['airline_filter']} | {file_info['departure_date']} → {file_info['return_date']}")
                
                result = self.extract_first_offer_simple(content)
                
                if result and len(result) == 3:  # offer_text, per_person, total
                    offer_text, per_person, total = result
                    offer_data = self.parse_offer_from_text(offer_text, per_person, total, file_info['airline_filter'])
                    
                    if offer_data:
                        offer = SimpleOffer(
                            filename=txt_file.name,
                            airline_filter=file_info['airline_filter'],
                            departure_date=file_info['departure_date'],
                            return_date=file_info['return_date'],
                            **offer_data
                        )
                        offers.append(offer)
                        print(f"  ✅ {offer.total_price:,.0f} PLN - {offer.airlines_outbound}")
                    else:
                        print(f"  ❌ Błąd parsowania szczegółów oferty")
                else:
                    print(f"  ❌ Nie znaleziono oferty")
                    
            except Exception as e:
                print(f"  ❌ Błąd: {e}")
        
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
                'Plik': offer.filename,
                'Filtr linii': offer.airline_filter,
                'Data wylotu': offer.departure_date,
                'Data powrotu': offer.return_date,
                'Cena łączna (PLN)': offer.total_price,
                'Cena za osobę (PLN)': offer.price_per_person,
                
                # Linie i lotniska
                'Linie lotnicze tam': offer.airlines_outbound,
                'Linie lotnicze powrót': offer.airlines_return,
                'Lotnisko wylotu': offer.departure_airport,
                'Lotnisko docelowe': offer.destination_airport,
                
                # Czasy
                'Wylot tam': offer.departure_time,
                'Przylot tam': offer.arrival_time,
                'Wylot powrót': offer.return_departure_time,
                'Przylot powrót': offer.return_arrival_time,
                
                # Czasy podróży
                'Czas podróży tam (total)': offer.total_travel_time_outbound,
                'Czas podróży powrót (total)': offer.total_travel_time_return,
                'Czas lotu tam (bez przesiadek)': offer.actual_flight_time_outbound,
                'Czas lotu powrót (bez przesiadek)': offer.actual_flight_time_return,
                
                # Przesiadki tam
                'Przesiadki tam': offer.stops_outbound,
                'Przesiadka 1 tam - lotnisko': offer.stop1_outbound_airport,
                'Przesiadka 1 tam - czas': offer.stop1_outbound_duration,
                'Przesiadka 2 tam - lotnisko': offer.stop2_outbound_airport,
                'Przesiadka 2 tam - czas': offer.stop2_outbound_duration,
                'Przesiadka 3 tam - lotnisko': offer.stop3_outbound_airport,
                'Przesiadka 3 tam - czas': offer.stop3_outbound_duration,
                
                # Przesiadki powrót
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
        
        # Zapisz do Excel
        df.to_excel(output_file, index=False, engine='openpyxl')
        
        print(f"📊 Eksport zakończony: {output_file}")
        print(f"📈 Wyeksportowano {len(offers)} ofert")
        
        if offers:
            prices = [offer.total_price for offer in offers]
            print(f"💰 Najniższa cena: {min(prices):,.0f} PLN")
            print(f"💰 Najwyższa cena: {max(prices):,.0f} PLN")
            print(f"💰 Średnia cena: {sum(prices)/len(prices):,.0f} PLN")
        
        return output_file

def main():
    """Główna funkcja"""
    import sys
    
    if len(sys.argv) < 2:
        print("🚀 SIMPLE KAYAK DATA EXTRACTOR")
        print("=" * 40)
        print("Użycie:")
        print(f"  python {sys.argv[0]} <folder_sesji>")
        print()
        print("Przykład:")
        print(f"  python {sys.argv[0]} kayak_text_data/txt_session_20250616_194500")
        print()
        
        # Pokaż dostępne foldery
        base_dir = Path("kayak_text_data")
        if base_dir.exists():
            sessions = [d for d in base_dir.iterdir() if d.is_dir() and d.name.startswith('txt_session_')]
            if sessions:
                print("📁 Dostępne sesje:")
                for session in sorted(sessions, reverse=True):
                    txt_count = len(list(session.glob("*.txt")))
                    print(f"  {session.name} ({txt_count} plików)")
        
        return 1
    
    session_folder = sys.argv[1]
    
    print(f"🔄 Przetwarzanie sesji: {session_folder}")
    
    extractor = SimpleKayakExtractor()
    offers = extractor.process_session_folder(session_folder)
    
    if offers:
        output_file = extractor.export_to_excel(offers)
        print(f"✅ Gotowe! Sprawdź plik: {output_file}")
    else:
        print("❌ Brak ofert do eksportu")
    
    return 0

if __name__ == "__main__":
    exit(main())