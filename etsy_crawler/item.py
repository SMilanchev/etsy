import time

from seleniumwire import webdriver
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.common.by import By

from etsy_crawler.utils import clear_options_items
from settings import WAIT_SECONDS

TYPES_XPATH = '/html/body/main/div[1]/div[1]/div/div/div[1]/div[2]/div/div[6]/div[1]/div[1]/div[2]/div/div[1]/select'


def find_search_result_on_page(driver: webdriver.Chrome) -> WebElement:
    search_result_xpath = '/html/body/main/div/div[1]'
    search_result = driver.find_element(by=By.XPATH, value=search_result_xpath)
    return search_result


def find_matching_elements_on_page(search_result: WebElement, shop_name: str) -> list[WebElement]:
    matching_elements = search_result.find_elements(by=By.PARTIAL_LINK_TEXT, value=shop_name)
    return matching_elements


def open_all_matching_items_in_new_tabs(driver: webdriver.Chrome, search_result: WebElement, shop_name: str):
    all_items_found = search_result.find_elements(by=By.PARTIAL_LINK_TEXT, value=shop_name)
    print('ALL MATCHING ELEMENTS', len(all_items_found))
    for item in all_items_found:
        item.click()
    return driver


def are_types_in_page(driver: webdriver.Chrome) -> bool:
    types_elements = driver.find_elements(by=By.XPATH, value=TYPES_XPATH)
    return True if types_elements else False


def open_types_for_item(driver: webdriver.Chrome):
    driver.find_element(by=By.XPATH, value=TYPES_XPATH).click()
    time.sleep(WAIT_SECONDS)
    return driver


def select_type_for_item(driver: webdriver.Chrome):
    options_element = driver.find_element(by=By.XPATH, value=TYPES_XPATH)
    options_cleared = clear_options_items(options_element.text)
    available_options = list(filter(lambda x: 'Select an option' not in x and '[Sold out]' not in x, options_cleared))
    if available_options:
        option_index = options_cleared.index(available_options[0]) + 1

        option_to_select_xpath = f'/html/body/main/div[1]/div[1]/div/div/div[1]/div[2]/div/div[6]/div[1]/div[1]' \
                                 f'/div[2]/div/div[1]/select/option[{option_index}]'
        time.sleep(WAIT_SECONDS)
        options_elements = driver.find_elements(by=By.XPATH, value=option_to_select_xpath)
        if options_elements:
            options_elements[0].click()
    time.sleep(WAIT_SECONDS)


def add_to_basket(driver: webdriver.Chrome):
    from selenium.webdriver.common.by import By
    add_to_basket_class_name = 'wt-display-flex-xs.wt-flex-direction-column-xs.wt-flex-wrap.' \
                               'wt-flex-direction-row-md.wt-flex-direction-column-lg'
    add_to_basket_elements = driver.find_elements(by=By.CLASS_NAME, value=add_to_basket_class_name)
    add_to_basket_elements[0].click()


def close_login_popup(driver: webdriver.Chrome):
    close_login_popup_selector = '/html/body/div[5]/div[2]/div/div[7]/div/button'
    close_login_popup_element = driver.find_elements(by=By.XPATH, value=close_login_popup_selector)
    close_login_popup_element[0].click()


def like_item(driver: webdriver.Chrome):
    like_button_xpath = '/html/body/main/div[1]/div[1]/div/div/div[1]/div[1]/div/div/div[2]/button/div'
    like_button_elements = driver.find_elements(by=By.XPATH, value=like_button_xpath)
    if like_button_elements:
        like_button_elements[0].click()
    time.sleep(WAIT_SECONDS)
    login_popup_selector = '/html/body/div[5]/div[2]/div/div[7]/div'
    popup_opened = driver.find_elements(by=By.XPATH, value=login_popup_selector)
    if popup_opened:
        close_login_popup(driver=driver)
