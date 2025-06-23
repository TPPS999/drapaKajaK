# 📊 Kayak Data Extractor - Kompletny przewodnik

Simple Kayak Data Extractor to narzędzie do automatycznego wyciągania najlepszych ofert z plików tekstowych wygenerowanych przez scrapery i organizowania ich w przejrzystym Excel.

## 🎯 Co robi Data Extractor?

### Automatyczne wyciąganie danych:
- **Pierwsza oferta** - najtańsza z każdego pliku .txt
- **Szczegółowe parsowanie** - czasy lotów, przesiadki, lotniska
- **Inteligentna analiza** - rozpoznaje wzorce Kayak
- **Excel export** - przejrzysta tabela z sortowaniem

### Wyciągane informacje:
- 💰 **Ceny** - łączna i za osobę
- ✈️ **Linie lotnicze** - tam i powrót
- 🛫 **Lotniska** - wylotu i docelowe
- 🕐 **Czasy** - wylotu, przylotu, całkowity czas podróży
- 🔄 **Przesiadki** - liczba, lotniska, czasy oczekiwania
- ⏱️ **Rzeczywisty czas lotu** - bez przesiadek

## 🚀 Podstawowe użycie

### 1. Sprawdź dostępne sesje

```bash
python simple_kayak_extractor.py
```

**Wynik:**
```
🚀 SIMPLE KAYAK DATA EXTRACTOR
========================================
Użycie:
  python simple_kayak_extractor.py <folder_sesji>

📁 Dostępne sesje:
  txt_session_20250623_143022 (45 plików)
  txt_session_20250623_120500 (23 plików)
  excel_session_20250623_101500 (12 plików)
```

### 2. Wyciągnij dane z sesji

```bash
python simple_kayak_extractor.py kayak_text_data/txt_session_20250623_143022
```

**Proces:**
```
🔄 Przetwarzanie sesji: kayak_text_data/txt_session_20250623_143022
🔍 Znaleziono 45 plików .txt

📄 Przetwarzanie: WAW-ICN_Turkish_2025-10-22_2025-11-10_xxx.txt
  📋 Z nazwy pliku: Turkish | 2025-10-22 → 2025-11-10
  🎯 Znaleziono ceny używając Pattern 1
  💰 Ceny: 3609.0 PLN/os → 7218.0 PLN łącznie (Pattern 1)
  📄 Parsowanie oferty (1247 znaków)
  ✈️ Linia z nazwy pliku: Turkish
  🛫 Trasa: WAW → ICN
  🕐 Lot tam: 08:45 → 23:45+1
  🕐 Lot powrót: 18:30 → 07:00+1
  ⏱️ Czasy podróży: tam 32 h 00 min, powrót 19 h 30 min
  🔄 Przesiadki TAM: 2
    1. DXB (3 h 10 min)
    2. MNL (9 h 15 min)
  🔄 Przesiadki POWRÓT: 1
    1. AUH (3 h 25 min)
  ✈️ Rzeczywiste czasy lotów: tam 19 h 35 min, powrót 15 h 05 min
  ✅ 7,218 PLN - Turkish

📄 Przetwarzanie: WAW-ICN_Qatar_2025-10-21_2025-11-12_xxx.txt
  ...

📊 Eksport zakończony: kayak_offers_20250623_145000.xlsx
📈 Wyeksportowano 42 ofert
💰 Najniższa cena: 6,240 PLN
💰 Najwyższa cena: 12,450 PLN
💰 Średnia cena: 8,127 PLN
✅ Gotowe! Sprawdź plik: kayak_offers_20250623_145000.xlsx
```

## 📊 Struktura pliku Excel

### Podstawowe kolumny:
| Kolumna | Przykład | Opis |
|---------|----------|------|
| Plik | `WAW-ICN_Turkish_2025-10-22...` | Oryginalny plik źródłowy |
| Filtr linii | `Turkish` | Linia z konfiguracji |
| Data wylotu | `2025-10-22` | Data wylotu |
| Data powrotu | `2025-11-10` | Data powrotu |
| Cena łączna (PLN) | `7218` | Cena dla wszystkich pasażerów |
| Cena za osobę (PLN) | `3609` | Cena za jedną osobę |

### Szczegóły lotów:
| Kolumna | Przykład | Opis |
|---------|----------|------|
| Linie lotnicze tam | `flydubai, Philippine Airlines` | Przewoźnicy na trasie tam |
| Linie lotnicze powrót | `Etihad Airways` | Przewoźnicy na trasie powrót |
| Lotnisko wylotu | `WAW` | Kod IATA wylotu |
| Lotnisko docelowe | `ICN` | Kod IATA miejsca docelowego |

