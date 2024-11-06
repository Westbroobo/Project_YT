"""
Filename:1.1-1.menu.py
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
title_ls = []
img_ls = []
href_ls = []
for page in range(1, 2):
    url = 'https://www.carid.com/trico/?page={}#prod-list'.format(page)
    rsp = requests.get(url=url, impersonate="chrome101", headers=headers)
    tree = etree.HTML(rsp.text)
    items = tree.xpath('//*[@class="js-product-list-item"]')
    for item in items:
        img = item.xpath('./div[1]/img')[0].get('data-src')
        href = 'https://www.carid.com/' + item.xpath('.//div[@class="lst-main"]/div[1]/a')[0].get('href')
        title = item.xpath('.//div[@class="lst-main"]/div[1]/a/text()')[0]
        title_ls.append(title)
        img_ls.append(img)
        href_ls.append(href)
    rsp.close()

df = pd.DataFrame(columns=['Title', 'Img', 'Url'])
df['Title'] = title_ls
df['Img'] = img_ls
df['Url'] = href_ls
df.to_excel('./menu.xlsx', index=False)

