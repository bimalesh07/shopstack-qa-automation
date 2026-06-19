# File Location: conftest.py (Main Project Root Folder)
import os
import pytest
import pytest_html

# =====================================================================================
# PLUGINS INCLUSION: Include fixtures from other folders globally
# =====================================================================================
pytest_plugins = [
    "Test_Case.test_database.conftest",  # Database fixtures path
    "Test_Case.test_ui.conftest" ,
    "Test_Case.test_api.conftest"        # UI fixtures path
]

# =====================================================================================
# GLOBAL HOOK: HTML REPORT HEADERS & METADATA CUSTOMIZATION
# =====================================================================================
def pytest_html_report_title(report):
    """Main title of the project report"""
    report.title = "ShopStack Automation Execution Report"

def pytest_configure(config):
    """Customize HTML report metadata dashboard"""
    if hasattr(config, '_metadata'):
        config._metadata['Project Name'] = 'ShopStack E-Commerce'
        config._metadata['Tester Name'] = 'Bimalesh Kumar'
        config._metadata['Environment'] = 'QA / Testing'
        
        # Remove unnecessary metadata from the report
        config._metadata.pop('JAVA_HOME', None)
        config._metadata.pop('Plugins', None)
        config._metadata.pop('Packages', None)
        config._metadata.pop('Platform', None)