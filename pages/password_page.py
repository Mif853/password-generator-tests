import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from .base_page import BasePage
import pyperclip


class PasswordPage(BasePage):
    PASSWORD_INPUT = (By.ID, "password")
    GENERATE_BUTTON = (By.XPATH, "//button[@title='Generate password']")
    LENGTH_SLIDER = (By.ID, "passwordLengthRange")
    LENGTH_INPUT = (By.ID, "passwordLength")
    LOWERCASE_CHECKBOX = (By.CSS_SELECTOR, "[for='option-lowercase']")
    UPPERCASE_CHECKBOX = (By.CSS_SELECTOR, "[for='option-uppercase']")
    NUMBERS_CHECKBOX = (By.CSS_SELECTOR, "[for='option-numbers']")
    SYMBOLS_CHECKBOX = (By.CSS_SELECTOR, "[for='option-symbols']")
    COPY_PASSWORD_ICON = (By.CSS_SELECTOR, "button[title='Copy password']")
    COPY_PASSWORD_BUTTON = (By.CSS_SELECTOR, "button[title='Copy Password']")
    CHECKBOX_LOCATOR = (By.CSS_SELECTOR, '[type="checkbox"]')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get("https://www.security.org/password-generator/")

    def wait_for_element(self, locator, timeout=10):
        """Wait for element to be visible on the page."""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def clear_element(self, locator, timeout=10):
        """Clear the input field before entering new value."""
        element = self.find_element(locator, timeout)
        if element:
            self.driver.execute_script("arguments[0].value = '';", element)

    def set_password_length(self, length):
        """Set the password length using the slider and input."""
        self.wait_for_element(self.COPY_PASSWORD_BUTTON)  # Wait for input field to be visible
        self.input_text(self.LENGTH_INPUT, str(length))
        self.driver.execute_script("arguments[0].value = arguments[1];", self.find_element(self.LENGTH_SLIDER), length)

    def toggle_option(self, locator, expected_state):
        """
        Toggle an option for generating passwords based on the expected state.

        :param locator: The locator of the checkbox element.
        :param expected_state: True if the checkbox should be selected, False if it should be deselected.
        """
        checkbox = self.wait_for_element(locator)
        if checkbox:
            is_selected = checkbox.is_selected()
            if expected_state != is_selected:
                checkbox.click()

    def generate_password(self):
        """Click the generate button to produce a new password."""
        self.wait_for_element(self.GENERATE_BUTTON)  # Wait for the button to be visible
        self.click_element(self.GENERATE_BUTTON)

    def get_generated_password(self):
        """Retrieve the generated password from the input field."""
        return self.get_element_text(self.PASSWORD_INPUT)

    def select_password_options(self, lowercase=True, uppercase=True, numbers=True, symbols=True):
        """Select or deselect options for the password generation."""
        self.toggle_option(self.LOWERCASE_CHECKBOX, lowercase)
        self.toggle_option(self.UPPERCASE_CHECKBOX, uppercase)
        self.toggle_option(self.NUMBERS_CHECKBOX, numbers)
        self.toggle_option(self.SYMBOLS_CHECKBOX, symbols)

    def is_option_selected(self, locator):
        """Check if a given option is selected using 'checked' property."""
        checkbox = self.find_element(locator)
        return checkbox.get_property('checked') == 'true'

    def is_any_option_enabled(self):
        """Check if at least one password option is selected."""
        return any([
            self.find_element(self.LOWERCASE_CHECKBOX).is_selected(),
            self.find_element(self.UPPERCASE_CHECKBOX).is_selected(),
            self.find_element(self.NUMBERS_CHECKBOX).is_selected(),
            self.find_element(self.SYMBOLS_CHECKBOX).is_selected()
        ])

    def copy_password_button(self):
        """Copy the current password to the clipboard."""
        copy_button = self.wait_for_element(self.COPY_PASSWORD_BUTTON)
        copy_button.click()
        return pyperclip.paste()

    def copy_password_icon(self):
        """Copy the current password to the clipboard."""
        copy_button = self.wait_for_element(self.COPY_PASSWORD_ICON)
        copy_button.click()
        return pyperclip.paste()

    def click_checkboxes(self, lowercase=None, uppercase=None, numbers=None, symbols=None):
        """
        Clicks on the specified checkboxes based on provided boolean values. If a value is None, the checkbox will not be toggled.

        :param lowercase: True to click, False to leave untouched, None to ignore the 'Lowercase' checkbox.
        :param uppercase: True to click, False to leave untouched, None to ignore the 'Uppercase' checkbox.
        :param numbers: True to click, False to leave untouched, None to ignore the 'Numbers' checkbox.
        :param symbols: True to click, False to leave untouched, None to ignore the 'Symbols' checkbox.
        """
        # Dictionary mapping checkbox settings to their respective locators and desired actions
        checkbox_settings = {
            'lowercase': (self.LOWERCASE_CHECKBOX, lowercase),
            'uppercase': (self.UPPERCASE_CHECKBOX, uppercase),
            'numbers': (self.NUMBERS_CHECKBOX, numbers),
            'symbols': (self.SYMBOLS_CHECKBOX, symbols),
        }

        for key, (locator, action) in checkbox_settings.items():
            if action is not None:
                checkbox_label = self.wait_for_element(locator)
                if action:
                    checkbox_label.click()

