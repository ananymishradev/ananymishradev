const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  try {
    // Set viewport size for high-quality screenshot
    await page.setViewportSize({ width: 1920, height: 1080 });
    
    // Navigate to website
    console.log('Navigating to https://ananymishra.tech...');
    await page.goto('https://ananymishra.tech', {
      waitUntil: 'networkidle',
      timeout: 30000
    });
    
    // Wait for any animations or lazy-loaded content
    console.log('Waiting for content to load...');
    await page.waitForTimeout(3000);
    
    // Take screenshot
    const screenshotPath = path.join(__dirname, '..', '..', 'assests', 'website.png');
    console.log('Taking screenshot...');
    await page.screenshot({
      path: screenshotPath,
      fullPage: true,
      quality: 90
    });
    
    console.log(`✅ Screenshot saved to ${screenshotPath}`);
  } catch (error) {
    console.error('❌ Error taking screenshot:', error);
    process.exit(1);
  } finally {
    await browser.close();
  }
})();
