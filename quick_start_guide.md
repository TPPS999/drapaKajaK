# 🚀 Quick Start Guide

## 1. Szybki start - Extended Mode

**Chcesz sprawdzić wszystkie loty WAW→ICN w październiku/listopadzie 2025?**

```bash
# 1. Pobierz projekt
git clone [repo]
cd kayak-flight-scraper

# 2. Zainstaluj zależności
pip install selenium pandas openpyxl webdriver-manager

# 3. Uruchom Extended Mode (użyje domyślnej konfiguracji)
python scrap_only_extended.py

# 4. 🆕 Wyciągnij najlepsze oferty do Excel
python simple_kayak_extractor.py kayak_text_data/txt_session_[timestamp]
```

Program automatycznie:
- Utworzy `config_extended.json` z przykładową konfiguracją
- Sprawdzi loty WAW→ICN na 19-24 dni w październiku/listopadzie
- Zapisze wyniki do `kayak_text_data/`
- **🆕 Extractor utworzy przejrzysty Excel z najlepszymi ofertami**

## 2. Szybki start - Excel Mode

**Masz konkretne daty lotów do sprawdzenia?**

```bash
# 1. Uruchom Excel Mode
python kayak_excel_scraper.py
```

Program automatycznie:
- Utworzy przykładowy plik `flights_list.xlsx`
- Wyświetli komunikat: "Edytuj plik i uruchom ponownie"

```bash
# 2. Edytuj flights_list.xlsx (dodaj swoje loty)
# 3. Uruchom ponownie
python kayak_excel_scraper.py

# 4. 🆕 Wyciągnij dane do Excel
python simple_kayak_extractor.py kayak_excel_data/excel_session_[timestamp]
```

## 3. Przykładowa konfiguracja - weekend w Amsterdamie

**config_extended.json:**
```json
{
  "scraping_config": {
    "origin": "WAW",
    "destination": "AMS", 
    "earliest_departure": "2025-09-01",
    "latest_return": "2025-10-31",
    "min_days": 2,
    "max_days": 4,
    "passengers": 2,
    "selected_airlines": ["KLM", "LOT"],
    "delay_between_requests": [25, 35],
    "rolling_mode": false
  }
}
```

## 4. Przykładowa konfiguracja Excel - konkretne loty

**flights_list.xlsx:**

| Lotnisko wylotu | Lotnisko docelowe | Filtr linii | Data wylotu | Data powrotu |
|-----------------|-------------------|-------------|-------------|--------------|
| WAW             | LHR               | LOT         | 2025-07-15  | 2025-07-22   |
| WAW             | CDG               | AirFrance   | 2025-08-10  | 2025-08-17   |
| WAW             | FCO               | Lufthansa   | 2025-09-05  | 2025-09-12   |
| KRK             | BCN               | Lufthansa   | 2025-10-01  | 2025-10-08   |

## 5. Rolling Mode - ciągły monitoring

```json
{
  "scraping_config": {
    "origin": "WAW",
    "destination": "JFK",
    "earliest_departure": "2025-12-01", 
    "latest_return": "2026-01-15",
    "min_days": 7,
    "max_days": 14,
    "passengers": 1,
    "selected_airlines": ["LOT", "Lufthansa"],
    "delay_between_requests": [30, 45],
    "rolling_mode": true,
    "rolling_break_minutes": [45, 90]
  }
}
```

**Uruchomienie:**
```bash
python scrap_only_extended.py
# Będzie działać w kółko, zatrzymanie: Ctrl+C
```

## 6. Popularne trasy i konfiguracje

### Seul (ICN) - długi pobyt
```json
"origin": "WAW", "destination": "ICN"
"min_days": 19, "max_days": 24
"selected_airlines": ["LOT", "Turkish", "Emirates", "Qatar", "China_Air"]
```

### Tokio (NRT) - krótki pobyt  
```json
"origin": "WAW", "destination": "NRT"
"min_days": 7, "max_days": 14
"selected_airlines": ["LOT", "Lufthansa", "KLM", "AirFrance"]
```

