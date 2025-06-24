# 🚀 Quick Start Guide - GUI Version

## ⚡ Szybki start (2 minuty) - Nowa wersja z GUI

### Windows
```bash
# 1. Pobierz projekt
git clone https://github.com/TPPS999/drapaKajaK.git
cd drapaKajaK

# 2. Uruchom automatyczną instalację i GUI
setup_and_run.bat

# 3. Gotowe! GUI się otworzy automatycznie 🎉
```

### Linux/macOS  
```bash
# 1. Pobierz projekt
git clone https://github.com/TPPS999/drapaKajaK.git
cd drapaKajaK

# 2. Uruchom automatyczną instalację i GUI
chmod +x setup_and_run.sh
./setup_and_run.sh

# 3. Gotowe! GUI się otworzy automatycznie 🎉
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

### ✅ setup_and_run.bat automatycznie:
1. **Sprawdza Python** - czy zainstalowany
2. **Instaluje komponenty** - wszystkie potrzebne biblioteki
3. **Testuje ChromeDriver** - pobiera i konfiguruje
4. **Uruchamia GUI** - otwiera FlightTool_Simple.py
5. **Wszystko gotowe!** - możesz od razu scrapować

## 📁 Co otrzymujesz po setup?

```
drapaKajaK/
├── ✅ FlightTool_Simple.py           # Główne GUI
├── ✅ scrap_only_extended.py         # Extended scraper
├── ✅ kayak_excel_scraper.py         # Excel scraper  
├── ✅ simple_kayak_extractor.py      # Data extractor
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

## ❌ Troubleshooting GUI

### GUI nie otwiera się:
```bash
# Ręczne uruchomienie:
python FlightTool_Simple.py

# Jeśli błąd - sprawdź komponenty:
python setup_components.py
python test_system.py
```

### "Python nie znaleziony":
- Zainstaluj Python 3.8+ z [python.org](https://python.org)
- Windows: Zaznacz "Add to PATH" podczas instalacji

### "Chrome nie znaleziony":  
- Zainstaluj Google Chrome z [chrome.google.com](https://chrome.google.com)

### Test nie przechodzi:
```
1. Zakładka "Test" → "Full System Test"
2. Sprawdź co jest czerwone
3. Menu → "Tools" → "Reinstall Components"
```

## 🎉 Zalety nowej wersji GUI:

✅ **Wszystko w jednym miejscu** - nie musisz pamiętać komend  
✅ **Logi na żywo** - widzisz postęp scrapingu  
✅ **Łatwa konfiguracja** - checkboxy zamiast edycji JSON  
✅ **Automatyczna instalacja** - jeden klik i działa  
✅ **Stop/Start** - możesz zatrzymać scraping w każdej chwili  
✅ **Preview danych** - sprawdzisz wyniki przed analizą  

## 🚀 Stara vs Nowa metoda:

### ❌ Stara metoda (manualna):
```bash
# Trzeba było pamiętać wszystkie komendy:
python scrap_only_extended.py
# Edytować config_extended.json ręcznie
python simple_kayak_extractor.py kayak_text_data/session_folder
```

### ✅ Nowa metoda (GUI):
```
1. setup_and_run.bat
2. Klik, klik, klik w GUI
3. Gotowe!
```

---

**💡 Tip**: GUI automatycznie zapisuje konfigurację, więc następnym razem wystarczy `python FlightTool_Simple.py` i twoje ustawienia będą zachowane!
