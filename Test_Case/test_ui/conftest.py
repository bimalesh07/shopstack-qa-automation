import os
import pytest
from selenium import webdriver
from dotenv import load_dotenv

load_dotenv()
@pytest.fixture(scope="class")
def setup(request):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    
    if request.cls is not None:
        request.cls.driver = driver 
        
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def fresh_url(request, setup):
    if hasattr(request.cls, 'driver') and request.cls.driver is not None:
        driver = request.cls.driver
        base_url = os.getenv("SHOPSTACK_BASE_URL", "https://shopstack-ecommerce.vercel.app")
        driver.delete_all_cookies()
        driver.get(base_url)
    yield  


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    
    if report.when == "call" or report.when == "setup":
        xfail = hasattr(report, "wasxfail")
        
        if (report.failed and not xfail) or (report.skipped and xfail):
            from pytest_html import extras
            
            file_name = report.nodeid.replace("::", "_").replace(".", "_").replace("/", "_") + ".png"
            screenshot_dir = ".\\Screenshots"
            
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
                
            file_path = os.path.join(screenshot_dir, file_name)
            driver = item.funcargs.get('setup') or (item.cls.driver if hasattr(item, 'cls') and hasattr(item.cls, 'driver') else None)
            
            if driver:
                driver.save_screenshot(file_path)
                print(f"\n UI Failure Saved to: {file_path}")
                
                if os.path.exists(file_path):
                    html = f'<div><img src="..\\Screenshots\\{file_name}" alt="screenshot" style="width:304px;height:228px;" ' \
                           f'onclick="window.open(self.src)" align="right"/></div>'
                    extra.append(extras.html(html))
                    
        report.extra = extra