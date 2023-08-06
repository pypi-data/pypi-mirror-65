from uplink import Consumer, post, Body, json
from requests.models import Response


class KoverjService(Consumer):
    @json
    @post("/locators")
    def post_locators(self, test_result: Body) -> Response:
        """post locators to server"""""
