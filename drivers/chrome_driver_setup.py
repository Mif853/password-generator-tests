from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from utils.config import Config


def get_chrome_driver():
    print("Creating Chrome driver with options:")
    options = Options()
    if Config.HEADLESS_MODE:
        print(" - Headless mode enabled")
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920x1080')

    print(" - Options set: ", options.arguments)

    try:
        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        print("Error creating WebDriver: ", e)
        raise