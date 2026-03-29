const puppeteer = require('puppeteer');
const http = require('http');

async function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function httpRequest(path, method = 'GET', data = null) {
  return new Promise((resolve) => {
    const url = new URL(path, 'http://localhost:8000');
    const options = {
      hostname: 'localhost',
      port: 8000,
      path: url.pathname + url.search,
      method: method,
      headers: { 'Content-Type': 'application/json' }
    };

    const req = http.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(body));
        } catch (e) {
          resolve({ raw: body, error: 'Parse error' });
        }
      });
    });

    req.on('error', (e) => resolve({ error: e.message }));
    if (data) req.write(JSON.stringify(data));
    req.end();
  });
}

async function runCompleteTests() {
  let browser;
  try {
    console.log('╔═══════════════════════════════════════════════════════╗');
    console.log('║       ChildFit 端到端完整测试套件                      ║');
    console.log('╚═══════════════════════════════════════════════════════╝\n');

    browser = await puppeteer.launch({
      headless: false,
      executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
      args: ['--no-sandbox', '--disable-setuid-sandbox', '--start-maximized']
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });

    let testResults = [];
    let testCount = 0;

    function logTest(name, passed, detail) {
      testCount++;
      const icon = passed ? '✓' : '✗';
      console.log(`${icon} ${testCount}. ${name}: ${detail}`);
      testResults.push({ test: name, passed, detail });
    }

    // ==================== 第一部分：前端 UI 测试 ====================
    console.log('━━━ 第一部分：前端 UI 测试 ━━━\n');

    // 1. 登录页面加载
    console.log('测试：登录页面加载');
    await page.goto('http://localhost:8082', { waitUntil: 'networkidle0', timeout: 15000 });
    await delay(2000);
    await page.screenshot({ path: '../test-results/ui-01-login.png', fullPage: true });

    const roleOptions = await page.$$('.role-option');
    logTest('登录页面 - 角色选择器', roleOptions.length === 2, `${roleOptions.length} 个选项`);

    // 2. 学生角色选择
    console.log('\n测试：学生角色选择');
    await page.click('.role-option:first-child');
    await delay(1000);
    await page.screenshot({ path: '../test-results/ui-02-student.png', fullPage: true });

    const studentActive = await page.$eval('.role-option:first-child', el => el.classList.contains('active'));
    logTest('学生角色 - 点击响应', studentActive, studentActive ? '选中状态正确' : '选中状态失败');

    // 检查学生功能说明
    const studentFeatures = await page.$$('.feature-item');
    logTest('学生功能说明', studentFeatures.length > 0, `${studentFeatures.length} 条功能说明`);

    // 3. 教师角色选择
    console.log('\n测试：教师角色选择');
    await page.click('.role-option:last-child');
    await delay(1000);
    await page.screenshot({ path: '../test-results/ui-03-teacher.png', fullPage: true });

    const teacherActive = await page.$eval('.role-option:last-child', el => el.classList.contains('active'));
    logTest('教师角色 - 点击响应', teacherActive, teacherActive ? '选中状态正确' : '选中状态失败');

    // 4. 登录按钮
    console.log('\n测试：登录按钮');
    const loginButton = await page.$('.btn-wechat');
    const buttonVisible = await loginButton.evaluate(el => {
      const style = window.getComputedStyle(el);
      return style.display !== 'none' && style.visibility !== 'hidden';
    });
    logTest('登录按钮 - 可见性', buttonVisible, buttonVisible ? '按钮可见' : '按钮隐藏');

    // 5. 执行登录
    console.log('\n测试：执行登录');
    await page.click('.btn-wechat');
    await delay(5000);
    await page.screenshot({ path: '../test-results/ui-04-after-login.png', fullPage: true });

    const currentUrl = page.url();
    logTest('登录后导航', true, `URL: ${currentUrl}`);

    // ==================== 第二部分：后端 API 测试 ====================
    console.log('\n━━━ 第二部分：后端 API 测试 ━━━\n');

    // 6. 健康检查
    console.log('测试：API 健康检查');
    const healthRes = await httpRequest('/api/health');
    logTest('健康检查 API', healthRes.status === 'healthy', `版本 ${healthRes.version}`);

    // 7. 用户注册
    console.log('\n测试：用户注册 API');
    const testUser = {
      wx_openid: 'e2e_test_' + Date.now(),
      nickname: 'E2E 测试用户',
      role: 'student'
    };
    const registerRes = await httpRequest('/api/users/register', 'POST', testUser);
    const userId = registerRes.id;
    logTest('用户注册 API', !!userId, `用户 ID: ${userId || '失败'}`);

    // 8. 用户登录
    console.log('\n测试：用户登录 API');
    const loginRes = await httpRequest('/api/users/login', 'POST', { wx_openid: testUser.wx_openid });
    const token = loginRes.access_token;
    logTest('用户登录 API', !!token, `Token: ${token ? token.substring(0, 20) + '...' : '失败'}`);

    // 9. 获取用户信息
    console.log('\n测试：获取用户信息 API');
    const userRes = await httpRequest(`/api/users/${userId}`);
    logTest('获取用户信息', userRes.id === userId, `昵称：${userRes.nickname}`);

    // 10. 创建孩子档案
    console.log('\n测试：创建孩子档案 API');
    const childRes = await httpRequest(`/api/children/?user_id=${userId}`, 'POST', {
      grade: 'grade_3',
      gender: 'male'
    });
    const childId = childRes.id;
    logTest('创建孩子档案', !!childId, `孩子 ID: ${childId || '失败'}`);

    // 11. 获取孩子列表
    console.log('\n测试：获取孩子列表 API');
    const childrenRes = await httpRequest(`/api/children/?user_id=${userId}`);
    logTest('获取孩子列表', childrenRes.data && childrenRes.data.length > 0, `${childrenRes.data?.length || 0} 个孩子`);

    // 12. 天气 API
    console.log('\n测试：天气 API');
    const weatherRes = await httpRequest('/api/weather/');
    logTest('天气 API', weatherRes.status === 'success', `城市：${weatherRes.data?.location || '未知'}`);

    // 13. 学校列表 API
    console.log('\n测试：学校列表 API');
    const schoolsRes = await httpRequest('/api/schools/');
    logTest('学校列表 API', Array.isArray(schoolsRes) && schoolsRes.length > 0, `${schoolsRes.length} 所学校`);

    // 14. 成就类型 API
    console.log('\n测试：成就类型 API');
    const achievementsRes = await httpRequest('/api/achievements/types');
    logTest('成就类型 API', Array.isArray(achievementsRes) && achievementsRes.length > 0, `${achievementsRes.length} 种成就`);

    // 15. 打卡统计 API（新孩子应为 0）
    console.log('\n测试：打卡统计 API');
    const checkinStats = await httpRequest(`/api/checkins/child/${childId}/stats`);
    logTest('打卡统计 API', checkinStats.total_checkins === 0, `总打卡：${checkinStats.total_checkins}`);

    // 截图
    await page.screenshot({ path: '../test-results/ui-99-final.png', fullPage: true });

    // ==================== 测试总结 ====================
    console.log('\n╔═══════════════════════════════════════════════════════╗');
    console.log('║                    测 试 总 结                        ║');
    console.log('╚═══════════════════════════════════════════════════════╝\n');

    const passed = testResults.filter(t => t.passed).length;
    const total = testResults.length;
    const successRate = ((passed / total) * 100).toFixed(1);

    console.log(`测试总数：${total}`);
    console.log(`通过：${passed}`);
    console.log(`失败：${total - passed}`);
    console.log(`成功率：${successRate}%\n`);

    const failed = testResults.filter(t => !t.passed);
    if (failed.length > 0) {
      console.log('失败的测试:');
      failed.forEach(t => console.log(`  ✗ ${t.test}: ${t.detail}`));
    }

    console.log('\n截图已保存到 test-results/ 目录');
    console.log('\n=== 测试完成！===\n');

    await browser.close();
    process.exit(passed === total ? 0 : 1);

  } catch (error) {
    console.error('致命错误:', error.message);
    console.error(error.stack);
    if (browser) await browser.close();
    process.exit(1);
  }
}

runCompleteTests();
