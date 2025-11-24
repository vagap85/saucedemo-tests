import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture
def browser():
    """Фикстура для создания браузера"""
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)  # headless=True для CI
    yield browser
    browser.close()
    playwright.stop()

@pytest.fixture
def context(browser):
    """Фикстура для создания контекста браузера"""
    context = browser.new_context()
    yield context
    context.close()

@pytest.fixture
def page(context):
    """Фикстура для создания страницы"""
    page = context.new_page()
    yield page
    page.close()

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Аргументы контекста браузера"""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
    }