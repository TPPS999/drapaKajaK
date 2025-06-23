# 🛫 Kayak Flight Scraper

Inteligentny scraper lotów z Kayak.pl umożliwiający monitorowanie cen i automatyczne wyszukiwanie najlepszych ofert.

## 📋 Spis treści
- [Funkcje](#-funkcje)
- [Wymagania](#-wymagania)
- [Instalacja](#-instalacja)
- [Konfiguracja](#-konfiguracja)
- [Użytkowanie](#-użytkowanie)
- [Struktura plików](#-struktura-plików)
- [Rozwiązywanie problemów](#-rozwiązywanie-problemów)

## ✨ Funkcje

- **Dwa tryby pracy:**
  - **Extended Mode** - wszystkie kombinacje dat w zadanym zakresie
  - **Excel Mode** - konkretne loty z pliku Excel
- **Rolling Mode** - ciągły monitoring w kółko
- **Inteligentne opóźnienia** - losowe czasy między zapytaniami
- **Obsługa wielu linii lotniczych** - LOT, Turkish, Emirates, Qatar i więcej
- **Bezpieczny scraping** - headless Chrome z losowymi User-Agent
- **Szczegółowe logowanie** - pełna kontrola nad procesem
- **Export wyników** - pliki tekstowe + JSON summary
- **🆕 Data Extractor** - automatyczne wyciąganie najlepszych ofert z plików tekstowych do Excel

## 🔧 Wymagania

### Software:
- Python 3.8+
- Chrome/Chromium browser
- ChromeDriver (automatycznie zarządzany)

### Wymagane biblioteki:
```bash
selenium
pandas
openpyxl
```

## 🚀 Instalacja

1. **Klonowanie repozytorium:**
```bash
git clone [url-repozytorium]
cd kayak-flight-scraper
```

2. **Instalacja zależności:**
```bash
pip install selenium pandas openpyxl
```

3. **Automatyczna instalacja ChromeDriver:**
```bash
pip install webdriver-manager
```

Lub pobierz ChromeDriver ręcznie z [chromdriver.chromium.org](https://chromedriver.chromium.org) i dodaj do PATH.

## ⚙️ Konfiguracja

### Extended Mode (wszystkie kombinacje)

Edytuj plik `config_extended.json`:

```json
{
  "scraping_config": {
    "origin": "WAW",              // Lotnisko wylotu (kod IATA)
    "destination": "ICN",         // Lotnisko docelowe (kod IATA) 
    "earliest_departure": "2025-10-05",  // Najwcześniejszy wylot
    "latest_return": "2025-11-15",       // Najpóźniejszy powrót
    "min_days": 19,               // Minimalna długość pobytu
    "max_days": 24,               // Maksymalna długość pobytu
    "passengers": 2,              // Liczba pasażerów (1-4)
    "selected_airlines": [        // Wybrane linie lotnicze
      "LOT", "Turkish", "Emirates", "Qatar", "China_Air"
    ],
    "delay_between_requests": [25, 45],   // Opóźnienie [min, max] sekund
    "rolling_mode": false,        // Tryb ciągły
    "rolling_break_minutes": [30, 60]    // Przerwa między rundami
  }
}
```

### Excel Mode (konkretne loty)

Utwórz plik `flights_list.xlsx` z kolumnami:

| Lotnisko wylotu | Lotnisko docelowe | Filtr linii | Data wylotu | Data powrotu |
|-----------------|-------------------|-------------|-------------|--------------|
| WAW             | ICN               | Turkish     | 2025-10-22  | 2025-11-10   |
| WAW             | ICN               | Qatar       | 2025-10-21  | 2025-11-12   |
| WAW             | ICN               | Emirates    | 2025-10-05  | 2025-10-24   |

Następnie edytuj `excel_config.json`:

```json
{
  "scraping_config": {
    "passengers": 2,
    "delay_between_requests": [20, 35],
    "randomize_order": true,
    "rolling_break_minutes": [30, 60]
  }
}
```

### Dostępne linie lotnicze

Obsługiwane filtry (nie zmieniaj bez znajomości URL encoding):

- **LOT** - LOT Polish Airlines
- **Turkish** - Turkish Airlines + Multi
- **Emirates** - Emirates
- **Qatar** - Qatar Airways
- **China_Air** - Air China
- **Lufthansa** - Lufthansa + Multi
- **KLM** - KLM + Multi
- **AirFrance** - Air France + Multi
- **Swiss** - Swiss
- **Austrian** - Austrian Airlines
- **Finnair** - Finnair
- **SAS** - SAS
- **Korean** - Korean Air
- **Asiana** - Asiana Airlines
- **Etihad** - Etihad Airways

## 🎯 Użytkowanie

### Extended Mode (wszystkie kombinacje)

```bash
python scrap_only_extended.py
```

Ten tryb sprawdzi wszystkie kombinacje dat w zadanym zakresie dla wybranych linii lotniczych.

**Przykład:** Dla zakresu 5 dni, 3 linii i długości pobytu 2-4 dni = ~45 zapytań

### Excel Mode (konkretne loty)

```bash
python kayak_excel_scraper.py
```

Ten tryb sprawdzi tylko konkretne loty z pliku Excel.

**Przykład:** 10 wierszy w Excel = 10 zapytań

### Rolling Mode (ciągły monitoring)

W konfiguracji ustaw `"rolling_mode": true` i uruchom dowolny skrypt.

Program będzie działał w kółko z przerwami między rundami. Zatrzymanie: **Ctrl+C**

### 🆕 Data Extractor (wyciągnij oferty do Excel)

Po wykonaniu scrapingu użyj extractora do wyciągnięcia najlepszych ofert:

```bash
python simple_kayak_extractor.py kayak_text_data/txt_session_20250623_143022
```

Extractor automatycznie:
- Znajdzie pierwszą (najtańszą) ofertę w każdym pliku .txt
- Wyciągnie szczegółowe informacje o lotach (czasy, przesiadki, lotniska)
- Zapisze wszystko w przejrzystym pliku Excel
- Pokaże statystyki cen i ranking ofert

## 📁 Struktura plików

Po uruchomieniu zostanie utworzona następująca struktura:

```
kayak_text_data/                    # Extended mode
├── txt_session_20250623_143022/    # Folder sesji
│   ├── WAW-ICN_Turkish_2025-10-22_2025-11-10_xxx.txt
│   ├── WAW-ICN_Qatar_2025-10-21_2025-11-12_xxx.txt
│   └── session_summary.json       # Podsumowanie sesji
│
kayak_excel_data/                   # Excel mode
├── excel_session_20250623_143500/
│   ├── WAW-ICN_Turkish_2025-10-22_2025-11-10_xxx.txt
│   └── session_summary.json
│
└── rolling_mode/                   # Rolling mode (wszystko w jednym folderze)
    ├── R001_WAW-ICN_Turkish_xxx.txt   # R001 = runda 1
    ├── R002_WAW-ICN_Qatar_xxx.txt     # R002 = runda 2
    └── round_001_summary.json

# Pliki wygenerowane przez Data Extractor:
kayak_offers_20250623_145000.xlsx  # Wyciągnięte oferty w Excel
```

### Format pliku wyników

Każdy plik `.txt` zawiera:

```
URL: https://www.kayak.pl/flights/WAW-ICN/2025-10-22/2025-11-10/2adults?sort=price_a&fs=airlines%3DTK%3Bbfc%3D1
Title: Flights from Warsaw to Seoul | Kayak
Timestamp: 20250623_143022_123
Round: Single
Route: WAW → ICN
Request: Turkish Airlines + Multi | 2025-10-22 → 2025-11-10 | 2 pax
Airline Filter: fs=airlines%3DTK%3Bbfc%3D1
Duration: 19 days
================================================================================

[CAŁY TEKST ZE STRONY KAYAK]
```

### 🆕 Format pliku Excel (Data Extractor)

Plik Excel zawiera szczegółowe kolumny:

| Kolumna | Opis |
|---------|------|
| **Podstawowe** |
| Plik | Nazwa oryginalnego pliku .txt |
| Filtr linii | Linia lotnicza z konfiguracji |
| Data wylotu/powrotu | Daty podróży |
| Cena łączna/za osobę | Ceny w PLN |
| **Loty** |
| Linie lotnicze tam/powrót | Nazwy przewoźników |
| Lotnisko wylotu/docelowe | Kody IATA (WAW/ICN) |
| Wylot/Przylot tam/powrót | Godziny lotów |
| **Czasy** |
| Czas podróży (total) | Całkowity czas z przesiadkami |
| Czas lotu (bez przesiadek) | Rzeczywisty czas w powietrzu |
| **Przesiadki (tam i powrót)** |
| Przesiadki | Liczba przesiadek (0-3) |
| Przesiadka 1/2/3 lotnisko | Kody lotnisk przesiadek |
| Przesiadka 1/2/3 czas | Czas oczekiwania na przesiadkę |

## 🛠️ Rozwiązywanie problemów

### Częste problemy

1. **ChromeDriver Error**
   ```bash
   pip install webdriver-manager
   ```

2. **Brak pliku konfiguracji**
   - Program automatycznie utworzy przykładowy config
   - Edytuj i uruchom ponownie

3. **Błąd "Brak lotów do sprawdzenia"**
   - Sprawdź format dat w Excel (YYYY-MM-DD)
   - Upewnij się, że kody lotnisk mają 3 znaki (WAW, ICN)
   - Sprawdź czy nazwy linii są poprawne

4. **Timeout errors**
   - Zwiększ opóźnienia w konfiguracji
   - Sprawdź połączenie internetowe

### Parametry dostrajania

**Dla wolniejszego internetu:**
```json
"delay_between_requests": [40, 60]
```

**Dla szybszego scrapowania (ryzykowne):**
```json
"delay_between_requests": [15, 25]
```

**Rolling mode - częstsze rundy:**
```json
"rolling_break_minutes": [15, 30]
```

## 📊 Statystyki i monitorowanie

Program wyświetla na bieżąco:

- **Progress** - ile zapytań wykonano/pozostało
- **Skuteczność** - procent udanych zapytań
- **Zebranych znaków** - ilość danych
- **Czas trwania** - w rolling mode

### Przykładowe podsumowanie:

```
🏁 ============================================================
🎉 SESJA ZAKOŃCZONA!
📊 WYNIKI:
   ✅ Sukces: 42
   ❌ Błędy: 3
   📈 Skuteczność: 93.3%
   📝 Zebranych znaków: 2,847,294
🛫 Trasa: WAW→ICN
📁 Dane zapisane w: kayak_text_data/txt_session_20250623_143022
============================================================
```

## 🔄 Kompletny workflow

### Standardowa procedura (Extended Mode):

```bash
# 1. Konfiguracja
# Edytuj config_extended.json (trasa, daty, linie)

# 2. Scraping
python scrap_only_extended.py
# Wynik: kayak_text_data/txt_session_20250623_143022/ z plikami .txt

# 3. Analiza danych
python simple_kayak_extractor.py kayak_text_data/txt_session_20250623_143022
# Wynik: kayak_offers_20250623_145000.xlsx z przejrzystą tabelą

# 4. Analiza w Excel
# Otwórz Excel, sortuj po cenie, filtruj po liniach, etc.
```

### Procedura dla konkretnych lotów (Excel Mode):

```bash
# 1. Przygotuj listę lotów
# Edytuj flights_list.xlsx (konkretne daty i trasy)

# 2. Scraping
python kayak_excel_scraper.py
# Wynik: kayak_excel_data/excel_session_20250623_143500/ z plikami .txt

# 3. Analiza danych
python simple_kayak_extractor.py kayak_excel_data/excel_session_20250623_143500
# Wynik: kayak_offers_20250623_145000.xlsx
```

### Rolling Mode (ciągły monitoring):

```bash
# 1. Konfiguracja
# W config_extended.json ustaw "rolling_mode": true

# 2. Długoterminowy monitoring
python scrap_only_extended.py
# Program działa w kółko, zatrzymanie: Ctrl+C
# Wszystkie pliki w rolling_mode/

# 3. Okresowa analiza
python simple_kayak_extractor.py rolling_mode
# Excel z najnowszymi danymi
```

- **Headless Chrome** - niewidoczne działanie
- **Losowe User-Agent** - imitacja prawdziwych użytkowników  
- **Inteligentne opóźnienia** - unikanie wykrycia
- **Rotacja żądań** - losowa kolejność
- **Graceful handling** - obsługa błędów bez crashy

## 📝 Notatki

- **Szacowany czas:** ~30-45s na zapytanie (z opóźnieniami)
- **Zalecane użycie:** maksymalnie 50-100 zapytań na sesję
- **Rolling mode:** idealny do długoterminowego monitorowania
- **Excel mode:** najlepszy do sprawdzania konkretnych dat

## 🚨 Ostrzeżenia

- Nie uruchamiaj zbyt wielu sesji równolegle
- Używaj rozsądnych opóźnień (min. 20s)
- W razie problemów zwiększ czasy oczekiwania
- Rolling mode może działać całymi dniami - monitoruj zużycie zasobów

---

**Autor:** [Twoje dane]  
**Wersja:** 2.0  
**Data:** Czerwiec 2025