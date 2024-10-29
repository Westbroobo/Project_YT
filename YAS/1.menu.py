"""
Filename:1.menu.py
Author: Westbroobo
Date: 2024/10/22
"""

import requests
from lxml import etree
from tool import UA
import pandas as pd

df = pd.DataFrame(columns=['Title', 'Simple', 'Img', 'Url'])
page = 37
for p in range(1, page+1):
    url = f'https://www.yas.com.cn/products2099650p{p}/Hydraulic-EPS-Steering-Gear.htm'
    rsp = requests.get(url=url, headers=UA.get_User_Agent_Requests())
    tree = etree.HTML(rsp.text)
    product_list = tree.xpath('//*[@class="content-bg content-bg-productlist"]/div[2]/div')
    for div in product_list:
        href = div.xpath('./div[1]/a')[0].get('href')
        detail_url = 'https:' + href
        img = div.xpath('./div[1]/a/img')[0].get('src')
        title = div.xpath('./div[2]/a/text()')[0]
        info_simple = div.xpath('./div[3]/text()')[0]
        df_transit = pd.DataFrame([{'Title': title, 'Simple': info_simple, 'Img': img, 'Url': detail_url}])
        df = pd.concat([df, df_transit], ignore_index=True).fillna('')
    rsp.close()

df.to_excel('./YAS_menu.xlsx', index=False)


