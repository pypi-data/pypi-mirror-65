import threading
import logging

from koverj.common.client.koverj_client import KoverjClient
from koverj.common.model.test_result import TestResult


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class LocatorsLifecycle(metaclass=Singleton):

    def __init__(self, client: KoverjClient = None):
        self.storage = threading.local()
        self.storage.locators = []
        self.client = client or KoverjClient()

    def send_locators(self, build_id: int, test_name: str):
        test_result = TestResult(buildId=build_id, testName=test_name, locators=list(set(self.storage.locators)))
        if self.client.config.log_locators:
            logging.debug(test_result)

        if self.client.config.use_koverj:
            self.client.send_test_result(test_result)
        self.storage.locators.clear()
