from uuid import uuid5, NAMESPACE_DNS
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.abstract_event_listener import AbstractEventListener
from koverj.common.client.locators_life_cycle import LocatorsLifecycle
from koverj.common.model.locator import Locator


class WebDriverLocatorListener(AbstractEventListener):
    def __init__(self, lifecycle: LocatorsLifecycle = None):
        super().__init__()
        self.lifecycle = lifecycle or LocatorsLifecycle()

    def before_navigate_to(self, url, driver):
        pass

    def after_navigate_to(self, url, driver):
        pass

    def before_navigate_back(self, driver):
        pass

    def after_navigate_back(self, driver):
        pass

    def before_navigate_forward(self, driver):
        pass

    def after_navigate_forward(self, driver):
        pass

    def before_find(self, by, value, driver: WebDriver):
        locator_repr = f"(By={by}, Value='{value}')"
        uuid = str(uuid5(NAMESPACE_DNS, name=f"{driver.current_url}{locator_repr}"))
        self.lifecycle.storage.locators.append(
            Locator(url=driver.current_url, locator=value, uuid=uuid)
        )

    def after_find(self, by, value, driver):
        pass

    def before_click(self, element, driver):
        pass

    def after_click(self, element, driver):
        pass

    def before_change_value_of(self, element, driver):
        pass

    def after_change_value_of(self, element, driver):
        pass

    def before_execute_script(self, script, driver):
        pass

    def after_execute_script(self, script, driver):
        pass

    def before_close(self, driver):
        pass

    def after_close(self, driver):
        pass

    def before_quit(self, driver):
        pass

    def after_quit(self, driver):
        pass

    def on_exception(self, exception, driver):
        pass
