import time

from seleniumwire import webdriver
from selenium.webdriver.common.by import By

from etsy_crawler.chrome_driver import get_driver
from etsy_crawler.proxies import get_proxy


def make_search(search_query: str, use_proxy: bool, proxy_countries: list):
    search_query = search_query.strip()
    search_query = search_query.replace(' ', '+')

    proxy = None
    if use_proxy:
        proxy = get_proxy(countries=proxy_countries)
    driver = get_driver(proxy=proxy)
    url_to_get = f'https://www.etsy.com/search?q={search_query}&ref=pagination&page=1'
    driver.get(url_to_get)
    time.sleep(5)

    driver = accept_cookies(driver=driver)
    time.sleep(4)
    return driver


def accept_cookies(driver: webdriver.Chrome,
                   accept_cookies_button='/html/body/div[5]/div[2]/div/div[2]/div/div[2]/div[2]/button'
                   ) -> webdriver.Chrome:
    cookies_element = driver.find_elements(by=By.XPATH, value=accept_cookies_button)

    if cookies_element:
        cookies_element[0].click()
    return driver
