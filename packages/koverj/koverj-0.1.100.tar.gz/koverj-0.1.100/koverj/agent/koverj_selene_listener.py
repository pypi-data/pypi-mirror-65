from uuid import uuid4
from selene.api import browser
from koverj.agent.selenium.webdriver_locator_listener import WebDriverLocatorListener
from koverj.common.client.locators_life_cycle import LocatorsLifecycle
from koverj.common.model.locator import Locator


class KoverjSeleneListener(WebDriverLocatorListener):
    def __init__(self):
        super().__init__()
        self.lifecycle = LocatorsLifecycle()

    def setup(self):
        current_url = browser.driver().current_url
        uuid = str(uuid4())
        self.lifecycle.storage.locators.append(
            Locator(url=current_url, locator="some locator here", uuid=uuid)
        )
