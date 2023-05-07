import re
from logging import getLogger

from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import SessionNotCreatedException

from etsy_crawler.proxies import Proxy
import settings

logger = getLogger(__name__)


def get_driver(proxy: None | Proxy, chrome_path=settings.CHROME_PATH, chrome_driver_path=settings.CHROME_DRIVER_PATH,
               headless=settings.HEADLESS, user_agent: str = None):
    seleniumwire_options = None
    if proxy:
        seleniumwire_options = {
            'proxy': {
                'https': proxy.uri,
                'no_proxy': 'localhost,127.0.0.1'
            }
        }
    headless = headless
    chrome_driver_path = chrome_driver_path
    service = Service(chrome_driver_path)
    chrome_path = chrome_path

    # Remove location tracking and other stuff indicating that the browser is emulated
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    prefs = {"profile.default_content_setting_values.geolocation": 2}
    options.add_experimental_option("prefs", prefs)

    if user_agent:
        options.add_argument(f'user-agent={user_agent}')

    if headless:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')  # Last I checked this was necessary.
        options.add_argument('--no-sandbox')  # Last I checked this was necessary.
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--disable-extensions')
    else:
        options.add_argument("--start-maximized")
    # Set chrome location
    options.binary_location = chrome_path

    options.add_argument('--disable-logging')

    options.add_argument('--disable-blank-features=AutomationControlled')
    # Create Driver
    driver = webdriver.Chrome(service=service, options=options, seleniumwire_options=seleniumwire_options)

    # Removes the webdriver.navigator attribute (indicates that the browser is automated)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
                Object.defineProperty(navigator, 'webdriver', {
                  get: () => undefined
                })
            """
    })

    driver.execute_cdp_cmd("Network.enable", {})
    return driver


def get_driver_and_browser_versions() -> dict:
    res = {'same': True, 'browser': '', 'driver_version': ''}
    try:
        driver = get_driver(proxy=None)
        driver.close()
        return res
    except SessionNotCreatedException as exc:
        exc_msg = exc.msg
        chrome_driver_version = re.findall(pattern='ChromeDriver only supports Chrome version (\d+)', string=exc_msg)[0]
        chrome_version = re.findall(pattern='Current browser version is (\d+.\d+.\d+.\d+)', string=exc_msg)[0]
        res.update({'same': False, 'browser': chrome_version, 'driver_version': chrome_driver_version})
        return res