### Czasy lotów:
| Kolumna | Przykład | Opis |
|---------|----------|------|
| Wylot tam | `08:45` | Godzina wylotu |
| Przylot tam | `23:45+1` | Godzina przylotu (+1 = następny dzień) |
| Wylot powrót | `18:30` | Godzina wylotu powrotnego |
| Przylot powrót | `07:00+1` | Godzina przylotu powrotnego |

### Analiza czasów:
| Kolumna | Przykład | Opis |
|---------|----------|------|
| Czas podróży tam (total) | `32 h 00 min` | Całkowity czas z przesiadkami |
| Czas podróży powrót (total) | `19 h 30 min` | Całkowity czas z przesiadkami |
| Czas lotu tam (bez przesiadek) | `19 h 35 min` | Rzeczywisty czas w powietrzu |
| Czas lotu powrót (bez przesiadek) | `15 h 05 min` | Rzeczywisty czas w powietrzu |

### Przesiadki (max 3 na kierunek):
| Kolumna | Przykład | Opis |
|---------|----------|------|
| Przesiadki tam | `2` | Liczba przesiadek |
| Przesiadka 1 tam - lotnisko | `DXB` | Kod lotniska przesiadki |
| Przesiadka 1 tam - czas | `3 h 10 min` | Czas oczekiwania |
| Przesiadka 2 tam - lotnisko | `MNL` | Drugie lotnisko przesiadki |
| Przesiadka 2 tam - czas | `9 h 15 min` | Drugi czas oczekiwania |

## 🎯 Przykłady użycia

### Porównanie linii lotniczych
```bash
# Po scrapingu z różnymi liniami
python simple_kayak_extractor.py kayak_text_data/txt_session_20250623_143022
```

**Excel rezultat:**
- Sortowanie po cenie: Turkish 7,218 PLN → Qatar 8,450 PLN → Emirates 9,120 PLN
- Filtrowanie po przesiadkach: Pokaż tylko loty z max 1 przesiadką
- Analiza czasów: Znajdź najkrótsze czasy podróży

### Analiza konkretnych dat
```bash
# Po Excel Mode z wybranymi datami
python simple_kayak_extractor.py kayak_excel_data/excel_session_20250623_101500
```

**Excel rezultat:**
- Porównanie cen dla różnych dat wylotu
- Analiza wpływu długości pobytu na cenę
- Optymalizacja terminów

### Rolling mode - trend cen
```bash
# Po długotrwałym monitoringu
python simple_kayak_extractor.py rolling_mode
```

**Excel rezultat:**
- Najnowsze ceny z każdej rundy
- Tracking zmian cen w czasie
- Identyfikacja najlepszych momentów na zakup

## 🔧 Zaawansowane funkcje

### Inteligentne parsowanie cen

Extractor rozpoznaje różne formaty cen Kayak:
```
✅ "3 609 zł / osoba 7 218 zł łącznie"
✅ "3609 zł/osoba, 7218 zł łącznie"  
✅ "3 609 PLN per person, 7 218 PLN total"
```

### Automatyczne obliczanie czasów lotu

```
Czas podróży total: 32 h 00 min
- Przesiadka DXB: 3 h 10 min  
- Przesiadka MNL: 9 h 15 min
= Rzeczywisty lot: 19 h 35 min ✈️
```

### Rozpoznawanie struktur oferów

Extractor automatycznie dzieli tekst na sekcje:
- **Lot tam:** pierwszy blok z czasami i przesiadkami
- **Lot powrót:** drugi blok z czasami i przesiadkami
- **Ceny:** na końcu oferty

## 🛠️ Rozwiązywanie problemów

### Problem: "Nie znaleziono oferty"

**Przyczyny:**
- Plik .txt nie zawiera cen w rozpoznawalnym formacie
- Kayak zwrócił błąd zamiast ofert
- Niezgodność formatów

**Rozwiązanie:**
```bash
# Sprawdź kilka plików ręcznie
head -n 50 kayak_text_data/session/plik.txt
# Szukaj wzorców: "zł", "PLN", "osoba", "łącznie"
```

### Problem: "Błędne ceny"

**Debug:**
```bash
# Uruchom z pojedynczym plikiem
python simple_kayak_extractor.py single_file_test/
```

Extractor pokazuje proces parsowania:
```
🎯 Znaleziono ceny używając Pattern 1
💰 Ceny: 3609.0 PLN/os → 7218.0 PLN łącznie (Pattern 1)
```

### Problem: "Brak przesiadek"

**Przyczyny:**
- Loty direct (bez przesiadek) ✅ 
- Niewykryte wzorce przesiadek
- Błędy w tekście Kayak

