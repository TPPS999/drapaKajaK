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
- Porównaj średnie ceny różnych przewo
