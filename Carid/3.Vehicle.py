"""
Filename:3.Vehicle.py
Author: Westbroobo
Date: 2024/11/5
"""
from curl_cffi import requests
from tool import UA
from lxml import etree
import pandas as pd

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
df_menu = pd.read_excel('./menu.xlsx')
Url = df_menu['Url'].to_list()
url_ls = []
make_ls = []
model_ls = []
year_ls = []
for url in Url:
    rsp = requests.get(url=url, impersonate="chrome101", headers=headers)
    tree = etree.HTML(rsp.text)
    try:
        trs = tree.xpath('//*[@id="applications"]/div/div/div[1]/table/tr')
        content = []
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
                year_ls.append(list_year[0])
                url_ls.append(url)
                make_ls.append(make)
                model_ls.append(model)
                year_ls.append(list_year[1])
            else:
                url_ls.append(url)
                make_ls.append(make)
                model_ls.append(model)
                year_ls.append(year)
    except:
        pass
    rsp.close()


