# 🛫 drapaKajaK - Flight Price Scraper

Zaawansowany system scrapingu i analizy cen lotów z Kayak.pl z **kompletnym interfejsem graficznym** i pełną automatyzacją.

## 🚀 Ultra-szybki start (2 minuty)

### 📥 Pobierz projekt (wybierz opcję):

#### Opcja A: Git (jeśli masz Git zainstalowany)
```bash
git clone https://github.com/TPPS999/drapaKajaK.git
cd drapaKajaK
```

#### Opcja B: Bez Git (pobierz jako ZIP)
1. **Idź na:** https://github.com/TPPS999/drapaKajaK
2. **Kliknij:** `🟢 Code` → `Download ZIP`
3. **Rozpakuj** ZIP do folderu `drapaKajaK`
4. **Otwórz terminal/cmd** w tym folderze

#### Opcja C: Zainstaluj Git (jednorazowo)
- **Windows:** https://git-scm.com/download/win
- **macOS:** `brew install git` lub https://git-scm.com/download/mac
- **Linux:** `sudo apt install git` (Ubuntu/Debian)

### 🚀 Ultra-prosty start - NOWY SPOSÓB! ⚡

#### Windows - Jedno kliknięcie!
```bash
# Automatycznie sprawdza/tworzy venv i uruchamia:
run.bat              # Uruchom GUI (domyślnie)
run.bat test         # Test systemu
run.bat scraper      # Extended scraper
run.bat excel        # Excel scraper
run.bat gui          # GUI (jawnie)

# Lub stare skrypty (też z auto-venv):
run_test.bat         # Test systemu
run_scraper.bat      # Extended scraper
```

#### Linux/macOS - Jedno polecenie!
```bash
# Nadaj uprawnienia (jednorazowo):
chmod +x run.sh run_test.sh run_scraper.sh

# Automatycznie sprawdza/tworzy venv i uruchamia:
./run.sh             # Uruchom GUI (domyślnie)
./run.sh test        # Test systemu
./run.sh scraper     # Extended scraper
./run.sh excel       # Excel scraper
./run.sh gui         # GUI (jawnie)

# Lub stare skrypty (też z auto-venv):
./run_test.sh        # Test systemu
./run_scraper.sh     # Extended scraper
```

**To wszystko!**
- ✅ **Pierwsze uruchomienie** - automatycznie tworzy venv
- ✅ **Kolejne uruchomienia** - używa istniejącego venv
- ✅ **Zero konfiguracji** - działa od razu! 🎉

---

