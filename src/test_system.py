#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flight Tool - System Test Script
Tests all components and dependencies
"""

import sys
import os
import importlib

# Fix Windows console encoding issues
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*50)
    print(f"  {text}")
    print("="*50)

def test_python_modules():
    """Test Python modules"""
    print_header("TESTING PYTHON MODULES")
    
    modules = {
        'selenium': 'Selenium WebDriver',
        'webdriver_manager': 'WebDriver Manager', 
        'requests': 'HTTP Requests',
        'beautifulsoup4': 'BeautifulSoup4',
        'pandas': 'Pandas Data Analysis',
        'openpyxl': 'Excel File Support'
    }
    
    all_passed = True
    
    for module_name, description in modules.items():
        try:
            # Convert pip name to import name if needed
            import_name = module_name
            if module_name == 'beautifulsoup4':
                import_name = 'bs4'
            elif module_name == 'webdriver_manager':
                import_name = 'webdriver_manager'
            
            importlib.import_module(import_name)
            print(f"  ✓ {description}")
        except ImportError:
            print(f"  ✗ {description} - MISSING")
            all_passed = False
        except Exception as e:
            print(f"  ✗ {description} - ERROR: {e}")
            all_passed = False
    
    return all_passed

def test_chromedriver():
    """Test ChromeDriver"""
    print_header("TESTING CHROMEDRIVER")
    
    try:
        print("  Testing Selenium WebDriver...")
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        
        print("  ✓ Selenium imports successful")
        
        # Test ChromeDriver installation
        print("  Installing/updating ChromeDriver...")
        driver_path = ChromeDriverManager().install()
        print(f"  ✓ ChromeDriver path: {driver_path}")
        
        # Test basic WebDriver functionality
        print("  Testing WebDriver initialization...")
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        
        print("  ✓ WebDriver initialized")
        
        # Test basic navigation
        print("  Testing basic navigation...")
        driver.get('data:text/html,<h1>Test Page</h1>')
        title = driver.title
        
        driver.quit()
        print("  ✓ Navigation test passed")
        print("  ✓ ChromeDriver working correctly")
        
        return True
        
    except Exception as e:
        print(f"  ✗ ChromeDriver test failed: {e}")
        print("\n  Troubleshooting:")
        print("  1. Make sure Google Chrome is installed")
        print("  2. Check internet connection for ChromeDriver download")
        print("  3. Try running as administrator")
        return False

def test_project_files():
    """Test project files"""
    print_header("TESTING PROJECT FILES")

    # Get the directory where this script is located (src/)
    script_dir = os.path.dirname(os.path.abspath(__file__))

    required_files = [
        'scrap_only_extended.py',
        'kayak_excel_scraper.py',
        'simple_kayak_extractor.py'
    ]

    all_present = True

    for filename in required_files:
        filepath = os.path.join(script_dir, filename)
        if os.path.exists(filepath):
            print(f"  ✓ {filename}")
        else:
            print(f"  ✗ {filename} - MISSING")
            all_present = False
    
    if not all_present:
        print("\n  ⚠️  Some project files are missing")
        print("  Make sure you have all scraper files in the project folder")
    
    return all_present

def test_network_connectivity():
    """Test network connectivity"""
    print_header("TESTING NETWORK CONNECTIVITY")
    
    try:
        import requests
        
        # Test basic HTTP connectivity
        print("  Testing HTTP connectivity...")
        response = requests.get('https://httpbin.org/get', timeout=10)
        if response.status_code == 200:
            print("  ✓ HTTP connectivity working")
        else:
            print(f"  ✗ HTTP test failed with status: {response.status_code}")
            return False
        
        # Test Kayak accessibility (without actually scraping)
        print("  Testing Kayak accessibility...")
        response = requests.head('https://www.kayak.com', timeout=10)
        if response.status_code in [200, 301, 302]:
            print("  ✓ Kayak is accessible")
        else:
            print(f"  ⚠️  Kayak returned status: {response.status_code}")
        
        return True
        
    except requests.RequestException as e:
        print(f"  ✗ Network test failed: {e}")
        print("  Check your internet connection")
        return False
    except Exception as e:
        print(f"  ✗ Unexpected error: {e}")
        return False

def main():
    """Main test function"""
    
    print_header("FLIGHT TOOL SYSTEM TESTS")
    print("Running comprehensive system tests...")
    
    tests = [
        ("Python Modules", test_python_modules),
        ("ChromeDriver", test_chromedriver),
        ("Project Files", test_project_files),
        ("Network", test_network_connectivity)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n✗ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    print_header("TEST SUMMARY")
    
    passed_tests = sum(results.values())
    total_tests = len(results)
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {test_name:<20} {status}")
    
    print(f"\nResults: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED!")
        print("Flight Tool is ready to use!")
        return True
    else:
        print(f"\n⚠️  {total_tests - passed_tests} TEST(S) FAILED")
        print("Some features may not work correctly.")
        
        if not results.get("Python Modules", False):
            print("\n❌ CRITICAL: Python modules test failed")
            print("Please run setup_components.py first")
            return False
        
        if not results.get("ChromeDriver", False):
            print("\n⚠️  WARNING: ChromeDriver test failed")
            print("Scraping functionality may not work")
        
        return True  # Allow to continue even with some failures

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTests cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Test suite crashed: {e}")
        sys.exit(1)