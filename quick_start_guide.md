# 🚀 Quick Start Guide - GUI Version

## ⚡ Szybki start (2 minuty) - Nowa wersja z GUI

### Windows
```bash
# 1. Pobierz projekt
git clone https://github.com/TPPS999/drapaKajaK.git
cd drapaKajaK

# 2. Utwórz środowisko wirtualne (venv)
python setup_venv.py

# 3. Aktywuj środowisko wirtualne
activate_venv.bat

# 4. Uruchom GUI
python FlightTool_Simple.py

# LUB użyj gotowych skryptów (nie wymaga aktywacji venv):
run_test.bat          # Test systemu
run_scraper.bat       # Scraper
```

### Linux/macOS
```bash
# 1. Pobierz projekt
git clone https://github.com/TPPS999/drapaKajaK.git
cd drapaKajaK

# 2. Utwórz środowisko wirtualne (venv)
python3 setup_venv.py

# 3. Aktywuj środowisko wirtualne
source activate_venv.sh
# lub: source venv/bin/activate

# 4. Uruchom GUI
python FlightTool_Simple.py

# LUB użyj gotowych skryptów (nie wymaga aktywacji venv):
./run_test.sh         # Test systemu
./run_scraper.sh      # Scraper
```

## 🖥️ Interfejs GUI - Flight Tool

Po uruchomieniu `setup_and_run.bat` automatycznie otwiera się **Flight Tool** z czterema zakładkami:

### 📑 Zakładki w GUI:

#### 1. **Extended Scraper**
- ✈️ **Trasa:** WAW → ICN (edytowalne)
- 📅 **Daty:** Zakres dat wylotu i powrotu
- ⏱️ **Pobyt:** 19-24 dni (konfigurowalne)
- 🛫 **Linie:** Wybierz z 15+ linii (checkboxy)
- ⚙️ **Ustawienia:** Opóźnienia, rolling mode
- ▶️ **START SCRAPING** - uruchamia scraping wszystkich kombinacji

#### 2. **Excel Scraper** 
- 📁 **Browse** - wybierz plik Excel z konkretnymi lotami
- 📋 **Create Sample** - tworzy przykładowy Excel
- ▶️ **START EXCEL SCRAPING** - sprawdza tylko loty z pliku

#### 3. **Data Extractor**
- 📂 **Browse** - wybierz folder z wynikami scrapingu
- 🔍 **Preview Data** - podgląd znalezionych plików
- 📊 **EXTRACT TO EXCEL** - tworzy analizę w Excel

#### 4. **Test**
- 🧪 **Quick ChromeDriver Test** - sprawdza czy wszystko działa
- 🔧 **Full System Test** - pełny test komponentów

## 🎯 Typowy workflow w GUI:

### Scenariusz 1: Znajdź najlepsze oferty (Extended)
```
1. Zakładka "Extended Scraper"
2. Ustaw trasę: WAW → ICN
3. Wybierz daty: Październik/Listopad 2025
4. Zaznacz linie: Turkish, Qatar, Emirates
5. Kliknij "START SCRAPING"
6. Po zakończeniu → zakładka "Data Extractor"
7. Wybierz folder wyników
8. Kliknij "EXTRACT TO EXCEL"
9. Otwiera się Excel z analizą!
```

### Scenariusz 2: Konkretne loty (Excel)
```
1. Zakładka "Excel Scraper"
2. Kliknij "Create Sample" → tworzy flights_list.xlsx
3. Edytuj Excel - dodaj swoje loty
4. W GUI: "Browse" → wybierz swój Excel
5. Kliknij "START EXCEL SCRAPING"
6. Po zakończeniu → "Data Extractor"
7. Analizuj wyniki w Excel
```

### Scenariusz 3: Test systemu
```
1. Zakładka "Test"
2. Kliknij "Quick ChromeDriver Test"
3. Sprawdź czy wszystko działa
4. Jeśli OK → przejdź do scrapingu
```

## 🔧 Co robi automatyczny setup?

### ✅ setup_venv.py automatycznie:
1. **Sprawdza Python** - weryfikuje wersję (3.7+)
2. **Tworzy venv** - izolowane środowisko Python
3. **Instaluje komponenty** - wszystkie biblioteki w venv
4. **Tworzy skrypty** - activate_venv.bat/sh, run_test.bat/sh
5. **Wszystko gotowe!** - możesz od razu używać narzędzi

### ✅ Zalety środowiska wirtualnego (venv):
- **Izolacja** - nie zmienia systemowego Pythona
- **Bezpieczeństwo** - każdy projekt ma swoje pakiety
- **Łatwość** - łatwe usunięcie (usuń folder venv)
- **Przenośność** - działa na każdym systemie

## 📁 Co otrzymujesz po setup?

