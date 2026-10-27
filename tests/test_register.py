
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def setup_teardown():
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install())
    )
    driver.maximize_window()
    yield driver
    driver.quit()


def get_alert_text(driver):
    WebDriverWait(driver, 5).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    text = alert.text
    alert.accept()
    return text


def test_empty_name(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5001/")

    driver.find_element(By.ID, "n").clear()
    driver.find_element(By.ID, "pw").send_keys("testpass")
    driver.find_element(By.ID, "submit").click()

    alert_text = get_alert_text(driver)
    assert alert_text == "Username cannot be empty"


def test_empty_password(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5001/")

    driver.find_element(By.ID, "n").send_keys("testuser")
    driver.find_element(By.ID, "pw").clear()
    driver.find_element(By.ID, "submit").click()

    alert_text = get_alert_text(driver)
    assert alert_text == "Password cannot be empty"


def test_short_password(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5001/")

    driver.find_element(By.ID, "n").send_keys("testuser")
    driver.find_element(By.ID, "pw").send_keys("123")
    driver.find_element(By.ID, "submit").click()

    alert_text = get_alert_text(driver)
    assert alert_text == "Password must be at least 6 chars"


def test_valid_registration(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5001/")

    driver.find_element(By.ID, "n").send_keys("testuser")
    driver.find_element(By.ID, "pw").send_keys("testpassword")
    driver.find_element(By.ID, "submit").click()

    WebDriverWait(driver, 5).until(
        EC.url_contains("/register")
    )

    curr_url = driver.current_url
    assert "/register" in curr_url, (
        f"Expected /register, but got {curr_url}"
    )

    body = driver.find_element(By.TAG_NAME, "body").text
    assert "Registration Successful" in body, (
        "Expected message not found"
    )
