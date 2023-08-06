import logging

from koverj.common.config.project_config import ProjectConfig
from koverj.common.model.test_result import TestResult
from koverj.common.service.koverj_service import KoverjService


class KoverjClient:

    def __init__(self, config: ProjectConfig = None):
        self.config = config or ProjectConfig()
        self.service = KoverjService(base_url=self.config.service_url)

    def send_test_result(self, test_result: TestResult):
        try:
            response = self.service.post_locators(test_result)
            if response.status_code != 200:
                logging.debug(response.text)
                raise RuntimeError(f"Locators not saved: {response.status_code}")
        except Exception as e:
            logging.error(e)
