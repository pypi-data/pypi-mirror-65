from selenium.webdriver.support.events import AbstractEventListener

from mpathways_driver.helpers import mp_switch_to_content, mp_wait


class MPathwaysListener(AbstractEventListener):
    def after_navigate_to(self, url, driver):
        mp_switch_to_content(driver)

    def before_click(self, element, driver):
        mp_switch_to_content(driver)
        mp_wait(driver)

    def after_click(self, element, driver):
        mp_switch_to_content(driver)
        mp_wait(driver)

    def after_change_value_of(self, element, driver):
        mp_switch_to_content(driver)
        mp_wait(driver)

    def before_change_value_of(self, element, driver):
        mp_switch_to_content(driver)
        mp_wait(driver)
