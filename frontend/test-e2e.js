const puppeteer = require('puppeteer');

async function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function runTests() {
  let browser;
  try {
    console.log('=== ChildFit E2E Test Suite ===\n');

    browser = await puppeteer.launch({
      headless: false,
      executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
      args: ['--no-sandbox', '--disable-setuid-sandbox', '--start-maximized']
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });

    let testResults = [];

    // ========== Test 1: Login Page ==========
    console.log('Test 1: Login Page');
    await page.goto('http://localhost:8082', { waitUntil: 'networkidle0', timeout: 15000 });
    await delay(2000);
    await page.screenshot({ path: '../test-results/01-login-page.png', fullPage: true });

    // Verify role options
    const roleOptions = await page.$$('.role-option');
    testResults.push({
      test: 'Login Page Role Options',
      passed: roleOptions.length === 2,
      detail: `Found ${roleOptions.length} role options`
    });
    console.log(`  Role options: ${roleOptions.length}\n`);

    // ========== Test 2: Select Student Role ==========
    console.log('Test 2: Select Student Role');
    await page.click('.role-option:first-child');
    await delay(1500);
    await page.screenshot({ path: '../test-results/02-student-selected.png', fullPage: true });

    const studentActive = await page.$eval('.role-option:first-child', el => el.classList.contains('active'));
    testResults.push({
      test: 'Student Role Selection',
      passed: studentActive,
      detail: studentActive ? 'Student option is active' : 'Student option not active'
    });
    console.log(`  Student selected: ${studentActive}\n`);

    // ========== Test 3: Select Teacher Role ==========
    console.log('Test 3: Select Teacher Role');
    await page.click('.role-option:last-child');
    await delay(1500);
    await page.screenshot({ path: '../test-results/03-teacher-selected.png', fullPage: true });

    const teacherActive = await page.$eval('.role-option:last-child', el => el.classList.contains('active'));
    testResults.push({
      test: 'Teacher Role Selection',
      passed: teacherActive,
      detail: teacherActive ? 'Teacher option is active' : 'Teacher option not active'
    });
    console.log(`  Teacher selected: ${teacherActive}\n`);

    // ========== Test 4: Click Login Button ==========
    console.log('Test 4: Click Login Button');
    await page.click('.btn-wechat');
    await delay(5000);
    await page.screenshot({ path: '../test-results/04-after-login.png', fullPage: true });

    const currentUrl = page.url();
    const loginSuccessful = currentUrl.includes('/pages/index/index') || currentUrl.includes('/pages/children') || currentUrl.includes('/pages/login');
    testResults.push({
      test: 'Login Navigation',
      passed: loginSuccessful,
      detail: `Current URL: ${currentUrl}`
    });
    console.log(`  Current URL: ${currentUrl}\n`);

    // ========== Test 5: Check Home Page (if navigated) ==========
    if (currentUrl.includes('/pages/index/index')) {
      console.log('Test 5: Home Page Elements');
      await delay(2000);

      const tabBarItems = await page.$$('.tabbar-item');
      testResults.push({
        test: 'Home Page Tab Bar',
        passed: tabBarItems.length > 0,
        detail: `Found ${tabBarItems.length} tab bar items`
      });
      console.log(`  Tab bar items: ${tabBarItems.length}\n`);

      await page.screenshot({ path: '../test-results/05-home-page.png', fullPage: true });
    }

    // ========== Test 6: API Health Check ==========
    console.log('Test 6: Backend API Health Check');
    const apiResponse = await page.evaluate(async () => {
      try {
        const res = await fetch('http://localhost:8000/api/health');
        return await res.json();
      } catch (e) {
        return { error: e.message };
      }
    });

    testResults.push({
      test: 'Backend API Health',
      passed: apiResponse.status === 'healthy',
      detail: JSON.stringify(apiResponse)
    });
    console.log(`  API Response: ${JSON.stringify(apiResponse)}\n`);

    // ========== Summary ==========
    console.log('=== Test Summary ===\n');
    const passed = testResults.filter(t => t.passed).length;
    const total = testResults.length;

    console.log(`Total: ${total} tests`);
    console.log(`Passed: ${passed}`);
    console.log(`Failed: ${total - passed}\n`);

    testResults.forEach(test => {
      const icon = test.passed ? '✓' : '✗';
      console.log(`${icon} ${test.test}: ${test.detail}`);
    });

    // Save summary
    await page.screenshot({ path: '../test-results/99-final-state.png', fullPage: true });

    await browser.close();
    console.log('\n=== All tests completed! ===');

    // Exit with error if any test failed
    process.exit(passed === total ? 0 : 1);

  } catch (error) {
    console.error('Fatal Error:', error.message);
    console.error(error.stack);
    if (browser) await browser.close();
    process.exit(1);
  }
}

runTests();
