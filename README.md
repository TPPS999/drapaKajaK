# drapaKajaK — Śledzenie cen lotów z Kayak

Narzędzie do automatycznego sprawdzania i monitorowania cen lotów z Kayak.pl. Obsługuje wiele linii lotniczych, zakresów dat i konkretnych linków. Ma prosty interfejs graficzny — nie trzeba nic pisać w terminalu.

---

## Zanim zaczniesz — wymagania wstępne

Zainstaluj dwie rzeczy. Bez nich nic nie zadziała.

### 1. Python 3.8 lub nowszy

**Windows:**
1. Wejdź na https://www.python.org/downloads/
2. Kliknij duży żółty przycisk „Download Python 3.x.x"
3. Uruchom pobrany instalator
4. ⚠️ **WAŻNE:** Zaznacz checkbox „**Add Python to PATH**" na pierwszym ekranie
5. Kliknij „Install Now"
6. Sprawdź w terminalu: `python --version` — powinno pokazać np. `Python 3.11.x`

**macOS:**
```bash
brew install python3
```
Jeśli nie masz brew: https://brew.sh

**Linux (Ubuntu/Debian):**
```bash
sudo apt install python3 python3-pip python3-venv
```

---

### 2. Google Chrome lub Chromium

Program otwiera Chrome automatycznie w tle (tryb niewidoczny) żeby sprawdzać ceny. Chrome musi być zainstalowany na komputerze.

**Windows:**
1. Wejdź na https://www.google.com/chrome/
2. Pobierz i zainstaluj

Lub jeśli wolisz Chromium (wersja open-source, bez Google):
1. Wejdź na https://www.chromium.org/getting-involved/download-chromium/
2. Pobierz i zainstaluj

**macOS:**
```bash
brew install --cask google-chrome
# lub Chromium:
brew install --cask chromium
```

**Linux:**
```bash
# Chrome:
sudo apt install google-chrome-stable

# Lub Chromium (lżejszy, bez Google):
sudo apt install chromium-browser
```

> **Dlaczego Chrome?** Kayak.pl to strona, która ładuje ceny przez JavaScript. Zwykłe zapytanie HTTP ich nie zobaczy — potrzebna jest prawdziwa przeglądarka. Program otwiera ją w tle, bez okna, czyta ceny i zamyka.

> **ChromeDriver** (sterownik do automatyzacji Chrome) jest pobierany automatycznie przy pierwszym uruchomieniu — nie musisz go instalować ręcznie.

---

## Instalacja i pierwsze uruchomienie

### Krok 1: Pobierz projekt

**Opcja A — przez Git (zalecane):**
```bash
git clone https://github.com/TPPP999/drapaKajaK.git
cd drapaKajaK
```

**Opcja B — jako ZIP (bez Git):**
1. Wejdź na https://github.com/TPPP999/drapaKajaK
2. Kliknij zielony przycisk `Code` → `Download ZIP`
3. Rozpakuj ZIP
4. Otwórz terminal/cmd w folderze `drapaKajaK`

### Krok 2: Uruchom

**Windows** — kliknij dwukrotnie `run.bat` lub wpisz w terminalu:
```
run.bat
```

**Linux/macOS:**
```bash
chmod +x run.sh   # jednorazowo, nadaje uprawnienia
./run.sh
```

To wszystko. Przy pierwszym uruchomieniu program automatycznie:
- tworzy środowisko wirtualne Python (`venv/`)
- instaluje wszystkie wymagane biblioteki
- otwiera interfejs graficzny

---

## Interfejs — zakładki

Po uruchomieniu zobaczysz okno z pięcioma zakładkami:

| Zakładka | Do czego służy |
|----------|---------------|
| **Extended Scraper** | Sprawdza wszystkie kombinacje dat w zadanym zakresie. Wybierasz trasę, daty od-do, linie lotnicze i klikasz START. |
| **URL Watcher** | Wklejasz konkretne linki z Kayak i program monitoruje je cyklicznie. Najprostsza opcja jeśli wiesz czego szukasz. |
| **Excel Scraper** | Sprawdza loty z pliku Excel (własna lista konkretnych dat/tras). |
| **Data Extractor** | Wyciąga najlepsze oferty z zebranych danych i zapisuje do Excel. |
| **Test** | Sprawdza czy Chrome i ChromeDriver działają poprawnie. |

---

## Tryb URL Watcher — monitorowanie konkretnych linków

Najprostszy sposób użycia. Zamiast konfigurować zakresy dat, wklejasz gotowe linki z Kayak.

### Jak uzyskać link z Kayak:
1. Wejdź na www.kayak.pl
2. Wybierz trasę, daty, liczbę pasażerów
3. Odfiltruj konkretną linię lotniczą (ważne — filter na stronie wyników)
4. Skopiuj URL z paska przeglądarki

Przykładowy link:
```
https://www.kayak.pl/flights/WAW-AKL/2026-10-28/2026-11-18/2adults?sort=bestflight_a&fs=airlines%3DQF%2CMULT
```

### Jak używać:
1. Otwórz zakładkę **URL Watcher**
2. Wklej linki — jeden na linię
3. Ustaw interwał sprawdzania (domyślnie: co 60 minut)
4. Kliknij **"Zapisz watchlistę"** a potem **"START WATCHING"**

Wyniki zapisywane są do pliku CSV w folderze `output/url_watcher/` — każdy dzień to osobny plik `prices_YYYYMMDD.csv`.

