# 🛫 Kayak Flight Scraper

Zaawansowany system scrapingu i analizy cen lotów z Kayak.pl z pełną automatyzacją i analizą danych.

## 📋 Spis treści
- [Funkcje](#-funkcje)
- [Wymagania](#-wymagania)
- [Instalacja](#-instalacja)
- [Szybki start](#-szybki-start)
- [Komponenty systemu](#-komponenty-systemu)
- [Konfiguracja](#-konfiguracja)
- [Użytkowanie](#-użytkowanie)
- [Analiza danych](#-analiza-danych)
- [Rozwiązywanie problemów](#-rozwiązywanie-problemów)

## ✨ Funkcje

### 🎯 Zaawansowany scraping
- **Extended Mode** - wszystkie kombinacje dat w zadanym zakresie
- **Excel Mode** - konkretne loty z pliku Excel  
- **Rolling Mode** - ciągły monitoring 24/7
- **Stealth Mode** - zaawansowane techniki unikania wykrycia

### 🔧 Inteligentne narzędzia
- **Multi-airline support** - 15+ linii lotniczych (LOT, Turkish, Emirates, Qatar, itp.)
- **Smart delays** - losowe opóźnienia między zapytaniami
- **Price extractor** - automatyczne wyciąganie cen z różnych formatów
- **Flight parser** - szczegółowa analiza tras, przesiadek i czasów

### 📊 Analiza i eksport
- **Data Extractor** - automatyczne wyciąganie najlepszych ofert do Excel
- **Szczegółowe raporty** - analiza przesiadek, czasów lotów, cen
- **Export do Excel** - przejrzyste tabele z sortowaniem i filtrami
- **Tracking cen** - monitoring zmian cen w czasie

### 🖥️ Graficzny interfejs
- **Flight Tool Complete** - kompletny GUI dla wszystkich funkcji
- **Real-time monitoring** - podgląd postępu na żywo

## 🔧 Wymagania

### Software
- **Python 3.8+**
- **Google Chrome** (najnowsza wersja)
- **ChromeDriver** (automatycznie zarządzany przez webdriver-manager)

### Biblioteki Python
```bash
# Podstawowe
selenium>=4.0.0
webdriver-manager>=3.8.0
pandas>=1.5.0
openpyxl>=3.0.0

# Dodatkowe 
requests>=2.28.0
beautifulsoup4>=4.11.0
plyer>=2.1.0  # powiadomienia
```

## 🚀 Szybki start

### 1. Instalacja
```bash
# Klonowanie projektu
git clone [url-repo]
cd kayak-flight-scraper

# Instalacja zależności
pip install -r requirements.txt
# LUB
pip install selenium webdriver-manager pandas openpyxl requests beautifulsoup4 plyer
```

### 2. Test systemu
```bash
# Uruchom GUI (automatycznie sprawdzi komponenty)
python FlightTool_Complete.py
```

### 3. Pierwszy scraping (Extended Mode)
```bash
# Scraping wszystkich kombinacji WAW→ICN październik/listopad
python scrap_only_extended.py

# Analiza wyników do Excel
python simple_kayak_extractor.py kayak_text_data/txt_session_[timestamp]
```

### 4. Konkretne loty (Excel Mode)
```bash
# Tworzy przykładowy Excel z lotami
python kayak_excel_scraper.py

# Edytuj flights_list.xlsx i uruchom ponownie
python kayak_excel_scraper.py

# Analiza do Excel
python simple_kayak_extractor.py kayak_excel_data/excel_session_[timestamp]
```

## 🧩 Komponenty systemu

### 1. **Extended Scraper** (`scrap_only_extended.py`)
Sprawdza wszystkie kombinacje dat w zadanym zakresie.
- **Konfiguracja**: `config_extended.json`
- **Output**: `kayak_text_data/txt_session_[timestamp]/`
- **Funkcje**: rolling mode, smart delays, multi-airline

### 2. **Excel Scraper** (`kayak_excel_scraper.py`)
Sprawdza konkretne loty z pliku Excel.
- **Input**: `flights_list.xlsx`
- **Konfiguracja**: `excel_config.json`
- **Output**: `kayak_excel_data/excel_session_[timestamp]/`

### 3. **Data Extractor** (`simple_kayak_extractor.py`)
Wyciąga najlepsze oferty z plików tekstowych do Excel.
- **Input**: Katalog z plikami .txt
- **Output**: `kayak_offers_[timestamp].xlsx`
- **Funkcje**: parsing przesiadek, analiza czasów, ranking cen

### 4. **Stealth Scraper** (`flight_monitor_stealth.py`)
Zaawansowany scraper z technikami stealth.
- **Funkcje**: rotating user agents, advanced delays, cookie handling

### 5. **GUI Tool** (`FlightTool_Complete.py`)
Kompletny interfejs graficzny.
- **Funkcje**: wszystkie scrapery w jednym miejscu
- **Auto-install**: automatyczna instalacja komponentów

## ⚙️ Konfiguracja

### Extended Mode (`config_extended.json`)
```json
{
  "scraping_config": {
    "origin": "WAW",
    "destination": "ICN", 
    "earliest_departure": "2025-10-05",
    "latest_return": "2025-11-15",
    "min_days": 19,
    "max_days": 24,
    "passengers": 2,
    "selected_airlines": ["Turkish", "Qatar", "Emirates", "China_Air"],
    "delay_between_requests": [25, 45],
    "rolling_mode": false,
    "rolling_break_minutes": [30, 60]
  }
}
```

### Excel Mode (`flights_list.xlsx`)
| Lotnisko wylotu | Lotnisko docelowe | Filtr linii | Data wylotu | Data powrotu |
|-----------------|-------------------|-------------|-------------|--------------|
| WAW             | ICN               | Turkish     | 2025-10-22  | 2025-11-10   |
| WAW             | ICN               | Qatar       | 2025-10-21  | 2025-11-12   |
| WAW             | ICN               | Emirates    | 2025-10-05  | 2025-10-24   |

### Obsługiwane linie lotnicze
- **Zatokowe**: Turkish, Emirates, Qatar, Etihad
- **Azjatyckie**: China_Air, Korean, Asiana  
- **Europejskie**: LOT, Lufthansa, KLM, Air_France, Swiss, Austrian
- **Nordyckie**: Finnair, SAS

## 🎯 Użytkowanie

### Scenariusz 1: Poszukiwanie najlepszej oferty
```bash
# 1. Scraping wszystkich kombinacji dla trasy WAW→ICN
python scrap_only_extended.py

# 2. Analiza wyników - automatycznie znajdzie najtańsze oferty
python simple_kayak_extractor.py kayak_text_data/txt_session_[timestamp]

# 3. Otwórz Excel i sortuj po cenie → TOP oferty
```

### Scenariusz 2: Konkretne daty
```bash
# 1. Przygotuj Excel z wybranymi datami
# 2. Scraping
python kayak_excel_scraper.py

# 3. Analiza
python simple_kayak_extractor.py kayak_excel_data/excel_session_[timestamp]
```

### Scenariusz 3: Ciągły monitoring (Rolling Mode)
```bash
# 1. W config_extended.json ustaw "rolling_mode": true
# 2. Uruchom długoterminowy monitoring
python scrap_only_extended.py
# Zatrzymanie: Ctrl+C

# 3. Okresowa analiza
python simple_kayak_extractor.py rolling_mode
```

### Scenariusz 4: GUI (najłatwiejszy)
```bash
# Uruchom kompletny interfejs graficzny
python FlightTool_Complete.py
```

## 📊 Analiza danych

### Struktura pliku Excel (Data Extractor)

**Podstawowe kolumny:**
- Plik źródłowy, filtr linii, daty
- Cena łączna i za osobę (PLN)
- Linie lotnicze tam/powrót

**Szczegółowe dane lotów:**
- Lotniska wylotu/docelowe (kody IATA)
- Czasy wylotu/przylotu
- Czas podróży total vs rzeczywisty czas lotu
- Przesiadki (do 3 na kierunek): lotniska + czasy oczekiwania

**Przykład analizy w Excel:**
```
Sortowanie po cenie → znajdź najtańsze oferty
Filtrowanie po linii → porównaj przewoźników
Filtrowanie po przesiadkach → loty direct vs przesiadkowe
Pivot table → średnie ceny według dat/linii
```

### Statystyki przykładowe
```
📊 WYNIKI SESJI:
✅ Sukces: 42 ofert
❌ Błędy: 3
📈 Skuteczność: 93.3%
💰 Najniższa cena: 6,240 PLN
💰 Najwyższa cena: 12,450 PLN  
💰 Średnia cena: 8,127 PLN
🛫 Trasa: WAW→ICN
```

## 🔄 Workflow

### Typowy proces pracy:
1. **Konfiguracja** → Edytuj config_extended.json lub flights_list.xlsx
2. **Scraping** → python scrap_only_extended.py (lub excel_scraper.py)
3. **Analiza** → python simple_kayak_extractor.py [katalog_sesji]
4. **Excel** → Otwórz wygenerowany plik, sortuj, filtruj, analizuj

### Szacowane czasy:
- **30-45s** na jedno zapytanie (z opóźnieniami)
- **100 zapytań** = ~1-1.5 godziny
- **Rolling mode** = ciągły (zatrzymanie Ctrl+C)

## 📁 Struktura plików

```
kayak-flight-scraper/
├── scrap_only_extended.py          # Extended scraper
├── kayak_excel_scraper.py          # Excel scraper  
├── simple_kayak_extractor.py       # Data extractor
├── FlightTool_Complete.py          # GUI
├── flight_monitor_stealth.py       # Stealth scraper
├── config_extended.json            # Konfiguracja Extended
├── excel_config.json               # Konfiguracja Excel
├── flights_list.xlsx               # Lista lotów (Excel mode)
├── kayak_text_data/                # Wyniki Extended mode
│   ├── txt_session_20250623_143022/
│   └── rolling_mode/
├── kayak_excel_data/               # Wyniki Excel mode
└── kayak_offers_[timestamp].xlsx   # Wyniki Data Extractor
```

## 🛠️ Rozwiązywanie problemów

### Częste problemy

**ChromeDriver Error**
```bash
pip install --upgrade webdriver-manager
```

**Timeout errors**
```json
"delay_between_requests": [40, 60]  // zwiększ opóźnienia
```

**Brak cen w wynikach**
- Sprawdź debug pliki w `D:\flightmonitor\debug`
- Kayak może wykrywać bot - zwiększ opóźnienia
- Spróbuj ponownie za kilka godzin

**Excel Mode - błędne kolumny**
- Kolumny muszą być dokładnie: `Lotnisko wylotu`, `Lotnisko docelowe`, `Filtr linii`, `Data wylotu`, `Data powrotu`
- Format dat: `YYYY-MM-DD`
- Kody lotnisk: 3 znaki (WAW, ICN)

### Tuning wydajności

**Dla szybszego scrapingu (ryzykowne):**
```json
"delay_between_requests": [15, 25]
```

**Dla stabilniejszego działania:**
```json
"delay_between_requests": [45, 75]
```

**Rolling mode - częstsze sprawdzenia:**
```json
"rolling_break_minutes": [15, 30]
```

## 🚨 Ważne uwagi

- **Szanuj zasoby**: Kayak ma mechanizmy anty-bot
- **Rozsądne limity**: Max 50-100 zapytań na sesję
- **Opóźnienia**: Minimum 20s między zapytaniami
- **Rolling mode**: Idealny do długoterminowego monitorowania
- **Backup danych**: Regularnie kopiuj wyniki

## 📝 Przykłady konfiguracji

### Weekend w Londynie
```json
{
  "origin": "WAW", "destination": "LHR",
  "min_days": 2, "max_days": 4,
  "selected_airlines": ["LOT", "Lufthansa"],
  "passengers": 2
}
```

### Długa podróż do Azji  
```json
{
  "origin": "WAW", "destination": "ICN",
  "min_days": 19, "max_days": 24,
  "selected_airlines": ["Turkish", "Emirates", "Qatar"],
  "rolling_mode": true
}
```

---

**Projekt**: Kayak Flight Scraper  
**Wersja**: 2.0  
**Status**: Aktywnie rozwijany  
**Licencja**: Do użytku osobistego