import os

import dotenv

dotenv.load_dotenv()
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

HEADLESS = False
WAIT_SECONDS = 2

CHROME_PATH = os.environ['CHROME_PATH']
CHROME_DRIVER_PATH = os.environ['CHROME_DRIVER_PATH']
INCOMPATIBLE_CHROME_DRIVER_EXC = 'YOU SHOULD DOWNLOAD CHROME DRIVER VERSION {chrome_version}, ' \
                                 'YOUR CURRENT CHROME VERSION IS: {chrome_driver_version}'

DB_NAME = 'proxies_db.json'
DB_PATH = os.path.join(os.getcwd(), DB_NAME)

PROXY_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
LEFT_HOURS_PROXY_TO_REMOVE = 2

SEARCH_QUERY = os.environ['SEARCH_QUERY']
SHOP_NAME = os.environ['SHOP_NAME']