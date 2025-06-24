# 🚀 Quick Setup - Automatyczna instalacja

Jeden skrypt robi wszystko - od instalacji do pierwszego scrapingu!

## ⚡ Szybki start (2 minuty)

### Windows
```bash
# 1. Pobierz projekt
git clone https://github.com/TPPS999/drapaKajaK.git
cd drapaKajaK

# 2. Uruchom automatyczną instalację i setup
setup_and_run.bat

# 3. Gotowe! 🎉
```

### Linux/macOS  
```bash
# 1. Pobierz projekt
git clone https://github.com/TPPS999/drapaKajaK.git
cd drapaKajaK

# 2. Uruchom automatyczną instalację i setup
chmod +x setup_and_run.sh
./setup_and_run.sh

# 3. Gotowe! 🎉
```

## 🛠️ Co robi automatyczny setup?

### ✅ Sprawdza system
- Python 3.8+ zainstalowany
- Google Chrome dostępny
- Połączenie internetowe

### 📦 Instaluje zależności
- Tworzy środowisko wirtualne (venv)
- Instaluje wszystkie biblioteki Python
- Pobiera i konfiguruje ChromeDriver

### 🔧 Konfiguruje projekt
- Tworzy katalogi robocze
- Generuje przykładowe pliki konfiguracyjne
- Testuje wszystkie komponenty

### 🚀 Uruchamia pierwszy test
- Krótki test scrapingu (5 minut)
- Weryfikuje że wszystko działa
- Pokazuje gdzie znaleźć wyniki

## 📁 Co otrzymujesz po setup?

```
kayak-flight-scraper/
├── ✅ venv/                        # Środowisko Python
├── ✅ config_extended.json         # Konfiguracja Extended
├── ✅ excel_config.json            # Konfiguracja Excel  
├── ✅ flights_list.xlsx            # Przykładowe loty
├── ✅ kayak_text_data/             # Katalog wyników
├── ✅ debug/                       # Debug pliki
└── ✅ test_results/                # Wyniki pierwszego testu
```

## 🎯 Następne kroki

Po pomyślnym setup:

### 1. **Sprawdź wyniki testu**
```bash
# Otwórz katalog z wynikami
cd test_results
ls -la

# Sprawdź Excel z pierwszymi danymi
start test_extraction.xlsx  # Windows
open test_extraction.xlsx   # macOS
```

### 2. **Uruchom GUI (najłatwiejsze)**
```bash
python FlightTool_Complete.py
```

### 3. **LUB uruchom scraper bezpośrednio**
```bash
# Extended mode (wszystkie kombinacje)
python scrap_only_extended.py

# Excel mode (konkretne loty)
python kayak_excel_scraper.py
```

### 4. **Analizuj wyniki**
```bash
# Po każdym scrapingu
python simple_kayak_extractor.py kayak_text_data/[session_folder]
```

## ❌ Troubleshooting

### Jeśli setup się nie powiódł:

**Windows:**
```bash
# Sprawdź logi
type setup.log

# Uruchom ponownie z administracyjnymi uprawnieniami
# Kliknij prawym → "Run as administrator"
setup_and_run.bat
```

**Linux/macOS:**
```bash
# Sprawdź logi
cat setup.log

# Uruchom z sudo jeśli potrzebne
sudo ./setup_and_run.sh
```

### Najczęstsze problemy:

**"Python nie znaleziony"**
- Zainstaluj Python 3.8+ z [python.org](https://python.org)
- Windows: Zaznacz "Add to PATH" podczas instalacji

**"Chrome nie znaleziony"**  
- Zainstaluj Google Chrome z [chrome.google.com](https://chrome.google.com)

**"Brak połączenia"**
- Sprawdź internet
- Wyłącz firewall/antywirus tymczasowo

## 🔄 Re-setup

Jeśli chcesz zacząć od nowa:

```bash
# Usuń stare środowisko
rm -rf venv kayak_text_data kayak_excel_data debug

# Uruchom setup ponownie
setup_and_run.bat  # Windows
./setup_and_run.sh # Linux/macOS
```

## 📞 Pomoc

- **Setup działa?** ✅ Przejdź do [README.md](README.md)
- **Setup nie działa?** ❌ Sprawdź [TROUBLESHOOTING.md](TROUBLESHOOTING.md)  
- **Chcesz ręczną instalację?** 🛠️ Zobacz [MANUAL_INSTALL.md](MANUAL_INSTALL.md)

---

💡 **Tip**: Setup automatycznie wykrywa twój system i dostosowuje instalację. Nie musisz nic konfigurować - po prostu uruchom i czekaj!
