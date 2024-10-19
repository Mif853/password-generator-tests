import time

import pytest
from pages.password_page import PasswordPage
from drivers.chrome_driver_setup import get_chrome_driver


@pytest.fixture(scope="session")
def driver():
    driver = get_chrome_driver()
    yield driver
    driver.quit()


@pytest.fixture(autouse=True)
def setup_page(driver):
    return PasswordPage(driver)


class TestPasswordGenerator:
    def test_default_password_generated(self, setup_page):
        assert setup_page.get_generated_password(), "Password should be generated on page load"

    def test_initial_checkbox_states(self, setup_page):
        """Test that by default, lowercase and uppercase are selected, numbers and symbols are not."""
        password = setup_page.get_generated_password()
        assert any(c.islower() for c in password), "Password should contain lowercase letters"
        assert any(c.isupper() for c in password), "Password should contain uppercase letters"

    def test_only_lowercase_enabled(self, setup_page):
        setup_page.select_password_options(lowercase=True, uppercase=False, numbers=False, symbols=False)
        password = setup_page.get_generated_password()
        assert any(c.isupper() for c in password), "Password should contain uppercase letters"

    def test_only_uppercase_enabled(self, setup_page):
        setup_page.select_password_options(lowercase=False, uppercase=True, numbers=False, symbols=False)
        password = setup_page.get_generated_password()
        assert any(c.islower() for c in password), "Password should contain lowercase letters"

    def test_only_numbers_enabled(self, setup_page):
        setup_page.click_checkboxes(numbers=True)
        setup_page.click_checkboxes(uppercase=True)
        setup_page.click_checkboxes(lowercase=True)
        password = setup_page.get_generated_password()
        assert all(char.isdigit() for char in password), "Password should contain only digits"

    def test_only_symbols_enabled(self, setup_page):
        setup_page.click_checkboxes(symbols=True)
        setup_page.click_checkboxes(lowercase=True)
        setup_page.click_checkboxes(uppercase=True)
        password = setup_page.get_generated_password()
        assert all(not c.isalnum() for c in password), "Password should contain only symbols"

    def test_all_options_enabled(self, setup_page):
        setup_page.select_password_options(lowercase=False, uppercase=False, numbers=True, symbols=True)
        password = setup_page.get_generated_password()
        assert any(c.islower() for c in password), "Password should contain lowercase letters"
        assert any(c.isupper() for c in password), "Password should contain uppercase letters"
        assert any(c.isdigit() for c in password), "Password should contain digits"
        assert any(not c.isalnum() for c in password), "Password should contain special characters"

    def test_no_options_enabled(self, setup_page):
        setup_page.select_password_options(lowercase=True, uppercase=True, numbers=False, symbols=False)
        assert setup_page.get_generated_password(), "Password should be generated when no options are selected"

    def test_password_length_adjustment(self, setup_page):
        expected_length = 20
        setup_page.clear_element(setup_page.LENGTH_INPUT)
        setup_page.set_password_length(expected_length)

        setup_page.generate_password()
        generated_password = setup_page.get_generated_password()
        assert len(
            generated_password) == expected_length, f"Generated password length should match the set value. Got {len(generated_password)}"

    def test_minimum_password_length(self, setup_page):
        min_length = 6
        setup_page.clear_element(setup_page.LENGTH_INPUT)
        setup_page.set_password_length(min_length)
        assert len(
            setup_page.get_generated_password()) == min_length, "Generated password length should match minimum allowed"

    def test_maximum_password_length(self, setup_page):
        max_length = 32
        setup_page.clear_element(setup_page.LENGTH_INPUT)
        setup_page.set_password_length(max_length)
        assert len(
            setup_page.get_generated_password()) == max_length, "Generated password length should match maximum allowed"

    def test_copy_password_button_functionality(self, setup_page):
        setup_page.generate_password()
        password_before_copy = setup_page.get_generated_password()
        assert setup_page.copy_password_button() == password_before_copy, ("Copied password should match the "
                                                                           "generated password")

    def test_copy_password_icon_functionality(self, setup_page):
        setup_page.generate_password()
        password_before_copy = setup_page.get_generated_password()
        assert password_before_copy == setup_page.copy_password_icon(), ("Copied password with icon should match "
                                                                             "the generated password")

    def test_input_negative_length(self, setup_page):
        default_length = 6
        setup_page.clear_element(setup_page.LENGTH_INPUT)
        setup_page.input_text(setup_page.LENGTH_INPUT, '-1')
        assert len(
            setup_page.get_generated_password()) == default_length, "Password should not be generated with negative length"

    def test_input_excessive_length(self, setup_page):
        excessive_length = '100'
        setup_page.clear_element(setup_page.LENGTH_INPUT)
        setup_page.input_text(setup_page.LENGTH_INPUT, excessive_length)
        assert len(setup_page.get_generated_password()) != int(
            excessive_length), "Password length should not exceed the maximum limit"

    def test_input_below_minimum_length(self, setup_page):
        """Test that setting the password length below the minimum defaults to the minimum."""
        setup_page.clear_element(setup_page.LENGTH_INPUT)
        setup_page.set_password_length(5)
        setup_page.generate_password()
        assert len(
            setup_page.get_generated_password()) == 6, "Password length should default to minimum (6) when set below it"

    def test_input_above_maximum_length(self, setup_page):
        """Test that setting the password length above the maximum defaults to the maximum."""
        setup_page.clear_element(setup_page.LENGTH_INPUT)
        setup_page.set_password_length(33)
        setup_page.generate_password()
        assert len(
            setup_page.get_generated_password()) == 32, ("Password length should default to maximum (32) when set "
                                                         "above it")
