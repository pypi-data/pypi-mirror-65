from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .exceptions import LoginError


def mp_wait(driver, timeout=30):
    """Wait for the processing spinner to disappear"""
    wait_loc = (By.ID, "processing")
    save_loc = (By.XPATH, "//*[starts-with(@id, 'saveWait')")
    wait = WebDriverWait(driver, timeout)
    wait.until(EC.invisibility_of_element_located(wait_loc))
    wait.until(EC.invisibility_of_element_located(save_loc))


def mp_switch_to_content(driver, frame="TargetContent"):
    """Passively try to switch to the content frame"""
    try:
        driver.switch_to.frame(frame)
    except:
        pass


def get_login_messages(driver):
    """
    Detect error messages on login page and raise a LoginError
    with the first message found.
    """
    messages = []
    # look for alerts
    try:
        el = driver.find_element_by_css_selector("div.alert")
    except NoSuchElementException:
        pass
    else:
        messages.append(el.text.strip())
    # look for field helptext
    helptext_css = ".form-group .help-block:not(.hidden)"
    try:
        els = driver.find_elements_by_css_selector(helptext_css)
    except NoSuchElementException:
        pass
    else:
        for el in els:
            messages.append(el.text.strip())
    if messages:
        raise LoginError(messages)
