# 👉 File Location: Test_Case/test_ui/conftest.py (Sirf UI Folder Ke Andar)
import os
import pytest
import pytest_html
from selenium import webdriver
from dotenv import load_dotenv

load_dotenv()

# =====================================================================================
# 🌐 BROWSER SETUP FIXTURES (Exclusive for UI)
# =====================================================================================
@pytest.fixture(scope="class")
def setup(request):
    print("\n🚀 --- [BROWSER START] Initializing Chrome Driver Context ---")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    
    if request.cls is not None:
        request.cls.driver = driver
        
    yield driver
    print("\n[BROWSER CLOSE] Destroying Driver Context ---")
    driver.quit()

@pytest.fixture(scope="function", autouse=True)
def fresh_url(request):
    if hasattr(request.cls, 'driver'):
        base_url = os.getenv("SHOPSTACK_BASE_URL", "https://shopstack-ecommerce.vercel.app")
        request.cls.driver.delete_all_cookies()
        request.cls.driver.get(base_url)


# =====================================================================================
# 📸 LOCAL HOOK: AUTOMATIC SCREENSHOT ON FAILURE (Sirf UI Fails ke liye)
# =====================================================================================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Agar UI test fail hoga, toh yeh hook automatic screenshot lekar report mein jod dega"""
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    
    if report.when == "call" or report.when == "setup":
        xfail = hasattr(report, "wasxfail")
        
        # Check agar test fail hua hai
        if (report.failed and not xfail) or (report.skipped and xfail):
            file_name = report.nodeid.replace("::", "_").replace(".", "_").replace("/", "_") + ".png"
            screenshot_dir = ".\\Screenshots"
            
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
                
            file_path = os.path.join(screenshot_dir, file_name)
            
            # Fixture se ya class context se driver nikalna
            driver = item.funcargs.get('setup') or (item.cls.driver if hasattr(item, 'cls') and hasattr(item.cls, 'driver') else None)
            
            if driver:
                driver.save_screenshot(file_path)
                print(f"\n📸 [SCREENSHOT CAPTURED] UI Failure Saved to: {file_path}")
                
                # HTML Report me image embed karne ka code
                if os.path.exists(file_path):
                    html = f'<div><img src="..\\Screenshots\\{file_name}" alt="screenshot" style="width:304px;height:228px;" ' \
                           f'onclick="window.open(self.src)" align="right"/></div>'
                    extra.append(pytest_html.extras.html(html))
                    
        report.extra = extra