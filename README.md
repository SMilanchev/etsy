# 1.  Before start add `SEARCH_QUERY`, `SHOP_NAME`, `CHROME_PATH` and `CHROME_DRIVER_PATH` in .env.

# 2. In order **to use a proxies** with this project you need to add them in the proxies_db.json!
## 2.1. When adding proxy in it, it is required to fill out the following parameters if it:
*      username
*      password
*      host
*      port
*      country
*      version
*      end_date in format '%Y-%m-%d %H:%M:%S' => ex. '2023-05-06 20:09:50'
# 2.2. After adding the proxies in proxies_db.json you must set the variable 'use_proxy' to 'True':
`use_proxy = True` 

# 3. If you want **to use proxies from specific country**, you must add the country in _proxy_countries_, which is a list. Ex:
`proxy_countries = ['US']`
## 3.1. In order **to use proxies from multiple countries**, add the countries to the _proxy_countries_, separated by ','. Ex:
`proxy_countries = ['US', 'UK']`

# 4. If you want **to use proxies from specific version**, you must add the version in _proxy_versions_, which is a list. Ex:
`proxy_versions = ['three']`
## 4.1. In order **to use proxies from multiple versions**, add the versions to the _proxy_versions_, separated by ','. Ex:
`proxy_countries = ['three', 'four']`

# **The values you provide for _proxy_versions_ and _proxy_countries_ should be the ones from country and version you provided in proxies_db.json.** 