Możesz też uruchomić jednorazowo (bez ciągłego monitorowania):
```
run.bat watcher-once
```

---

## Tryb Extended Scraper — wszystkie kombinacje

Jeśli nie masz jeszcze konkretnych dat, ten tryb sprawdza wszystkie możliwe kombinacje w zadanym zakresie.

### Konfiguracja w GUI:
- **Trasa:** kody IATA lotnisk, np. `WAW` → `AKL`
- **Daty wylotu:** zakres od-do (np. 24-30 października)
- **Daty powrotu:** zakres od-do
- **Długość pobytu:** minimalna i maksymalna liczba dni
- **Linie lotnicze:** zaznacz checkboxy
- **Opóźnienia:** czas między zapytaniami (zalecane 30-45s)

### Dostępne linie lotnicze:
| Region | Linie |
|--------|-------|
| Zatokowe | Turkish Airlines, Emirates, Qatar Airways, Etihad |
| Europejskie | LOT, Lufthansa, KLM, Air France, Swiss, Austrian, Finnair, SAS |
| Azjatyckie | Singapore Airlines, Korean Air, All Nippon Airways, Cathay Pacific, Asiana, Air China |
| Australijskie / inne | Qantas, British Airways, American Airlines |

### Rolling mode (ciągłe monitorowanie):
Zaznacz checkbox „Rolling mode" — program po zakończeniu jednej rundy odczeka podaną liczbę minut i zaczyna od nowa. Idealny do uruchomienia na noc.

---

## Analiza wyników — Data Extractor

Po zebraniu danych:
1. Otwórz zakładkę **Data Extractor**
2. Kliknij **Browse** i wybierz folder z wynikami (`output/kayak_text_data/...`)
3. **Preview Data** — sprawdź ile plików znaleziono
4. **EXTRACT TO EXCEL** — tworzy plik Excel z najlepszymi ofertami

Plik Excel zawiera kolumny:
- Cena za osobę i łącznie (PLN)
- Data wylotu i powrotu
- Linia lotnicza
- Czasy lotów i przesiadek
- Lotniska przesiadkowe

---

## Komendy CLI (bez GUI)

```bash
run.bat                  # Uruchom GUI (Windows)
run.bat test             # Test ChromeDriver
run.bat scraper          # Extended scraper (bez GUI)
run.bat watcher          # URL Watcher — ciągłe monitorowanie
run.bat watcher-once     # URL Watcher — jednorazowe sprawdzenie
run.bat extractor <ścieżka>  # Data Extractor
```

Linux/macOS — te same komendy z `./run.sh` zamiast `run.bat`.

---

## Struktura plików

```
drapaKajaK/
├── run.bat / run.sh          ← TUTAJ ZACZYNASZ
├── requirements.txt          ← lista bibliotek Python
│
├── src/
│   ├── FlightTool_Simple.py  ← główne GUI
│   ├── url_watcher.py        ← URL Watcher (scraper)
│   ├── scrap_only_extended.py← Extended scraper
│   ├── kayak_excel_scraper.py← Excel scraper
│   ├── simple_kayak_extractor.py ← analiza wyników
│   └── test_system.py        ← testy
│
├── config/
│   ├── config_extended.json  ← konfiguracja Extended (zapisywana przez GUI)
│   └── url_watchlist.json    ← lista URLi do monitorowania
│
├── output/
│   ├── kayak_text_data/      ← surowe wyniki Extended mode
│   ├── kayak_excel_data/     ← wyniki Excel mode
│   └── url_watcher/          ← wyniki URL Watcher (CSV)
│
├── scripts/
│   └── setup_venv.py         ← tworzenie środowiska (wywoływane przez run.bat)
│
└── venv/                     ← środowisko wirtualne (tworzone automatycznie)
```

---

## Rozwiązywanie problemów

### „Python nie znaleziony" / „python is not recognized"
- Zainstaluj Python ze strony https://www.python.org/downloads/
- Podczas instalacji zaznacz **„Add Python to PATH"**
- Zrestartuj terminal po instalacji

### „Chrome nie znaleziony" / błąd ChromeDriver
- Zainstaluj Google Chrome: https://www.google.com/chrome/
- Jeśli masz Chromium zamiast Chrome — też powinno działać
- Sprawdź zakładkę **Test** → „Quick ChromeDriver Test"

### Ceny nie są znajdowane / scraper nic nie zbiera
- Zwiększ opóźnienia do 40-60s (Kayak blokuje zbyt szybkie zapytania)
- Spróbuj za kilka godzin — Kayak może tymczasowo blokować
- Sprawdź czy link z Kayak jest poprawny (zakładka URL Watcher)

### Okno GUI się nie otwiera
```bash
# Windows:
run.bat gui

# Linux/macOS:
./run.sh gui
```
Jeśli nadal nie działa, sprawdź czy `python --version` zwraca 3.8+.

### Trzeba przeinstalować biblioteki
```bash
# Usuń venv i uruchom ponownie:
# Windows:
rmdir /s /q venv
run.bat

# Linux/macOS:
rm -rf venv
./run.sh
```

---

## Ważne uwagi

- Używaj **rozsądnych opóźnień** (30-45s między zapytaniami) — szanuj serwis Kayak
- **Rolling mode** najlepiej uruchamiać na noc lub na wiele godzin
- Wyniki są zapisywane lokalnie — nigdzie nie są wysyłane
- Program działa tylko z **kayak.pl** i **kayak.com**