```
drapaKajaK/
├── ✅ venv/                          # Środowisko wirtualne
├── ✅ setup_venv.py                  # Tworzenie venv
├── ✅ activate_venv.bat/sh           # Aktywacja venv
├── ✅ run_test.bat/sh                # Uruchom testy
├── ✅ run_scraper.bat/sh             # Uruchom scraper
├── ✅ FlightTool_Simple.py           # Główne GUI
├── ✅ scrap_only_extended.py         # Extended scraper
├── ✅ kayak_excel_scraper.py         # Excel scraper
├── ✅ simple_kayak_extractor.py      # Data extractor
├── ✅ test_system.py                 # Testy systemowe
├── ✅ config_extended.json           # Konfiguracja
├── ✅ flights_list.xlsx              # Przykładowe loty
├── ✅ kayak_text_data/               # Wyniki Extended
├── ✅ kayak_excel_data/              # Wyniki Excel
└── ✅ kayak_offers_[timestamp].xlsx  # Analiza Excel
```

## 🖱️ Pierwsze kroki w GUI:

### 1. **Test systemu** (zalecane na start)
```
Zakładka "Test" → "Quick ChromeDriver Test"
Sprawdź czy wyświetla: "✓ ChromeDriver test PASSED"
```

### 2. **Pierwszy scraping** (Extended Mode)
```
Zakładka "Extended Scraper":
- Zostaw domyślne WAW → ICN
- Zostaw daty październik/listopad
- Zaznacz 2-3 linie lotnicze
- Kliknij "START SCRAPING"
- Obserwuj logi w czasie rzeczywistym
```

### 3. **Analiza wyników**
```
Zakładka "Data Extractor":
- Kliknij "Browse" → wybierz kayak_text_data/txt_session_[data]
- Kliknij "Preview Data" → zobacz ile plików
- Kliknij "EXTRACT TO EXCEL" → tworzy analizę
- Otwiera się Excel z najlepszymi ofertami!
```

## ❌ Troubleshooting

### 1. GUI nie otwiera się:
```bash
# Windows:
activate_venv.bat
python FlightTool_Simple.py

# Linux/macOS:
source activate_venv.sh
python FlightTool_Simple.py

# LUB sprawdź testy:
run_test.bat         # Windows
./run_test.sh        # Linux/macOS
```

### 2. "Python nie znaleziony":
- Zainstaluj Python 3.7+ z [python.org](https://python.org)
- Windows: Zaznacz "Add to PATH" podczas instalacji
- Sprawdź: `python --version`

### 3. "Chrome nie znaleziony":
- Zainstaluj Google Chrome z [chrome.google.com](https://chrome.google.com)

### 4. Błędy kodowania Unicode (Windows):
- **Naprawione!** test_system.py automatycznie obsługuje UTF-8
- Jeśli nadal problem: użyj `chcp 65001` przed uruchomieniem

### 5. Venv nie działa:
```bash
# Usuń i utwórz ponownie:
# Windows:
rmdir /s venv
python setup_venv.py

# Linux/macOS:
rm -rf venv
python3 setup_venv.py
```

### 6. Brak modułów po aktywacji venv:
```bash
# Sprawdź czy używasz właściwego Pythona:
which python        # Linux/macOS
where python        # Windows

# Powinno pokazać ścieżkę do venv/Scripts/python.exe (Windows)
# lub venv/bin/python (Linux/macOS)
```

## 🎉 Zalety nowej wersji GUI:

✅ **Wszystko w jednym miejscu** - nie musisz pamiętać komend  
✅ **Logi na żywo** - widzisz postęp scrapingu  
✅ **Łatwa konfiguracja** - checkboxy zamiast edycji JSON  
✅ **Automatyczna instalacja** - jeden klik i działa  
✅ **Stop/Start** - możesz zatrzymać scraping w każdej chwili  
✅ **Preview danych** - sprawdzisz wyniki przed analizą  

## 🚀 Stara vs Nowa metoda:

### ❌ Stara metoda (bezpośrednio na systemie):
```bash
# Instalacja globalna (ryzykowna):
pip install selenium webdriver-manager requests...
# Może konfliktować z innymi projektami
python scrap_only_extended.py
```

### ✅ Nowa metoda (venv + GUI):
```bash
# Raz:
python setup_venv.py

# Zawsze:
activate_venv.bat         # Windows
source activate_venv.sh   # Linux/macOS
python FlightTool_Simple.py

# LUB bez aktywacji:
run_test.bat / run_scraper.bat
```

## 🌟 Zalety nowego podejścia:

✅ **Venv izoluje pakiety** - nie psuje systemowego Pythona
✅ **Łatwe usuwanie** - usuń folder `venv/` i gotowe
✅ **Portable** - działa wszędzie tak samo
✅ **Fix Unicode** - automatycznie obsługuje polskie znaki
✅ **Gotowe skrypty** - run_test.bat, run_scraper.bat

---

**💡 Tip 1**: Nie musisz aktywować venv - użyj `run_*.bat` skryptów!
**💡 Tip 2**: GUI automatycznie zapisuje konfigurację w config_extended.json
**💡 Tip 3**: Możesz mieć wiele venv dla różnych projektów bez konfliktów!
