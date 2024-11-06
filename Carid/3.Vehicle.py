"""
Filename:3.Vehicle.py
Author: Westbroobo
Date: 2024/11/5
"""
from gevent import monkey, pool
monkey.patch_all(thread=False)
from curl_cffi import requests
from tool import UA, Proxy
from lxml import etree
import pandas as pd
import time

df_menu = pd.read_excel('./menu.xlsx')
Url = df_menu['Url'].to_list()
url_ls = []
make_ls = []
model_ls = []
year_ls = []
def fetch_data(url):
    num = 20
    for test in range(num):
        try:
            headers = {
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': UA.get_UA(),
                'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
                'sec-ch-ua-arch': '"x86"',
                'sec-ch-ua-bitness': '"64"',
                'sec-ch-ua-full-version': '"130.0.6723.71"',
                'sec-ch-ua-full-version-list': '"Chromium";v="130.0.6723.71", "Google Chrome";v="130.0.6723.71", "Not?A_Brand";v="99.0.0.0"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"10.0.0"',
            }
            rsp = requests.get(url=url, impersonate="chrome101", headers=headers, proxies=Proxy.get_Proxy_Requests())
            status_code = rsp.status_code
            tree = etree.HTML(rsp.text)
            trs = tree.xpath('//*[@id="applications"]/div/div/div[1]/table/tr')
            if len(trs) == 0:
                url_ls.append(url)
                make_ls.append('')
                model_ls.append('')
                year_ls.append('')
            else:
                make = ''
                for tr in trs[1:]:
                    td_ = len(tr.xpath('./td'))
                    if td_ == 3:
                        make = tr.xpath('./td[1]/text()')[0]
                        model = tr.xpath('./td[2]/text()')[0]
                        year = tr.xpath('./td[3]/text()')[0]
                    else:
                        model = tr.xpath('./td[1]/text()')[0]
                        year = tr.xpath('./td[2]/text()')[0]
                    if ', ' in year:
                        list_year = year.split(', ')
                        url_ls.append(url)
                        make_ls.append(make)
                        model_ls.append(model)
                        year_ls.append(list_year[0].strip())
                        url_ls.append(url)
                        make_ls.append(make)
                        model_ls.append(model)
                        year_ls.append(list_year[1].strip())
                    else:
                        url_ls.append(url)
                        make_ls.append(make)
                        model_ls.append(model)
                        year_ls.append(year.strip())
            if status_code == 200:
                print(f'{url}【尝试次数：{test + 1}】-success，进度：{len(set(url_ls))}/{len(Url)}')
                rsp.close()
                break
        except:
            time.sleep(0.3)
            if test == num - 1:
                print(f'{url}【尝试次数：{test}】-error')
                continue

pool = pool.Pool(15)
for url in Url:
    pool.spawn(fetch_data, url)
pool.join()
df = pd.DataFrame(columns=['Url', 'Make', 'Model', 'Year'])
df['Url'] = url_ls
df['Make'] = make_ls
df['Model'] = model_ls
df['Year'] = year_ls
def year_split(years):
    years_ = []
    if '-' in str(years):
        year1 = years.split('-')[0]
        year2 = years.split('-')[1]
        for y in range(int(year1), int(year2)+1):
            years_.append(y)
    elif years == '':
        pass
    else:
        years_.append(int(years))
    return years_
df['Year'] = df['Year'].apply(lambda x: year_split(x))
df = df.explode('Year')
df.to_excel('./Vehicle.xlsx', index=False)

