const puppeteer = require('puppeteer');

(async () => {
  let browser;
  try {
    console.log('Starting Puppeteer with Edge...');
    browser = await puppeteer.launch({
      headless: false,
      executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });

    console.log('Opening login page http://localhost:8082');
    await page.goto('http://localhost:8082', { waitUntil: 'networkidle0', timeout: 15000 });
    await page.screenshot({ path: '../test-results/01-login-page.png', fullPage: true });
    console.log('Screenshot 1: Login page saved');

    // Check role options exist
    const roleOptions = await page.$$('.role-option');
    console.log('Found role options:', roleOptions.length);

    if (roleOptions.length >= 2) {
      // Test student option
      console.log('Clicking student option...');
      await page.click('.role-option:first-child');
      await new Promise(resolve => setTimeout(resolve, 1000));
      await page.screenshot({ path: '../test-results/02-student-selected.png', fullPage: true });
      console.log('Screenshot 2: Student selected saved');

      // Test teacher option
      console.log('Clicking teacher option...');
      await page.click('.role-option:last-child');
      await new Promise(resolve => setTimeout(resolve, 1000));
      await page.screenshot({ path: '../test-results/03-teacher-selected.png', fullPage: true });
      console.log('Screenshot 3: Teacher selected saved');

      // Test login button
      console.log('Clicking login button...');
      await page.click('.btn-wechat');
      await new Promise(resolve => setTimeout(resolve, 3000));
      await page.screenshot({ path: '../test-results/04-login-clicked.png', fullPage: true });
      console.log('Screenshot 4: Login clicked saved');

      // Get current URL
      const currentUrl = page.url();
      console.log('Current URL:', currentUrl);

      // Check if navigation happened
      if (currentUrl.includes('/pages/index/index') || currentUrl.includes('/pages/children')) {
        console.log('Navigation successful!');
        await page.screenshot({ path: '../test-results/05-after-login.png', fullPage: true });
      }
    } else {
      console.log('Role options not found!');
    }

    await browser.close();
    console.log('=== Test completed successfully! ===');
  } catch (error) {
    console.error('Error:', error.message);
    console.error(error.stack);
    if (browser) await browser.close();
    process.exit(1);
  }
})();
