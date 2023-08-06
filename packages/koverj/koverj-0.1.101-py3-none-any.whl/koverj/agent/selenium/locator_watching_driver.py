from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver
from koverj.agent.selenium.webdriver_locator_listener import WebDriverLocatorListener


class LocatorsWatchingDriver(EventFiringWebDriver):
    def __init__(self, driver: WebDriver):
        super().__init__(driver=driver, event_listener=WebDriverLocatorListener())
