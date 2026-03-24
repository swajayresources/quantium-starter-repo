# Anchors pytest rootdir and puts the correct chromedriver on PATH before any test setup.
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def pytest_configure(config):
    """Download chromedriver and prepend its directory to PATH."""
    driver_path = ChromeDriverManager().install()
    driver_dir = os.path.dirname(driver_path)
    os.environ["PATH"] = driver_dir + os.pathsep + os.environ.get("PATH", "")


def pytest_setup_options():
    """Pass headless Chrome options to Dash's browser fixture."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return options
