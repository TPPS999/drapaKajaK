# 🛠️ Ręczna instalacja - Kayak Flight Scraper

**⚠️ Uwaga**: To instrukcja dla zaawansowanych użytkowników. Jeśli chcesz prostą instalację, użyj [QUICK_SETUP.md](QUICK_SETUP.md)

Kompletny przewodnik ręcznej instalacji systemu scrapingu lotów z pełną kontrolą nad każdym krokiem.

## 🎯 Wymagania systemowe

### Obsługiwane systemy operacyjne
- **Windows 10/11** ✅ (zalecane)
- **macOS 10.15+** ✅
- **Linux** (Ubuntu 20.04+, Debian 11+) ✅

### Wymagane oprogramowanie
- **Python 3.8 lub nowszy** (zalecane: Python 3.10+)
- **Google Chrome browser** (najnowsza wersja)
- **Git** (dla klonowania repozytorium)

## 🚀 Instalacja krok po kroku

### Krok 1: Instalacja Python

#### Windows
```bash
# Pobierz Python z https://python.org
# LUB użyj Chocolatey
choco install python

# LUB użyj winget
winget install Python.Python.3.12
```

#### macOS
```bash
# Użyj Homebrew
brew install python@3.12

# LUB pobierz z https://python.org
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.12 python3.12-pip python3.12-venv
```

**Weryfikacja instalacji:**
```bash
python --version
# Powinno pokazać: Python 3.8+ lub nowszy
```

### Krok 2: Instalacja Google Chrome

#### Windows
```bash
# Pobierz z https://chrome.google.com
# LUB użyj Chocolatey
choco install googlechrome
```

#### macOS
```bash
# Pobierz z https://chrome.google.com
# LUB użyj Homebrew
brew install --cask google-chrome
```

#### Linux
```bash
# Ubuntu/Debian
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
sudo apt update
sudo apt install google-chrome-stable
```

### Krok 3: Pobieranie projektu

#### Opcja A: Git clone (zalecane)
```bash
git clone [URL-REPOZYTORIUM]
cd kayak-flight-scraper
```

#### Opcja B: Pobierz ZIP
```bash
# Pobierz ZIP z GitHub
# Rozpakuj do katalogu kayak-flight-scraper
cd kayak-flight-scraper
```

### Krok 4: Tworzenie środowiska wirtualnego (zalecane)

```bash
# Utwórz środowisko wirtualne
python -m venv venv

# Aktywuj środowisko
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Sprawdź aktywację (powinien pojawić się (venv) na początku linii)
```

### Krok 5: Instalacja zależności

#### Metoda automatyczna (zalecana)
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Metoda ręczna
```bash
pip install --upgrade pip

# Core dependencies
pip install selenium>=4.15.0
pip install webdriver-manager>=4.0.1
pip install pandas>=2.0.0
pip install openpyxl>=3.1.0
pip install requests>=2.31.0
pip install beautifulsoup4>=4.12.0
pip install plyer>=2.1.0

# Optional
pip install colorama>=0.4.6
```

### Krok 6: Test instalacji

#### Test podstawowy
```bash
python -c "import selenium; print('Selenium:', selenium.__version__)"
python -c "import pandas; print('Pandas:', pandas.__version__)"
python -c "import webdriver_manager; print('WebDriver Manager: OK')"
```

#### Test ChromeDriver
```bash
python -c "
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.get('data:text/html,<h1>Test OK</h1>')
print('ChromeDriver działa!')
driver.quit()
"
```

#### Test GUI (opcjonalny)
```bash
python FlightTool_Complete.py
# Powinno otworzyć się okno GUI
```

## 🔧 Konfiguracja początkowa

### 1. Sprawdź pliki konfiguracyjne

#### Extended Mode
```bash
# Sprawdź czy istnieje config_extended.json
ls config_extended.json

# Jeśli nie ma, uruchom scraper (utworzy automatycznie)
python scrap_only_extended.py
```

#### Excel Mode
```bash
# Sprawdź czy istnieje excel_config.json
ls excel_config.json

# Jeśli nie ma, uruchom scraper (utworzy automatycznie)  
python kayak_excel_scraper.py
```

### 2. Utwórz katalogi robocze
```bash
mkdir -p kayak_text_data
mkdir -p kayak_excel_data
mkdir -p debug
```

### 3. Test pierwszego scrapingu
```bash
# Krótki test (5 minut)
# Edytuj config_extended.json:
# - ustaw krótki zakres dat (2-3 dni)
# - wybierz 1-2 linie lotnicze
# - delay_between_requests: [20, 30]

python scrap_only_extended.py
```

