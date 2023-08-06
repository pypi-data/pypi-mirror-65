from uuid import uuid4
from selenium.webdriver.remote.webdriver import WebDriver
from koverj.common.client.locators_life_cycle import LocatorsLifecycle
from koverj.common.model.locator import Locator


class KoverjSelenium:
    def __init__(self):
        self.lifecycle = LocatorsLifecycle()

    def setup(self, driver: WebDriver):
        uuid = str(uuid4())
        self.lifecycle.storage.locators.append(
            Locator(url=driver.current_url, locator="some locator here", uuid=uuid)
        )