**Weryfikacja:**
```bash
# Sprawdź oryginalny tekst
grep -A 10 -B 10 "Przesiadka" kayak_text_data/session/plik.txt
```

### Problem: "Błędne czasy lotów"

**Najczęstsze przyczyny:**
- Strefy czasowe (+1, +2) - to normalne ✅
- Loty przez datę (departure 23:45, arrival 07:00+1) ✅
- Niepoprawne parsowanie formatów czasu

**Sprawdzenie:**
```bash
# Znajdź wszystkie wzorce czasów w pliku
grep -E "\d{2}:\d{2}" kayak_text_data/session/plik.txt
```

## 📈 Analiza wyników w Excel

### Sortowanie i filtrowanie

**Po otwarciu Excel:**

1. **Sortuj po cenie** - znajdź najtańsze oferty
2. **Filtruj po linii** - porównaj konkretnych przewoźników  
3. **Filtruj po przesiadkach** - wybierz loty direct lub z max 1 przesiadką
4. **Filtruj po czasie** - eliminuj za długie podróże

### Przydatne formuły Excel

**Oblicz oszczędności vs średnia:**
```excel
=ŚREDNIA(E:E)-E2
```

**Ranking czasów podróży:**
```excel
=RANK(P2,P:P,1)
```

**Stosunek cena/czas:**
```excel
=E2/CZAS(P2)
```

### Wykresy i dashboardy

**Scatter plot: Cena vs Czas podróży**
- X: Czas podróży (total)
- Y: Cena łączna
- Znajdź optimum: niska cena + krótki czas

**Bar chart: Średnie ceny według linii**
- Porównaj średnie ceny różnych przewoźników
- Identyfikuj najbardziej competitive linie

## 🔄 Workflow dla różnych scenariuszy

### Scenariusz 1: Poszukiwanie najlepszej oferty

```bash
# 1. Scraping wszystkich kombinacji
python scrap_only_extended.py

# 2. Analiza wyników
python simple_kayak_extractor.py kayak_text_data/txt_session_[timestamp]

# 3. Excel: Sortuj po cenie → TOP 10 najlepszych ofert
```

### Scenariusz 2: Porównanie konkretnych dat

```bash
# 1. Przygotuj Excel z wybranymi datami
# flights_list.xlsx: 2025-10-22, 2025-10-25, 2025-10-28

# 2. Scraping
python kayak_excel_scraper.py

# 3. Analiza
python simple_kayak_extractor.py kayak_excel_data/excel_session_[timestamp]

# 4. Excel: Pivot table - Data wylotu vs Średnia cena
```

### Scenariusz 3: Monitoring cen w czasie

```bash
# 1. Rolling mode przez tydzień
python scrap_only_extended.py  # z rolling_mode: true

# 2. Codziennie rano analiza
python simple_kayak_extractor.py rolling_mode

# 3. Excel: Track najniższej ceny + wykres trendu
```

## 🎨 Customizacja Extractora

### Modyfikacja wzorców cen

Edytuj `simple_kayak_extractor.py`:

```python
price_patterns = [
    r'(\d+(?:\s+\d{3})*)\s*zł\s*/\s*osoba\s+(\d+(?:\s+\d{3})*)\s*zł\s*łącznie',
    r'(\d+(?:\s+\d{3})*)\s*PLN\s*/\s*person\s+(\d+(?:\s+\d{3})*)\s*PLN\s*total',  # English
    # Dodaj własne wzorce...
]
```

### Dodatkowe kolumny w Excel

```python
# W funkcji export_to_excel dodaj:
'Stosunek cena/czas': offer.total_price / self.parse_duration_to_minutes(offer.total_travel_time_outbound),
'Weekend wylot': 'TAK' if datetime.strptime(offer.departure_date, '%Y-%m-%d').weekday() >= 5 else 'NIE',
'Długość pobytu': self.calculate_stay_length(offer.departure_date, offer.return_date),
```

### Filtrowanie ofert przed eksportem

```python
# Dodaj w process_session_folder:
if offer.total_price > 15000:  # Odrzuć za drogie
    continue
if offer.stops_outbound > 2:   # Odrzuć z za dużo przesiadek
    continue
```

## 📋 Checklist jakości danych

### ✅ Sprawdź przed analizą:

- **Kompletność cen:** Wszystkie pliki mają cenę?
- **Logiczne ceny:** Brak cen 0 PLN lub 999,999 PLN?
- **Czasy lotów:** Realistyczne czasy (nie 1h WAW→ICN)?
- **Przesiadki:** Kody lotnisk to poprawne IATA (3 znaki)?
- **Daty:** Wszystkie w poprawnym formacie YYYY-MM-DD?

### 🔧 Automatyczna walidacja:

