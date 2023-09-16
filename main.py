from etsy_crawler import make_etsy_search
from statistics import make_statistics
from utils import init_project_settings
import settings


init_project_settings()

statistics_data = []

total_searches: int
pages_per_search: int
search_query: str
shop_name: str
use_proxy: bool
proxy_countries: list
proxy_versions: list

total_searches = 20
pages_per_search = 3
search_query = settings.SEARCH_QUERY
shop_name = settings.SHOP_NAME
use_proxy = False
proxy_countries = []
proxy_versions = []


for search_num in range(1, total_searches+1):
    print(f'-----  NEW SEARCH  -----  SEARCH COUNT:  {search_num}  -----')

    make_etsy_search(search_query=search_query, shop_name=shop_name, pages_to_iterate=pages_per_search,
                     use_proxy=use_proxy, proxy_countries=proxy_countries, proxy_versions=proxy_versions,
                     search_num=search_num, stats_data=statistics_data)

make_statistics(data=statistics_data)
