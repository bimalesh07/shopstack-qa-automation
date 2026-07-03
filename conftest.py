import os
import pytest
import pytest_html

pytest_plugins = [
    "Test_Case.test_database.conftest",
    "Test_Case.test_ui.conftest",
    "Test_Case.test_api.conftest"
]

def pytest_html_report_title(report):
    report.title = "ShopStack Automation Execution Report"

def pytest_configure(config):
    if hasattr(config, '_metadata'):
        config._metadata['Project Name'] = 'ShopStack E-Commerce'
        config._metadata['Tester Name'] = 'Bimalesh Kumar'
        config._metadata['Environment'] = 'QA / Testing'
        
        config._metadata.pop('JAVA_HOME', None)
        config._metadata.pop('Plugins', None)
        config._metadata.pop('Packages', None)
        config._metadata.pop('Platform', None)