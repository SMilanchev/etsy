import time
import random

from selenium.common.exceptions import WebDriverException

from etsy_crawler.search import make_search
from etsy_crawler.item import (
    open_all_matching_items_in_new_tabs, open_types_for_item, select_type_for_item, add_to_basket,
    find_matching_elements_on_page, like_item, find_search_result_on_page, are_types_in_page
)
from settings import WAIT_SECONDS


def make_etsy_search(search_query: str, shop_name: str, use_proxy: bool, proxy_countries: list[str],
                     pages_to_iterate: int = 10):
    try:
        driver_search = make_search(search_query=search_query, use_proxy=use_proxy, proxy_countries=proxy_countries)
        for i in range(1, pages_to_iterate + 1):
            scroll_height = random.randint(1800, 3000)
            driver_search.execute_script(f"window.scrollTo(0, {scroll_height});")

            page_search_result = find_search_result_on_page(driver=driver_search)
            matching_elements = find_matching_elements_on_page(search_result=page_search_result, shop_name=shop_name)
            print('PAGE NUM:', i, 'ELEMENTS MATCHING:', len(matching_elements))
            if len(matching_elements) > 0:
                original_window = driver_search.current_window_handle

                driver_search = open_all_matching_items_in_new_tabs(driver=driver_search,
                                                                    search_result=page_search_result,
                                                                    shop_name=shop_name)
                time.sleep(4)

                new_tabs_opened = set(driver_search.window_handles) - {original_window}
                for tab in new_tabs_opened:

                    driver_search.switch_to.window(tab)
                    time.sleep(WAIT_SECONDS)
                    like_item(driver=driver_search)
                    if are_types_in_page(driver=driver_search):
                        driver_search = open_types_for_item(driver=driver_search)
                        select_type_for_item(driver=driver_search)
                    # if there are no types, there may be quantity which has default value - do not do anything
                    add_to_basket(driver=driver_search)
                    driver_search.close()
                    time.sleep(WAIT_SECONDS)
                driver_search.switch_to.window(original_window)

            current_page = driver_search.current_url
            next_page_url = current_page.replace(f'page={i}', f'page={i + 1}')
            driver_search.get(next_page_url)
            time.sleep(10)
        driver_search.close()
    except WebDriverException as e:
        print('IN EXCEPTION. ERROR MESSAGE:')
        print(e.msg)