## 📋 Spis treści
- [Interfejs GUI](#-interfejs-gui---flight-tool)
- [Funkcje](#-funkcje)
- [Pierwszy scraping](#-pierwszy-scraping---krok-po-kroku)
- [Wymagania](#-wymagania)
- [Scenariusze użycia](#-scenariusze-użycia)
- [Analiza danych](#-analiza-danych)
- [Rozwiązywanie problemów](#-rozwiązywanie-problemów)

## 🖥️ Interfejs GUI - Flight Tool

Po uruchomieniu `setup_and_run.bat` automatycznie otwiera się **Flight Tool** - kompletny interfejs graficzny z czterema zakładkami:

### 🎯 Główne zakładki:

| Zakładka | Funkcja | Opis |
|----------|---------|------|
| **Extended Scraper** | 🔄 Wszystkie kombinacje | Sprawdza wszystkie daty/linie w zadanym zakresie |
| **Excel Scraper** | 📋 Konkretne loty | Sprawdza tylko wybrane loty z pliku Excel |
| **Data Extractor** | 📊 Analiza wyników | Wyciąga najlepsze oferty do Excel |
| **Test** | 🧪 Sprawdzenie systemu | Testuje czy wszystko działa |

### 🖱️ Wszystko przez kliknięcia:
- ✅ **Bez edycji JSON** - konfiguracja przez checkboxy i pola
- ✅ **Logi na żywo** - widzisz postęp scrapingu w czasie rzeczywistym  
- ✅ **Stop/Start** - pełna kontrola nad procesem
- ✅ **Automatyczna instalacja** - `setup_and_run.bat` robi wszystko

## ✨ Funkcje

### 🎯 Zaawansowany scraping
- **Extended Mode** - wszystkie kombinacje dat w zadanym zakresie
- **Excel Mode** - konkretne loty z pliku Excel  
- **Rolling Mode** - ciągły monitoring 24/7 (przez GUI)
- **Smart delays** - inteligentne opóźnienia między zapytaniami

### 🔧 15+ linii lotniczych (wybór przez checkboxy)
- **Zatokowe**: Turkish, Emirates, Qatar, Etihad
- **Azjatyckie**: Air China, Korean Air, Asiana, ANA, Singapore
- **Europejskie**: LOT, Lufthansa, KLM, Air France, Swiss, Austrian
- **Pozostałe**: British Airways, Finnair, SAS, Cathay Pacific

### 📊 Inteligentna analiza
- **Data Extractor** - automatyczne wyciąganie najlepszych ofert
- **Excel eksport** - szczegółowe tabele z analizą przesiadek, czasów, cen
- **Sortowanie i ranking** - znajdź najtańsze opcje automatycznie
- **Statystyki tras** - porównanie średnich cen według linii

## 🎯 Pierwszy scraping - krok po kroku

### 1. **Uruchomienie** (jednorazowo)
```bash
git clone https://github.com/TPPS999/drapaKajaK.git
cd drapaKajaK

# Utwórz środowisko wirtualne (venv)
python setup_venv.py

# Aktywuj venv
activate_venv.bat         # Windows
source activate_venv.sh   # Linux/macOS
```

### 2. **Test systemu** (zalecane)
- Zakładka **"Test"** → **"Quick ChromeDriver Test"**
- Sprawdź czy wyświetla: `✓ ChromeDriver test PASSED`

### 3. **Twój pierwszy scraping**
- Zakładka **"Extended Scraper"**
- Zostaw domyślne: **WAW → ICN** (Warszawa → Seul)
- Daty: **październik/listopad 2025**
- Zaznacz **2-3 linie** (np. Turkish, Qatar, Emirates)
- Kliknij **"START SCRAPING"**

### 4. **Obserwuj postęp**
- Logi pokazują się na żywo
- Widzisz ile zapytań zostało: `[15/120] Turkish Airlines...`
- Możesz zatrzymać w każdej chwili: **"STOP SCRAPING"**

### 5. **Analiza wyników**
- Zakładka **"Data Extractor"**
- **"Browse"** → wybierz `kayak_text_data/txt_session_[data]`
- **"Preview Data"** → zobacz ile plików znaleziono
- **"EXTRACT TO EXCEL"** → tworzy analizę

### 6. **🎉 Gotowe!**
- Automatycznie otwiera się Excel z najlepszymi ofertami
- Sortowanie po cenie, analiza przesiadek, porównanie tras

## 🔧 Wymagania

### Automatycznie instalowane przez setup_venv.py:
- ✅ **Środowisko wirtualne (venv)** - izolowane od systemu
- ✅ **Wszystkie biblioteki Python** - selenium, pandas, openpyxl, webdriver-manager, requests, beautifulsoup4
- ✅ **ChromeDriver** - pobierany automatycznie przy pierwszym uruchomieniu
- ✅ **Skrypty pomocnicze** - activate_venv.bat/sh, run_test.bat/sh, run_scraper.bat/sh

### Wymagania systemowe (musisz zainstalować ręcznie):
- **Python 3.7+** z [python.org](https://python.org) - upewnij się, że jest w PATH
- **Google Chrome** z [chrome.google.com](https://chrome.google.com)

### Zalety środowiska wirtualnego (venv):
- 🔒 **Izolacja** - nie psuje systemowego Pythona
- 🧹 **Czystość** - łatwe usunięcie (usuń folder venv/)
- 🔧 **Portable** - działa tak samo na Windows/Linux/macOS
- ⚡ **Fix Unicode** - automatycznie obsługuje polskie znaki (Windows)

**Reszta dzieje się automatycznie!** 🚀

## 🎯 Scenariusze użycia

### Scenariusz 1: Znajdź najlepszą ofertę (Extended Mode)
```
GUI → Extended Scraper → START SCRAPING
↓ (automatycznie sprawdza wszystkie kombinacje)
GUI → Data Extractor → EXTRACT TO EXCEL  
↓ (Excel z ranking najlepszych ofert)
🎯 Masz TOP oferty posortowane po cenie!
```

### Scenariusz 2: Konkretne loty (Excel Mode)
```
GUI → Excel Scraper → Create Sample
↓ (tworzy flights_list.xlsx)
Edytuj Excel → dodaj swoje loty
↓
GUI → Excel Scraper → START EXCEL SCRAPING
↓
GUI → Data Extractor → analiza w Excel
```

### Scenariusz 3: Ciągły monitoring (Rolling Mode)
```
GUI → Extended Scraper → ☑️ Rolling mode
↓ (działa w kółko sprawdzając ceny)
START SCRAPING → działa 24/7
↓ (zatrzymanie: STOP SCRAPING)
Regularnie analizuj przez Data Extractor
```

### Scenariusz 4: Szybki test
```
GUI → Test → Quick ChromeDriver Test
↓ (sprawdza czy wszystko działa)
Extended Scraper → zaznacz 1 linię → krótki test
```

## 📊 Analiza danych w Excel

### Automatyczne kolumny w wyniku:
- **Podstawowe:** Cena łączna/za osobę, Data wylotu/powrotu, Linia
- **Lotniska:** Kody IATA (WAW, ICN), Trasa
- **Czasy:** Wylot/Przylot, Czas podróży total vs rzeczywisty lot
- **Przesiadki:** Do 3 na kierunek - lotniska + czasy oczekiwania
- **Ranking:** Automatyczne sortowanie po cenie

### Przykład rezultatu:
```
📊 Najlepsze oferty WAW→ICN:
1. Turkish Airlines: 6,240 PLN (1 przesiadka)
2. Qatar Airways: 7,180 PLN (1 przesiadka) 
3. Emirates: 8,450 PLN (1 przesiadka)
4. Air China: 9,120 PLN (2 przesiadki)
```

## 🛠️ Rozwiązywanie problemów

### 1. GUI nie otwiera się
```bash
# Windows:
activate_venv.bat
python FlightTool_Simple.py

# Linux/macOS:
source activate_venv.sh
python FlightTool_Simple.py

# LUB użyj gotowego skryptu (bez aktywacji):
run_test.bat         # Windows
./run_test.sh        # Linux/macOS
```

### 2. "Python nie znaleziony"
- Zainstaluj Python 3.7+ z [python.org](https://python.org)
- **Windows:** Zaznacz "Add to PATH" podczas instalacji
- Sprawdź: `python --version`

### 3. "Chrome nie znaleziony"
- Zainstaluj Google Chrome z [chrome.google.com](https://chrome.google.com)

### 4. Błędy kodowania Unicode (Windows)
- **Naprawione!** test_system.py automatycznie obsługuje UTF-8
- Jeśli nadal problem: `chcp 65001` przed uruchomieniem

### 5. Venv nie działa
```bash
# Usuń i utwórz ponownie:
# Windows:
rmdir /s venv
python setup_venv.py

# Linux/macOS:
rm -rf venv
python3 setup_venv.py
```

### 6. Brak modułów po aktywacji venv
```bash
# Sprawdź czy używasz właściwego Pythona:
which python        # Linux/macOS
where python        # Windows

# Powinno pokazać ścieżkę do venv/Scripts/python.exe (Windows)
# lub venv/bin/python (Linux/macOS)
```

### 7. Test ChromeDriver nie przechodzi
```bash
# Uruchom test z venv:
run_test.bat         # Windows
./run_test.sh        # Linux/macOS

# Lub ręcznie:
activate_venv.bat && python test_system.py
```

### 8. Brak wyników w scrapingu
- Zwiększ opóźnienia: 40-60s między zapytaniami
- Sprawdź czy Kayak nie blokuje (spróbuj za kilka godzin)
- Użyj mniejszej liczby linii lotniczych

### 9. Błędy w Data Extractor
```
GUI → Data Extractor → Preview Data
(sprawdź czy pliki .txt zawierają ceny)
```

## 📁 Struktura projektu

```
drapaKajaK/
├── 🌐 venv/                         # Środowisko wirtualne Python
├──
├── ⚡ run.bat/sh                     # GŁÓWNY LAUNCHER (auto-venv) ⭐ NOWY!
├── ⚙️ setup_venv.py                 # Tworzenie środowiska wirtualnego
├── 🚀 activate_venv.bat/sh          # Aktywacja venv (opcjonalne)
├── ▶️ run_test.bat/sh               # Uruchom testy (auto-venv)
├── ▶️ run_scraper.bat/sh            # Uruchom scraper (auto-venv)
├──
├── 🖥️ FlightTool_Simple.py          # GŁÓWNE GUI
├── 🔧 test_system.py                # Tester systemu (Unicode fix)
├──
├── 🔄 scrap_only_extended.py        # Extended scraper (używany przez GUI)
├── 📋 kayak_excel_scraper.py        # Excel scraper (używany przez GUI)
├── 📊 simple_kayak_extractor.py     # Data extractor (używany przez GUI)
├──
├── ⚙️ config_extended.json          # Konfiguracja (generowana przez GUI)
├── 📄 flights_list.xlsx             # Przykładowe loty (tworzony przez GUI)
├──
├── 📁 kayak_text_data/              # Wyniki Extended mode
├── 📁 kayak_excel_data/             # Wyniki Excel mode
└── 📊 kayak_offers_[timestamp].xlsx # Analiza Excel (generowany przez GUI)
```

## 🎨 Zaawansowane funkcje GUI

### Extended Scraper (zakładka):
- **Route:** WAW → ICN (edytowalne kody IATA)
- **Dates:** Zakresy dat z polami tekstowymi  
- **Airlines:** 15+ linii jako checkboxy z przyciskami "Select All/None/Popular"
- **Rolling Mode:** Checkbox + ustawienia przerw
- **Live Logs:** Postęp w czasie rzeczywistym

### Excel Scraper (zakładka):
- **Browse:** Wybór pliku Excel
- **Create Sample:** Automatyczne tworzenie przykładu
- **Live Logs:** Postęp dla każdego lotu z Excel

### Data Extractor (zakładka):
- **Browse:** Wybór folderu z wynikami
- **Preview:** Podgląd znalezionych plików
- **Quick Select:** Szybki wybór `rolling_mode`

## 🚨 Ważne uwagi

- **Szanuj Kayak**: Używaj rozsądnych opóźnień (30-45s)
- **Nie przesadzaj**: Max 50-100 zapytań na sesję
- **Rolling mode**: Idealny do długoterminowego monitorowania
- **GUI automatycznie zapisuje** konfigurację między sesjami

## 🎯 Porównanie: Stara vs Nowa metoda

### ❌ Stara metoda (instalacja globalna):
```bash
# Instalacja na systemowym Pythonie (niebezpieczne):
pip install selenium webdriver-manager requests pandas...
# Może konfliktować z innymi projektami
# Problemy z Unicode na Windows
python scrap_only_extended.py
# Pamiętać komendy i ścieżki
python simple_kayak_extractor.py kayak_text_data/session_folder
```

### ✅ Nowa metoda (auto-venv + GUI):
```bash
# NAJŁATWIEJ - run.bat/sh (auto-venv!):
run.bat              # Windows - GUI
./run.sh             # Linux/macOS - GUI
run.bat test         # Test systemu
./run.sh scraper     # Extended scraper

# Lub ręcznie (jeśli wolisz):
python setup_venv.py         # Raz - tworzy venv
activate_venv.bat            # Windows - aktywuj
python FlightTool_Simple.py  # Uruchom
```

## 🌟 Zalety nowego podejścia:

✅ **Auto-venv** - `run.bat` automatycznie tworzy i używa venv!
✅ **Zero konfiguracji** - działaa od razu, bez instalacji ręcznej
✅ **Venv izoluje pakiety** - nie psuje systemowego Pythona
✅ **Łatwe usuwanie** - usuń folder `venv/` i gotowe
✅ **Portable** - działa tak samo na Windows/Linux/macOS
✅ **Fix Unicode** - automatycznie obsługuje polskie znaki (Windows)
✅ **Bezpieczne** - każdy projekt ma swoje pakiety

---

**Projekt**: drapaKajaK - Flight Price Scraper
**Typ**: GUI-first aplikacja scrapingu lotów z auto-venv
**Status**: Aktywnie rozwijany
**Główny interfejs**: FlightTool_Simple.py
**Quick Start**: `run.bat` (Windows) lub `./run.sh` (Linux/macOS)

**💡 Tip 1**: Użyj `run.bat` - automatycznie sprawdza i tworzy venv!
**💡 Tip 2**: GUI automatycznie zapisuje konfigurację
**💡 Tip 3**: Wszystkie skrypty mają auto-venv - `run_test.bat`, `run_scraper.bat`
**💡 Tip 4**: Możesz mieć wiele venv dla różnych projektów bez konfliktów!
