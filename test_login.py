import pytest
from playwright.sync_api import Page, expect

# Константы
BASE_URL = "https://www.saucedemo.com"
VALID_USERNAME = "standard_user"
VALID_PASSWORD = "secret_sauce"
LOCKED_USERNAME = "locked_out_user"
INVALID_USERNAME = "invalid_user"
INVALID_PASSWORD = "invalid_password"


class TestLogin:
    """Тесты для функциональности логина"""

    def test_successful_login(self, page: Page):
        """Тест 1: Успешный логин с валидными данными"""
        page.goto(BASE_URL)

        # Заполняем форму логина
        page.locator("[data-test='username']").fill(VALID_USERNAME)
        page.locator("[data-test='password']").fill(VALID_PASSWORD)
        page.locator("[data-test='login-button']").click()

        # Проверяем успешную авторизацию
        expect(page.locator(".title")).to_contain_text("Products")
        expect(page.locator("[data-test='inventory-container']")).to_be_visible()

        # Проверяем URL после логина
        expect(page).to_have_url(f"{BASE_URL}/inventory.html")

    def test_login_with_locked_user(self, page: Page):
        """Тест 2: Логин с заблокированным пользователем"""
        page.goto(BASE_URL)

        # Заполняем форму с заблокированным пользователем
        page.locator("[data-test='username']").fill(LOCKED_USERNAME)
        page.locator("[data-test='password']").fill(VALID_PASSWORD)
        page.locator("[data-test='login-button']").click()

        # Проверяем сообщение об ошибке
        error_message = page.locator("[data-test='error']")
        expect(error_message).to_be_visible()
        expect(error_message).to_contain_text("Sorry, this user has been locked out")

        # Проверяем, что остались на странице логина
        expect(page).to_have_url(BASE_URL + "/")

    def test_login_with_invalid_username(self, page: Page):
        """Тест 3: Логин с невалидным username"""
        page.goto(BASE_URL)

        # Заполняем форму с неверным username
        page.locator("[data-test='username']").fill(INVALID_USERNAME)
        page.locator("[data-test='password']").fill(VALID_PASSWORD)
        page.locator("[data-test='login-button']").click()

        # Проверяем сообщение об ошибке
        error_message = page.locator("[data-test='error']")
        expect(error_message).to_be_visible()
        expect(error_message).to_contain_text(
            "Username and password do not match any user in this service"
        )

    def test_login_with_invalid_password(self, page: Page):
        """Тест 4: Логин с невалидным паролем"""
        page.goto(BASE_URL)

        # Заполняем форму с неверным паролем
        page.locator("[data-test='username']").fill(VALID_USERNAME)
        page.locator("[data-test='password']").fill(INVALID_PASSWORD)
        page.locator("[data-test='login-button']").click()

        # Проверяем сообщение об ошибке
        error_message = page.locator("[data-test='error']")
        expect(error_message).to_be_visible()
        expect(error_message).to_contain_text(
            "Username and password do not match any user in this service"
        )

    def test_login_with_empty_credentials(self, page: Page):
        """Тест 5: Логин с пустыми полями"""
        page.goto(BASE_URL)

        # Нажимаем кнопку логина без заполнения полей
        page.locator("[data-test='login-button']").click()

        # Проверяем сообщение об ошибке
        error_message = page.locator("[data-test='error']")
        expect(error_message).to_be_visible()
        expect(error_message).to_contain_text("Username is required")

    def test_error_message_closing(self, page: Page):
        """Тест 6: Закрытие сообщения об ошибке"""
        page.goto(BASE_URL)

        # Вызываем ошибку
        page.locator("[data-test='login-button']").click()

        # Проверяем, что ошибка отображается
        error_message = page.locator("[data-test='error']")
        expect(error_message).to_be_visible()

        # Закрываем ошибку
        page.locator(".error-button").click()

        # Проверяем, что ошибка скрыта
        expect(error_message).not_to_be_visible()