```python
# Dodaj do kodu walidacje:
def validate_offer(self, offer):
    if not (1000 <= offer.total_price <= 50000):
        return False
    if offer.departure_date >= offer.return_date:
        return False
    if len(offer.departure_airport) != 3:
        return False
    return True
```

## 🚀 Przydatne skrypty

### Szybka analiza sesji

```bash
#!/bin/bash
# quick_analysis.sh

LATEST_SESSION=$(ls -t kayak_text_data/ | head -n 1)
echo "📊 Analizuję najnowszą sesję: $LATEST_SESSION"

python simple_kayak_extractor.py "kayak_text_data/$LATEST_SESSION"

echo "✅ Gotowe! Otwierając Excel..."
# Windows:
# start kayak_offers_*.xlsx
# macOS:
# open kayak_offers_*.xlsx
# Linux:
# xdg-open kayak_offers_*.xlsx
```

### Batch processing wielu sesji

```python
#!/usr/bin/env python3
# batch_extract.py

import os
from pathlib import Path
import subprocess

base_dir = Path("kayak_text_data")
sessions = [d for d in base_dir.iterdir() if d.is_dir()]

for session in sessions:
    print(f"🔄 Przetwarzanie: {session.name}")
    result = subprocess.run([
        "python", "simple_kayak_extractor.py", str(session)
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {session.name} - OK")
    else:
        print(f"❌ {session.name} - ERROR")
```

### Monitoring nowych plików

```python
#!/usr/bin/env python3
# auto_extract.py - monitoruje folder i automatycznie ekstraktuje nowe sesje

import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class NewSessionHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory and "session_" in event.src_path:
            print(f"🆕 Nowa sesja: {event.src_path}")
            time.sleep(10)  # Czekaj na zakończenie scrapingu
            os.system(f"python simple_kayak_extractor.py {event.src_path}")

observer = Observer()
observer.schedule(NewSessionHandler(), "kayak_text_data", recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
```

## 📚 Zaawansowane analizy

### Power BI / Tableau integration

```python
# Export do formatu kompatybilnego z narzędziami BI
def export_for_powerbi(self, offers, output_file="kayak_powerbi.csv"):
    data = []
    for offer in offers:
        data.append({
            'Date': datetime.now().isoformat(),
            'FlightDate': offer.departure_date,
            'ReturnDate': offer.return_date,
            'Airline': offer.airline_filter,
            'Price': offer.total_price,
            'PricePerPerson': offer.price_per_person,
            'OutboundStops': offer.stops_outbound,
            'ReturnStops': offer.stops_return,
            'TotalTravelTime': self.duration_to_minutes(offer.total_travel_time_outbound),
            'IsWeekend': datetime.strptime(offer.departure_date, '%Y-%m-%d').weekday() >= 5,
            'StayLength': (datetime.strptime(offer.return_date, '%Y-%m-%d') - 
                          datetime.strptime(offer.departure_date, '%Y-%m-%d')).days
        })
    
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
```

### Machine Learning - predykcja cen

```python
# Prosty model predykcji
from sklearn.linear_model import LinearRegression
import numpy as np

def predict_prices(historical_data):
    # Features: day_of_week, stay_length, stops, airline_encoded
    features = []
    prices = []
    
    for offer in historical_data:
        dep_date = datetime.strptime(offer.departure_date, '%Y-%m-%d')
        stay_length = (datetime.strptime(offer.return_date, '%Y-%m-%d') - dep_date).days
        
        features.append([
            dep_date.weekday(),  # 0=Monday, 6=Sunday
            stay_length,
            offer.stops_outbound + offer.stops_return,
            hash(offer.airline_filter) % 100  # Simple airline encoding
        ])
        prices.append(offer.total_price)
    
    model = LinearRegression()
    model.fit(features, prices)
    
    return model
```

---

**🎯 Podsumowanie:**

Data Extractor to potężne narzędzie do analizy danych lotów. Kombinuje automatyczne parsowanie z elastycznym eksportem do Excel, umożliwiając szybkie identyfikowanie najlepszych ofert i trendów cenowych.

**Najważniejsze zalety:**
- ⚡ **Szybkość** - analiza setek plików w minuty
- 🎯 **Precyzja** - inteligentne parsowanie wzorców Kayak  
- 📊 **Elastyczność** - eksport do Excel z pełną analizą
- 🔧 **Customizacja** - łatwa modyfikacja i rozszerzanie

**Typowy workflow:**
1. **Scraping** → setki plików .txt
2. **Extraction** → jeden przejrzysty Excel  
3. **Analiza** → najlepsze oferty i trendy
4. **Decyzja** → świadomy wybór lotu ✈️