#!/usr/bin/env node

/**
 * Script to update website screenshot for GitHub profile README
 * Usage: npm run screenshot
 * Or: node scripts/update-screenshot.js
 */

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
    console.log('🌐 Navigating to https://ananymishra.tech...');
    await page.goto('https://ananymishra.tech', {
      waitUntil: 'networkidle',
      timeout: 30000
    });
    
    // Wait for any animations or lazy-loaded content
    console.log('⏳ Waiting for content to load...');
    await page.waitForTimeout(3000);
    
    // Ensure directory exists
    const screenshotDir = path.join(process.cwd(), 'assests');
    if (!fs.existsSync(screenshotDir)) {
      fs.mkdirSync(screenshotDir, { recursive: true });
      console.log(`📁 Created directory: ${screenshotDir}`);
    }
    
    // Take screenshot
    const screenshotPath = path.join(screenshotDir, 'website.png');
    console.log('📸 Taking screenshot...');
    await page.screenshot({
      path: screenshotPath,
      fullPage: true,
      quality: 90
    });
    
    console.log(`✅ Screenshot saved successfully to ${screenshotPath}`);
    console.log('🎉 Done! You can now commit this change to update your README.');
  } catch (error) {
    console.error('❌ Error taking screenshot:', error.message);
    process.exit(1);
  } finally {
    await browser.close();
  }
})();
