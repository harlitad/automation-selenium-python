from selenium import webdriver
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time


@pytest.fixture()
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test_alert(driver):
    driver.get("https://demoqa.com/alerts")
    click_button = driver.find_element_by_id("alertButton")
    click_button.click()
    WebDriverWait(driver, 3000).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    assert alert.text == "You clicked a button"
    alert.accept()


def test_alert_with_time(driver):
    driver.get("https://demoqa.com/alerts")
    click_button = driver.find_element_by_id("timerAlertButton")
    click_button.click()
    WebDriverWait(driver, 6000).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    assert alert.text == "This alert appeared after 5 seconds"
    alert.accept()


def test_alert_confirm_ok(driver):
    driver.get("https://demoqa.com/alerts")
    click_button = driver.find_element_by_id("confirmButton")
    click_button.click()
    WebDriverWait(driver, 5000).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()
    result = WebDriverWait(driver, 50000).until(
        EC.visibility_of_element_located((By.ID, "confirmResult")))
    assert result.text == "You selected Ok"


def test_alert_confirm_cancel(driver):
    driver.get("https://demoqa.com/alerts")
    click_button = driver.find_element_by_id("confirmButton")
    click_button.click()
    WebDriverWait(driver, 5000).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.dismiss()
    result = WebDriverWait(driver, 50000).until(
        EC.visibility_of_element_located((By.ID, "confirmResult")))
    assert result.text == "You selected Cancel"


def test_prompt_box(driver):
    driver.get("https://demoqa.com/alerts")
    text = "gak bisa basa engress"
    click_button = driver.find_element_by_id("promtButton")
    click_button.click()
    WebDriverWait(driver, 50000).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.send_keys(text)
    alert.accept()
    result = WebDriverWait(driver, 50000).until(
        EC.visibility_of_element_located((By.ID, "promptResult")))
    assert result.text == "You entered " + text


def test_upload_file(driver):
    driver.get("https://demoqa.com/upload-download")
    button = driver.find_element(By.ID, "uploadFile")
    button.send_keys("/home/harlita/Box/demo-selenium/test_login.py")
    path = WebDriverWait(driver, 3000).until(
        EC.presence_of_element_located((By.ID, "uploadedFilePath")))
    assert path.text == "C:\\fakepath\\test_login.py"
    time.sleep(1)


def test_modal_dialogs_small(driver):
    driver.get("https://demoqa.com/modal-dialogs")
    button_modal = driver.find_element(By.ID, "showSmallModal")
    button_modal.click()
    assert driver.find_element(
        By.ID, "example-modal-sizes-title-sm").text == "Small Modal"
    assert driver.find_element(
        By.CLASS_NAME, "modal-body").text == "This is a small modal. It has very less content"
    button_close = driver.find_element(By.ID, "closeSmallModal")
    button_close.click()


def test_autocomplete_multiple_color_name(driver):
    driver.get("https://demoqa.com/auto-complete")
    input = driver.find_element(By.ID, "autoCompleteMultipleInput")
    input.send_keys("yellow")
    input.send_keys(Keys.DOWN)
    input.send_keys(Keys.ENTER)
    assert WebDriverWait(driver, 3000).until(EC.presence_of_element_located(
        (By.ID, "css-12jo7m5 auto-complete__multi-value__label"))).text == "Yellow"
    time.sleep(10)


def test_slider(driver):
    driver.get("https://demoqa.com/slider")
    slider = driver.find_element(
        By.CSS_SELECTOR, ".range-slider.range-slider--primary")
    min_number = int(slider.get_attribute("min"))
    max_number = int(slider.get_attribute("max"))
    default_value = int(slider.get_attribute("value"))
    print("Number Slider: ", min_number, max_number, default_value)
    # # cara 1
    for i in range(min_number + default_value, max_number - 10):
        slider.send_keys(Keys.RIGHT)
    assert driver.find_element(
        By.ID, "sliderValue").get_attribute("value") == "90"
    # # cara 2, tapi susah cari xy -nya
    # action_slide = ActionChains(driver)
    # action_slide.drag_and_drop_by_offset(slider, 0, 0)
    time.sleep(10)


def test_progress_bar(driver):
    driver.get("https://demoqa.com/progress-bar")
    set_value = "50"
    start_stop_button = driver.find_element(By.ID, "startStopButton")
    if start_stop_button.text == "Start":
        start_stop_button.click()
        assert start_stop_button.text == "Stop"
        # driver.implicitly_wait(10)
        time.sleep(5)
        start_stop_button.click()
        assert driver.find_element(
            By.CSS_SELECTOR, ".progress-bar").get_attribute("aria-valuenow") == set_value

def test_accordian(driver):
    driver.get("https://demoqa.com/accordian")
    section1 = driver.find_element(By.ID, "section1Heading")
    section2 = driver.find_element(By.ID, "section2Heading")
    section2.click()
    section2.find_element(By.CSS_SELECTOR, ".collapse.show")