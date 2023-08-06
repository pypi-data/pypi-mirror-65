from dataclasses import dataclass


@dataclass(frozen=True)
class Locator:
    url: str
    locator: str
    subject: str = ""
    uuid: str = ""
    parent_uuid: str = "constant"
    # TODO no solution yet to get parent UUID in find().find() cases
