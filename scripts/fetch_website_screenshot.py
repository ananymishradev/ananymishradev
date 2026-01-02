#!/usr/bin/env python3
"""
Capture a screenshot of www.ananymishra.tech using a free screenshot API
"""

import urllib.request
import os
from pathlib import Path

# Configuration
WEBSITE_URL = "https://www.ananymishra.tech"
OUTPUT_DIR = Path("assests")
OUTPUT_FILE = "website.png"

# Free screenshot API (no API key needed)
# Using screenshot.abstractapi.com alternative - microlink
SCREENSHOT_API = f"https://api.microlink.io/?url={WEBSITE_URL}&screenshot=true&meta=false&embed=screenshot.url"

def main():
    print("=" * 50)
    print("🖥️  Website Screenshot Capture")
    print("=" * 50)
    
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / OUTPUT_FILE
    
    print(f"📍 Website: {WEBSITE_URL}")
    print(f"📁 Output: {output_path}")
    
    # Use a simpler approach - direct screenshot via thum.io (free, no key)
    screenshot_url = f"https://image.thum.io/get/width/1920/crop/1080/noanimate/{WEBSITE_URL}"
    
    print(f"🌐 Fetching screenshot from thum.io...")
    print(f"📎 URL: {screenshot_url}")
    
    try:
        # Create request with user agent
        request = urllib.request.Request(
            screenshot_url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        
        # Download the screenshot
        with urllib.request.urlopen(request, timeout=60) as response:
            image_data = response.read()
            
        print(f"📥 Downloaded {len(image_data)} bytes")
        
        # Save to file
        with open(output_path, 'wb') as f:
            f.write(image_data)
        
        # Verify
        if output_path.exists():
            size = output_path.stat().st_size
            print(f"✅ SUCCESS! Screenshot saved: {output_path} ({size} bytes)")
        else:
            print("❌ FAILED! File was not created")
            exit(1)
            
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
    
    print("=" * 50)
    print("✨ Done!")

if __name__ == "__main__":
    main()