### Nowy Jork (JFK) - weekend
```json
"origin": "WAW", "destination": "JFK" 
"min_days": 3, "max_days": 7
"selected_airlines": ["LOT", "Lufthansa"]
```

### Londyn (LHR) - biznes
```json
"origin": "WAW", "destination": "LHR"
"min_days": 1, "max_days": 3  
"selected_airlines": ["LOT", "Lufthansa"]
```

## 7. Najczęstsze kody lotnisk

| Kod | Miasto | Kod | Miasto |
|-----|--------|-----|--------|
| WAW | Warszawa | ICN | Seul |
| KRK | Kraków | NRT | Tokio |
| GDN | Gdańsk | JFK | Nowy Jork |
| WRO | Wrocław | LHR | Londyn |
| POZ | Poznań | CDG | Paryż |
| KTW | Katowice | AMS | Amsterdam |
| RZE | Rzeszów | FCO | Rzym |
| LUZ | Lublin | BCN | Barcelona |

## 8. Pierwsze uruchomienie - checklist

✅ **Python 3.8+** zainstalowany  
✅ **Chrome browser** zainstalowany  
✅ **pip install selenium pandas openpyxl webdriver-manager**  
✅ **Kod pobrany** z repo  
✅ **Konfiguracja** sprawdzona (daty, kody lotnisk)  
✅ **Pierwsz test** - `python scrap_only_extended.py`  

## 9. Co się dzieje podczas działania?

```
🚀 ============================================================
🎯 KAYAK TEXT SCRAPER - SESJA ROZPOCZĘTA
🛫 Trasa: WAW → ICN  
📅 Zakres dat: 2025-10-05 → 2025-11-15
⏰ Długość pobytu: 19-24 dni
👥 Pasażerowie: 2
✈️ Linie: ['LOT', 'Turkish', 'Emirates', 'Qatar', 'China_Air']  
📁 Dane: kayak_text_data/txt_session_20250623_143022
============================================================

📅 120 kombinacji dat (standard mode)
🎯 600 zapytań dla trasy WAW→ICN (wszystkie kombinacje)

🔄 [1/600] LOT Polish Airlines | 2025-10-05→2025-10-24
🔍 LOT Polish Airlines | WAW→ICN | 2025-10-05→2025-10-24
🌐 Otwieram stronę...
⏳ Czekam 15.3s na załadowanie...
📝 Kopiuję tekst...
✅ Zapisano: 45,234 znaków → WAW-ICN_LOT_2025-10-05_2025-10-24_20250623_143022_123.txt
📊 Progress: 1 ✅ | 0 ❌ | 599 pozostało
💤 Opóźnienie: 32.1s

🔄 [2/600] Turkish Airlines + Multi | 2025-10-05→2025-10-24
...
```

## 10. Szybka diagnostyka problemów

**❌ "ChromeDriver Error"**
```bash
pip install webdriver-manager
```

**❌ "Nie można wczytać config"**
- Sprawdź czy plik istnieje
- Sprawdź składnię JSON (przecinki, cudzysłowy)

**❌ "Brak lotów w Excel"**
- Sprawdź nazwy kolumn (dokładnie jak w instrukcji)
- Sprawdź format dat (YYYY-MM-DD)
- Sprawdź kody lotnisk (3 znaki, wielkie litery)

**❌ "Timeout/Connection errors"**
- Zwiększ `delay_between_requests` do [40, 60]
- Sprawdź internet
- Spróbuj ponownie za kilka minut

**✅ Wszystko działa - ile czasu to zajmie?**
- ~30-45s na jedno zapytanie
- 100 zapytań = ~1-1.5 godziny
- Rolling mode: w nieskończoność (zatrzymanie Ctrl+C)

---

💡 **Protip:** Zacznij od małej konfiguracji (5-10 zapytań) żeby sprawdzić czy wszystko działa!