# 🚀 Quick Start - drapaKajaK Flight Tool

## ⚡ Ultra-szybki start (1 minuta!)

### Windows
```bash
# 1. Pobierz projekt
git clone https://github.com/TPPS999/drapaKajaK.git
cd drapaKajaK

# 2. Uruchom - AUTOMATYCZNIE TWORZY VENV!
run.bat              # Uruchom GUI
run.bat test         # Test systemu
```

### Linux/macOS
```bash
# 1. Pobierz projekt
git clone https://github.com/TPPS999/drapaKajaK.git
cd drapaKajaK

# 2. Nadaj uprawnienia (jednorazowo)
chmod +x run.sh run_test.sh run_scraper.sh

# 3. Uruchom - AUTOMATYCZNIE TWORZY VENV!
./run.sh             # Uruchom GUI
./run.sh test        # Test systemu
```

## 🎯 Dostępne komendy

### run.bat / run.sh - Główny launcher

```bash
run.bat              # GUI (domyślnie)
run.bat test         # Test systemu
run.bat gui          # GUI (jawnie)
run.bat scraper      # Extended scraper
run.bat excel        # Excel scraper
run.bat extractor    # Data extractor
```

### Specjalistyczne skrypty

```bash
run_test.bat         # Tylko test systemu
run_scraper.bat      # Tylko extended scraper
```

## ✨ Magia auto-venv

**Pierwsze uruchomienie:**
- ✅ Automatycznie tworzy venv
- ✅ Instaluje wszystkie pakiety
- ✅ Uruchamia wybraną funkcję

**Kolejne uruchomienia:**
- ✅ Używa istniejącego venv
- ✅ Natychmiastowy start

**Nigdy nie musisz:**
- ❌ Ręcznie tworzyć venv
- ❌ Aktywować venv
- ❌ Instalować pakietów
- ❌ Pamiętać komend

## 🧪 Test systemu

```bash
# Windows:
run.bat test

# Linux/macOS:
./run.sh test
```

Powinno pokazać:
```
✓ Python Modules       PASS
✓ ChromeDriver         PASS
✓ Project Files        PASS
✓ Network              PASS

🎉 ALL TESTS PASSED!
```

## 🖥️ Uruchomienie GUI

```bash
# Windows:
run.bat              # lub: run.bat gui

# Linux/macOS:
./run.sh             # lub: ./run.sh gui
```

GUI ma 4 zakładki:
1. **Extended Scraper** - wszystkie kombinacje dat/linii
2. **Excel Scraper** - konkretne loty z Excel
3. **Data Extractor** - analiza wyników do Excel
4. **Test** - sprawdzenie systemu

## 🔧 Wymagania

### Musisz mieć zainstalowane:
- **Python 3.7+** z [python.org](https://python.org)
- **Google Chrome** z [chrome.google.com](https://chrome.google.com)

### Reszta jest automatyczna!
- ✅ Venv - tworzone automatycznie
- ✅ Pakiety - instalowane automatycznie
- ✅ ChromeDriver - pobierany automatycznie

## ❓ Problemy?

### "Python nie znaleziony"
```bash
# Sprawdź czy Python jest w PATH:
python --version

# Jeśli nie - zainstaluj z python.org
# Windows: zaznacz "Add to PATH" podczas instalacji
```

### "Chrome nie znaleziony"
```bash
# Zainstaluj Google Chrome:
https://chrome.google.com
```

### Venv nie działa
```bash
# Usuń i utwórz ponownie:
# Windows:
rmdir /s venv
run.bat test

# Linux/macOS:
rm -rf venv
./run.sh test
```

### Unicode błędy (Windows)
✅ **Naprawione!** test_system.py automatycznie obsługuje UTF-8

## 📚 Więcej informacji

- **README.md** - pełna dokumentacja
- **quick_start_guide.md** - szczegółowy przewodnik GUI
- **installation_guide.md** - problemy z instalacją

## 💡 Protips

1. **Nie aktywuj venv ręcznie** - użyj `run.bat/sh`
2. **Pierwszy test** - uruchom `run.bat test` przed scrapingiem
3. **GUI zapisuje config** - ustawienia zachowane między sesjami
4. **Wiele venv OK** - każdy projekt może mieć swój venv

---

**Gotowe!** Teraz po prostu uruchom `run.bat` i zacznij scrapować! 🚀
