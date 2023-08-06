from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.events import AbstractEventListener, EventFiringWebDriver
from selenium.webdriver.support.wait import WebDriverWait

from mpathways_driver.helpers import get_login_messages, mp_switch_to_content, mp_wait
from mpathways_driver.listener import MPathwaysListener

ENTRY_URL = "https://{env}.dsc.umich.edu/services/mpathways"


class MPathwaysDriver(EventFiringWebDriver):
    def mp_login(self, username, password, env="csqa92"):
        """Log into MPathways via 2FA and wait for MPathways to load"""
        driver = self.wrapped_driver
        url = ENTRY_URL.format(env=env.lower())
        driver.get(url)
        driver.find_element_by_id("login").send_keys(username)
        driver.find_element_by_id("password").send_keys(password)
        driver.find_element_by_id("loginSubmit").click()
        # detect login messages - LoginError will be raised if errors present
        get_login_messages(driver)
        # wait for 2FA and for mpathways to finish loading (pt_pageinfo present)
        WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.ID, "pt_pageinfo")))


def make_mp_driver(driver: webdriver.Firefox) -> MPathwaysDriver:
    """Wraps the provided driver with the MPathwaysDriver, returning the wrapped driver"""
    return MPathwaysDriver(driver, MPathwaysListener())


def Chrome(**kwargs) -> MPathwaysDriver:
    """
    Make an MPathways-enabled Chromedriver.

    Kwargs are passed to chrome WebDriver initialization.
    """
    driver = webdriver.Chrome(**kwargs)
    return make_mp_driver(driver)


def Firefox(**kwargs) -> MPathwaysDriver:
    """
    An MPathways-enabled Firefox WebDriver

    Kwargs are passed to chrome WebDriver initialization.
    """
    driver = webdriver.Firefox(**kwargs)
    return make_mp_driver(driver)


def Ie(**kwargs) -> MPathwaysDriver:
    """
    An MPathways-enabled IE WebDriver

    Kwargs are passed to chrome WebDriver initialization.
    """
    driver = webdriver.Ie(**kwargs)
    return make_mp_driver(driver)


def Safari(**kwargs) -> MPathwaysDriver:
    """
        An MPathways-enabled IE WebDriver

        Kwargs are passed to chrome WebDriver initialization.
        """
    driver = webdriver.Safari(**kwargs)
    return make_mp_driver(driver)
