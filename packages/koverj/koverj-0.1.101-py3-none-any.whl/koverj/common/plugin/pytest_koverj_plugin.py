from koverj.common.client.locators_life_cycle import LocatorsLifecycle


def pytest_runtest_teardown(item):
    LocatorsLifecycle().send_locators(build_id=1, test_name=item.name)
