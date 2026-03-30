import { test, expect } from '@playwright/test';

test.describe('ChildFit E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:8082');
  });

  test('should load login page', async ({ page }) => {
    await expect(page).toHaveTitle(/ChildFit/);
    await expect(page.locator('h1')).toContainText('ChildFit');
  });

  test('should select role', async ({ page }) => {
    const studentRole = page.locator('.role-option:first-child');
    const teacherRole = page.locator('.role-option:last-child');
    
    await expect(studentRole).toBeVisible();
    await expect(teacherRole).toBeVisible();
    
    await studentRole.click();
    await expect(studentRole).toHaveClass(/active/);
    
    await teacherRole.click();
    await expect(teacherRole).toHaveClass(/active/);
  });

  test('should login with valid credentials', async ({ page }) => {
    await page.fill('input[placeholder*="OpenID"]', 'test123');
    await page.fill('input[placeholder*="昵称"]', '测试用户');
    
    await page.click('.btn-wechat');
    
    // Should navigate to children page after login
    await page.waitForURL(/\/children/);
    await expect(page.locator('h1')).toContainText('孩子档案');
  });

  test('should add a child profile', async ({ page }) => {
    // Login first
    await page.fill('input[placeholder*="OpenID"]', 'test123');
    await page.fill('input[placeholder*="昵称"]', '测试用户');
    await page.click('.btn-wechat');
    await page.waitForURL(/\/children/);
    
    // Click add child button
    await page.click('button:has-text("添加孩子")');
    
    // Fill child info
    await page.fill('input[placeholder*="姓名"]', '小明');
    await page.fill('input[type="date"]', '2020-01-01');
    await page.selectOption('select', 'male');
    await page.fill('input[placeholder*="城市"]', '北京');
    
    // Save
    await page.click('button:has-text("保存")');
    
    // Should navigate to home page
    await page.waitForURL(/\/home/);
    await expect(page.locator('h1')).toContainText('首页');
  });

  test('should display weather card on home page', async ({ page }) => {
    // Login and navigate to home
    await page.fill('input[placeholder*="OpenID"]', 'test123');
    await page.fill('input[placeholder*="昵称"]', '测试用户');
    await page.click('.btn-wechat');
    await page.waitForURL(/\/children/);
    
    // Wait for child selection or navigate directly
    await page.goto('http://localhost:8082/home');
    
    // Check weather card
    await expect(page.locator('.weather-card')).toBeVisible();
  });

  test('should navigate using tab bar', async ({ page }) => {
    // Login first
    await page.fill('input[placeholder*="OpenID"]', 'test123');
    await page.fill('input[placeholder*="昵称"]', '测试用户');
    await page.click('.btn-wechat');
    await page.waitForURL(/\/children/);
    await page.goto('http://localhost:8082/home');
    
    // Test tab navigation
    const tabBarItems = page.locator('.tab-bar-item');
    await expect(tabBarItems).toHaveCount(5);
    
    // Click Plan tab
    await page.click('.tab-bar-item:has-text("计划")');
    await page.waitForURL(/\/plan/);
    
    // Click CheckIn tab
    await page.click('.tab-bar-item:has-text("打卡")');
    await page.waitForURL(/\/checkin/);
    
    // Click Achievements tab
    await page.click('.tab-bar-item:has-text("成就")');
    await page.waitForURL(/\/achievements/);
    
    // Click Profile tab
    await page.click('.tab-bar-item:has-text("我的")');
    await page.waitForURL(/\/profile/);
  });

  test('should logout from profile page', async ({ page }) => {
    // Login first
    await page.fill('input[placeholder*="OpenID"]', 'test123');
    await page.fill('input[placeholder*="昵称"]', '测试用户');
    await page.click('.btn-wechat');
    await page.waitForURL(/\/children/);
    await page.goto('http://localhost:8082/profile');
    
    // Click logout
    await page.click('button:has-text("退出登录")');
    
    // Should handle confirmation and redirect to login
    page.on('dialog', async dialog => {
      expect(dialog.type()).toBe('confirm');
      await dialog.accept();
    });
    
    await page.waitForURL(/\/login/);
  });
});