## 🛠️ Rozwiązywanie problemów instalacji

### Problem: Python nie jest rozpoznawany

**Windows:**
```bash
# Dodaj Python do PATH
# Control Panel → System → Advanced → Environment Variables
# Dodaj do PATH: C:\Python312 i C:\Python312\Scripts
```

**Rozwiązanie uniwersalne:**
```bash
# Użyj py zamiast python (Windows)
py --version
py -m pip install -r requirements.txt
```

### Problem: pip nie działa

```bash
# Aktualizuj pip
python -m pip install --upgrade pip

# LUB zainstaluj pip ręcznie
python -m ensurepip --default-pip
```

### Problem: ChromeDriver error

```bash
# Sprawdź wersję Chrome
google-chrome --version  # Linux/macOS
# W Windows: Chrome → Help → About

# Usuń stare ChromeDriver
rm -rf ~/.wdm  # macOS/Linux
# Windows: usuń C:\Users\[user]\.wdm

# Przeinstaluj webdriver-manager
pip uninstall webdriver-manager
pip install webdriver-manager>=4.0.1
```

### Problem: Selenium WebDriver nie działa

```bash
# Sprawdź konflikt z innymi wersjami
pip list | grep selenium

# Przeinstaluj selenium
pip uninstall selenium
pip install selenium>=4.15.0

# Test ręczny
python -c "
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--version')
driver = webdriver.Chrome(options=options)
driver.quit()
print('OK')
"
```

### Problem: Pandas/openpyxl błędy

```bash
# Zainstaluj dodatkowe zależności
pip install xlsxwriter
pip install lxml

# Windows - może wymagać Visual C++
# Pobierz: Microsoft Visual C++ Redistributable
```

### Problem: Import errors

```bash
# Sprawdź środowisko wirtualne
which python  # macOS/Linux
where python  # Windows

# Upewnij się że używasz właściwego Python
pip list | grep -E "(selenium|pandas|webdriver)"

# Reinstalacja w czystym środowisku
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

## 📋 Checklist instalacji

### ✅ Przed uruchomieniem sprawdź:

- [ ] **Python 3.8+** zainstalowany i działa
- [ ] **Google Chrome** najnowsza wersja
- [ ] **Środowisko wirtualne** aktywne (zalecane)
- [ ] **Wszystkie zależności** zainstalowane (`pip list`)
- [ ] **ChromeDriver test** przeszedł pomyślnie
- [ ] **Struktura katalogów** utworzona
- [ ] **Pierwszy test scrapingu** zakończony sukcesem

### 🎯 Gotowe do użycia!

```bash
# Test wszystkich komponentów
python FlightTool_Complete.py
# → powinno otworzyć GUI bez błędów

# LUB test Extended scrapingu
python scrap_only_extended.py
# → powinno utworzyć config i rozpocząć scraping

# LUB test Excel scrapingu  
python kayak_excel_scraper.py
# → powinno utworzyć przykładowy flights_list.xlsx
```

## 🚀 Co dalej?

Po pomyślnej ręcznej instalacji przejdź do:
1. **[QUICK_SETUP.md](QUICK_SETUP.md)** - porównaj z automatyczną instalacją
2. **[README.md](README.md)** - główna dokumentacja użytkowania  
3. **[data_extractor_guide.md](data_extractor_guide.md)** - analiza danych

## 💡 Wskazówki dla zaawansowanych

### Instalacja w środowisku Docker
```dockerfile
FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "scrap_only_extended.py"]
```

### Instalacja na serwerze (headless)
```bash
# Ubuntu Server bez GUI
sudo apt install python3-pip xvfb
pip install -r requirements.txt

# Uruchom z virtual display
xvfb-run -a python scrap_only_extended.py
```

### Automatyzacja z systemd (Linux)
```ini
# /etc/systemd/system/kayak-scraper.service
[Unit]
Description=Kayak Flight Scraper
After=network.target

[Service]
Type=simple
User=scraper
WorkingDirectory=/home/scraper/kayak-flight-scraper
ExecStart=/home/scraper/kayak-flight-scraper/venv/bin/python scrap_only_extended.py
Restart=always

[Install]
WantedBy=multi-user.target
```

---

**Pomoc techniczna**: 
- **Preferujesz automatyczną instalację?** → [QUICK_SETUP.md](QUICK_SETUP.md)
- **Problemy z ręczną instalacją?** → [TROUBLESHOOTING.md](TROUBLESHOOTING.md) 
- **Inne problemy?** → Utwórz issue w repozytorium