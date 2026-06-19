# 👉 File Location: conftest.py (Main Project Root Folder - Sabse Bahar)
import os
import pytest
import pytest_html

# =====================================================================================
# 🛠️ PLUGINS INCLUSION: Baki folders ke fixtures ko globally jodna
# =====================================================================================
pytest_plugins = [
    "Test_Case.test_database.conftest",  # Database wale fixtures ka rasta
    "Test_Case.test_ui.conftest" ,
    "Test_Case.test_api.conftest"        # UI wale fixtures ka rasta
]

# =====================================================================================
# 🎨 GLOBAL HOOK: HTML REPORT HEADERS & METADATA CUSTOMIZATION (Sabke Liye Common)
# =====================================================================================
def pytest_html_report_title(report):
    """Pure project ki report ka master title"""
    report.title = "ShopStack Automation Execution Report"

def pytest_configure(config):
    """HTML Report ke metadata dashboard ko customize karna"""
    if hasattr(config, '_metadata'):
        config._metadata['Project Name'] = 'ShopStack E-Commerce'
        config._metadata['Tester Name'] = 'Bimalesh Kumar'
        config._metadata['Environment'] = 'QA / Testing'
        
        # ❌ REPORT SE FALTU KACHRA METADATA HATANE KE LIYE
        config._metadata.pop('JAVA_HOME', None)
        config._metadata.pop('Plugins', None)
        config._metadata.pop('Packages', None)
        config._metadata.pop('Platform', None)