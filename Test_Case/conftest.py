# 👉 File: conftest.py (Project Root Folder)
import os
import time
import pytest
from selenium import webdriver
from dotenv import load_dotenv

load_dotenv()

# BROWSER SETUP FIXTURE
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
    print("\n🛑 --- [BROWSER CLOSE] Destroying Driver Context ---")
    driver.quit()

@pytest.fixture(scope="function", autouse=True)
def fresh_url(request):
    if hasattr(request.cls, 'driver'):
        base_url = os.getenv("SHOPSTACK_BASE_URL", "https://shopstack-ecommerce.vercel.app")
        request.cls.driver.delete_all_cookies()
        request.cls.driver.get(base_url)





# 🚨 HOOK 1: AUTOMATIC SCREENSHOT ON FAILURE & ATTACH TO HTML REPORT
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Agar koi test fail hoga, toh screenshot lekar use html report me jodh dega"""
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    
    if report.when == "call" or report.when == "setup":
        xfail = hasattr(report, "wasxfail")
        # Check agar test fail hua hai (and it's not expected to fail)
        if (report.failed and not xfail) or (report.skipped and xfail):
            file_name = report.nodeid.replace("::", "_").replace(".", "_").replace("/", "_") + ".png"
            # Folder check/create karna
            screenshot_dir = ".\\Screenshots"
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
                
            file_path = os.path.join(screenshot_dir, file_name)
            
            # Fixture se driver nikalna
            driver = item.funcargs.get('setup') or (item.cls.driver if hasattr(item, 'cls') and hasattr(item.cls, 'driver') else None)
            
            if driver:
                driver.save_screenshot(file_path)
                print(f"\n📸 [SCREENSHOT CAPTURED] Saved to: {file_path}")
                
                # HTML Report me image embed karne ka code
                if os.path.exists(file_path):
                    html = f'<div><img src="..\\Screenshots\\{file_name}" alt="screenshot" style="width:304px;height:228px;" ' \
                           f'onclick="window.open(self.src)" align="right"/></div>'
                    extra.append(pytest_html.extras.html(html))
        report.extra = extra

# 📊 HOOK 2: HTML REPORT HEADERS CUSTOMIZE KARNA (Add metadata)
def pytest_html_report_title(report):
    report.title = "ShopStack Automation Execution Report"
def pytest_configure(config):
    # Agar report plugin active hai, toh customize karo metadata
    if hasattr(config, '_metadata'):
        config._metadata['Project Name'] = 'ShopStack E-Commerce'
        config._metadata['Tester Name'] = 'Bimalesh Kumar'
        config._metadata['Environment'] = 'QA / Testing'
        
        # ❌ IGNORE/REMOVE FALTU METADATA (Jo tumne kaha ignore karne ko)
        # Yeh report se machine name, python version wagera ka kachra mita dega
        config._metadata.pop('JAVA_HOME', None)
        config._metadata.pop('Plugins', None)
        config._metadata.pop('Packages', None)
        config._metadata.pop('Platform', None)

# Import handling for hook inside reporting
import pytest_html