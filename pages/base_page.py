from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator, timeout=10):
        """Find an element on the page, waiting until it is visible."""
        try:
            return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            return None

    def find_elements(self, locator, timeout=10):
        """Find all elements on the page, waiting until they are visible."""
        try:
            return WebDriverWait(self.driver, timeout).until(EC.visibility_of_all_elements_located(locator))
        except TimeoutException:
            return []

    def click_element(self, locator, timeout=10):
        """Click on an element once it becomes clickable."""
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
            element.click()
        except TimeoutException:
            print(f"Element with locator {locator} not clickable.")

    def input_text(self, locator, text, timeout=10):
        """Enter text into an input field, waiting until it is available."""
        try:
            element = self.find_element(locator, timeout)
            element.clear()
            element.send_keys(text)
        except TimeoutException:
            print(f"Cannot input text into element with locator {locator}.")

    def is_element_present(self, locator, timeout=10):
        """Check if an element is present on the page."""
        try:
            self.find_element(locator, timeout)
            return True
        except NoSuchElementException:
            return False

    def is_element_visible(self, locator, timeout=10):
        """Check if an element is visible on the page."""
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return element.is_displayed()
        except TimeoutException:
            return False

    def get_element_text(self, locator, timeout=10):
        """Get the text of an element."""
        element = self.find_element(locator, timeout)
        if element and element.tag_name == "input":
            return element.get_attribute('value')
        return element.text if element else ""

    def scroll_to_element(self, locator):
        """Scroll the page to an element."""
        element = self.find_element(locator)
        if element:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
