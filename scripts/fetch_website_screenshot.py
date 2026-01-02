#!/usr/bin/env python3
"""
Script to capture a live screenshot of www.ananymishra.tech
and save it for the GitHub README.
"""

import os
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Configuration
WEBSITE_URL = "https://www.ananymishra.tech"
OUTPUT_DIR = Path("assests")
OUTPUT_FILE = "website.png"
VIEWPORT_WIDTH = 1920
VIEWPORT_HEIGHT = 1080
WAIT_TIME = 5  # seconds to wait for page to fully load


def setup_driver():
    """Configure and return a headless Chrome WebDriver."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(f"--window-size={VIEWPORT_WIDTH},{VIEWPORT_HEIGHT}")
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.add_argument("--force-device-scale-factor=1")
    
    # For better rendering
    chrome_options.add_argument("--enable-features=NetworkService,NetworkServiceInProcess")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def capture_screenshot(driver, url, output_path):
    """Navigate to URL and capture a screenshot."""
    print(f"🌐 Navigating to {url}")
    driver.get(url)
    
    # Wait for page to load completely
    print(f"⏳ Waiting {WAIT_TIME} seconds for page to fully load...")
    time.sleep(WAIT_TIME)
    
    # Try to wait for body to be present
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(("tag name", "body"))
        )
    except TimeoutException:
        print("⚠️ Page load timeout, continuing with screenshot...")
    
    # Get full page dimensions for full-page screenshot (optional)
    total_height = driver.execute_script("return document.body.scrollHeight")
    total_width = driver.execute_script("return document.body.scrollWidth")
    
    print(f"📐 Page dimensions: {total_width}x{total_height}")
    
    # Capture screenshot
    print(f"📸 Capturing screenshot...")
    driver.save_screenshot(str(output_path))
    print(f"✅ Screenshot saved to: {output_path}")


def capture_full_page_screenshot(driver, url, output_path):
    """Capture a full-page screenshot by scrolling."""
    print(f"🌐 Navigating to {url}...")
    driver.get(url)
    
    # Wait for page to load
    print(f"⏳ Waiting {WAIT_TIME} seconds for page to fully load...")
    time.sleep(WAIT_TIME)
    
    # Get page dimensions
    total_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")
    
    # Set window size to capture full page
    driver.set_window_size(VIEWPORT_WIDTH, min(total_height, 4000))  # Cap at 4000px
    
    # Small delay after resize
    time.sleep(1)
    
    # Capture screenshot
    print(f"📸 Capturing full-page screenshot...")
    driver.save_screenshot(str(output_path))
    print(f"✅ Screenshot saved to: {output_path}")


def main():
    """Main function to capture website screenshot."""
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / OUTPUT_FILE
    
    print("=" * 50)
    print("🖥️  Website Screenshot Capture")
    print("=" * 50)
    print(f"📍 URL: {WEBSITE_URL}")
    print(f"📁 Output: {output_path}")
    print("=" * 50)
    
    driver = None
    try:
        driver = setup_driver()
        
        # Capture viewport screenshot (not full page)
        capture_screenshot(driver, WEBSITE_URL, output_path)
        
        # Alternatively, use this for full page:
        # capture_full_page_screenshot(driver, WEBSITE_URL, output_path)
        
        print("\n✨ Done! Screenshot captured successfully.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise
    finally:
        if driver:
            driver.quit()
            print("🔒 Browser closed.")


if __name__ == "__main__":
    main()
