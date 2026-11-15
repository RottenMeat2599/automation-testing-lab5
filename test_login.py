"""Laboratory 5: independent UI checks against the live SauceDemo site."""

from playwright.sync_api import Page, expect

BASE_URL = "https://www.saucedemo.com/"


def login(page: Page, password: str = "secret_sauce"):
    page.goto(BASE_URL)
    page.locator('[data-test="username"]').fill("standard_user")
    page.locator('[data-test="password"]').fill(password)
    page.locator('[data-test="login-button"]').click()


def test_login_page_is_displayed(page: Page):
    page.goto(BASE_URL)
    expect(page.locator('[data-test="username"]')).to_be_visible()
    expect(page.locator('[data-test="password"]')).to_be_visible()
    expect(page.locator('[data-test="login-button"]')).to_be_visible()


def test_successful_login(page: Page):
    login(page)
    expect(page).to_have_url(BASE_URL + "inventory.html")
    expect(page.locator('[data-test="inventory-container"]')).to_be_visible()


def test_add_product_to_cart(page: Page):
    login(page)
    expect(page.locator('[data-test="inventory-container"]')).to_be_visible()
    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_text("1")
    page.locator('[data-test="shopping-cart-link"]').click()
    expect(page).to_have_url(BASE_URL + "cart.html")
    expect(page.locator('[data-test="inventory-item"]')).to_have_count(1)
    expect(page.locator('[data-test="inventory-item-name"]')).to_have_text(
        "Sauce Labs Backpack"
    )


def test_login_with_invalid_password(page: Page):
    login(page, "wrong_password")
    expect(page.locator('[data-test="error"]')).to_be_visible()
    expect(page.locator('[data-test="error"]')).to_contain_text(
        "Username and password do not match"
    )
    expect(page).to_have_url(BASE_URL)
