
class Config:
    # URL of the application to be tested
    BASE_URL = "https://www.security.org/password-generator/"

    # Browser settings
    BROWSER = "Chrome"  # Options: "Chrome", "Firefox", "Safari", etc.

    # Wait times
    SHORT_WAIT = 5
    MEDIUM_WAIT = 10
    LONG_WAIT = 15

    # Whether to run the browser in headless mode
    HEADLESS_MODE = False

    # Path to the browser driver, if not using WebDriver Manager
    CHROME_DRIVER_PATH = "drivers/chromedriver"
    FIREFOX_DRIVER_PATH = "drivers/geckodriver"

    # Test data
    MIN_PASSWORD_LENGTH = 6  # Minimum length of password allowed by the generator
    MAX_PASSWORD_LENGTH = 32  # Maximum length of password allowed by the generator

    # Logging
    LOG_FILE = "test_logs.txt"
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

    # Screenshots
    TAKE_SCREENSHOTS = True
    SCREENSHOTS_DIRECTORY = "screenshots/"