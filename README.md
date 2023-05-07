# In order to use a proxy with this project you need to add it in the proxies_db.json!
# When adding proxy in it, it is required to fill out the following parameters if it:
*      username
*      password
*      host
*      port
*      country
*      version
*      end_date in format '%Y-%m-%d %H:%M:%S' => ex. '2023-05-06 20:09:50'
# In order to use proxy you must set the variables 'use_proxy' to 'True', which is boolean and  
# 'countries', which is a list of Alpha-2 codes of countries of proxies /the country in the proxies_db.json/. Ex:
`use_proxy = True` 
`proxy_countries = ['US']`
# In order to use proxies from multiple countries, add the countries to the 'proxy_countries', separated by ','. Ex:
`proxy_countries = ['US', 'UK']`