### Python (>=3.7) agent that allow to collect locators from Selenium based UI tests.
Inspired by SergeyPirogov koverj-java-agent.
Browser_driver instance (e.g. webdriver.Chrome()) has to be created and passed to a LocatorsWatchingDriver

#### - Selenium usage:
```
chrome_driver = webdriver.Chrome(executable_path=executable_path, options=chrome_options)
driver = LocatorsWatchingDriver(driver=chrome_driver)
```

#### - Selene usage:
```
driver = LocatorsWatchingDriver(driver=chrome_driver)
browser.set_driver(driver)
```

An web_driver may be created as pytest fixture, e.g.:

```
@pytest.fixture()    
def web_driver(chrome_driver):
    driver = LocatorsWatchingDrive(driver=chrome_web_driver)
    browser.set_driver(driver)
    yield browser.driver()
    browser.quit()
```

If pytest is used the koverj plugin may be registered in conftest.py:
```
pytest_plugins = [
    'koverj.common.plugin.pytest_koverj_plugin',
]
```

#### Supported integrations:
- Selene
- Selenium

#### Supported test runners:
- pytest

In order to collect data you have to run koverj server (thanks to):
docker run -p 8086:8086 spirogov/koverj:0.1.0

In order to see results in your browser add **koverj-browser-plugin** to your browser.