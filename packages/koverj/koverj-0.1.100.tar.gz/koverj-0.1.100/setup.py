# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['koverj',
 'koverj.agent',
 'koverj.agent.selenium',
 'koverj.common',
 'koverj.common.client',
 'koverj.common.config',
 'koverj.common.model',
 'koverj.common.plugin',
 'koverj.common.service']

package_data = \
{'': ['*'],
 'koverj': ['koverj-browser-plugin/*',
            'koverj-browser-plugin/assets/*',
            'koverj-browser-plugin/assets/css/*',
            'koverj-browser-plugin/assets/js/*',
            'koverj-browser-plugin/mock/*',
            'koverj-browser-plugin/plugin/*']}

install_requires = \
['configparser>=5.0.0,<6.0.0',
 'future>=0.18.2,<0.19.0',
 'pytest>=5.4.1,<6.0.0',
 'requests>=2.23.0,<3.0.0',
 'selene>=1.0.2,<2.0.0',
 'selenium==3.141',
 'uplink>=0.9.1,<0.10.0']

setup_kwargs = {
    'name': 'koverj',
    'version': '0.1.100',
    'description': 'Test coverage for selenium based tests',
    'long_description': "### Python (>=3.7) agent that allow to collect locators from Selenium based UI tests.\nInspired by SergeyPirogov koverj-java-agent.\nBrowser_driver instance (e.g. webdriver.Chrome()) has to be created and passed to a LocatorsWatchingDriver\n\n#### - Selenium usage:\n```\nchrome_driver = webdriver.Chrome(executable_path=executable_path, options=chrome_options)\ndriver = LocatorsWatchingDriver(driver=chrome_driver)\n```\n\n#### - Selene usage:\n```\ndriver = LocatorsWatchingDriver(driver=chrome_driver)\nbrowser.set_driver(driver)\n```\n\nAn web_driver may be created as pytest fixture, e.g.:\n\n```\n@pytest.fixture()    \ndef web_driver(chrome_driver):\n    driver = LocatorsWatchingDrive(driver=chrome_web_driver)\n    browser.set_driver(driver)\n    yield browser.driver()\n    browser.quit()\n```\n\nIf pytest is used the koverj plugin may be registered in conftest.py:\n```\npytest_plugins = [\n    'koverj.common.plugin.pytest_koverj_plugin',\n]\n```\n\n#### Supported integrations:\n- Selene\n- Selenium\n\n#### Supported test runners:\n- pytest\n\nIn order to collect data you have to run koverj server (thanks to):\ndocker run -p 8086:8086 spirogov/koverj:0.1.0\n\nIn order to see results in your browser add **koverj-browser-plugin** to your browser.",
    'author': 'Ivan Huryn',
    'author_email': 'igur007@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Igur007/koverj-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
