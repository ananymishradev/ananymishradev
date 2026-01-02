#!/usr/bin/env python3
"""
Script to capture a live screenshot of www.ananymishra.tech
"""

import sys
import time
from pathlib import Path

# Try importing selenium
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    print("✅ Selenium imported successfully")
except ImportError as e:
    print(f"❌ Failed to import selenium: {e}")
    sys.exit(1)

# Configuration
WEBSITE_URL = "https://www.ananymishra.tech"
OUTPUT_DIR = Path("assests")
OUTPUT_FILE = "website.png"

def main():
    print("=" * 50)
    print("🖥️  Website Screenshot Capture")
    print("=" * 50)
    
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / OUTPUT_FILE
    
    print(f"📍 URL: {WEBSITE_URL}")
    print(f"📁 Output: {output_path}")
    
    # Setup Chrome options
    print("🔧 Setting up Chrome options...")
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--hide-scrollbars")
    
    # Start browser
    print("🚀 Starting Chrome browser...")
    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        print("✅ Chrome started successfully")
        
        # Navigate to page
        print(f"🌐 Navigating to {WEBSITE_URL}")
        driver.get(WEBSITE_URL)
        
        # Wait for page to load
        print("⏳ Waiting 8 seconds for page to load...")
        time.sleep(8)
        
        # Get page info
        title = driver.title
        print(f"📄 Page title: {title}")
        
        # Take screenshot
        print(f"📸 Taking screenshot...")
        result = driver.save_screenshot(str(output_path))
        print(f"📸 save_screenshot returned: {result}")
        
        # Verify file
        if output_path.exists():
            size = output_path.stat().st_size
            print(f"✅ SUCCESS! Screenshot saved: {output_path} ({size} bytes)")
        else:
            print(f"❌ FAILED! File not found: {output_path}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        if driver:
            driver.quit()
            print("🔒 Browser closed")
    
    print("=" * 50)
    print("✨ Done!")

if __name__ == "__main__":
    main()
