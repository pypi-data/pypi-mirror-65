from typing import List
from uplink import Body
from dataclasses import dataclass
from koverj.common.model.locator import Locator


@dataclass(frozen=True)
class TestResult(Body):
    buildId: int
    testName: str
    locators: List[Locator]

    def __repr__(self):
        locators_repr = "\n\t\t".join([str(loc) for loc in self.locators])
        return f"\n{self.__class__.__name__}(" \
               f"\n\tbuildId={self.buildId}" \
               f"\n\ttestName={self.testName}" \
               f"\n\tlocators=[" \
               f"\n\t\t{locators_repr}" \
               f"\n)"
