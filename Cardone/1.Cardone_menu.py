# -*- coding: utf-8 -*- 
# @Time ： 2024/7/29 10:04
# @Auth ： Westbroobo
# @File ：1.Cardone_menu.py


import requests
import pandas as pd
from lxml import etree
import time
from tool import UA

part_number_ls = []
product_url_ls = []
img_url_ls = []
for i in range(1, 7):
    try:
        url = 'https://www.cardone.com/fuel-air-exhaust/air-intake/mass-air-flow-sensor/?limit=96&page={}'.format(i)
        headers = UA.get_User_Agent_Requests()
        headers['referer'] = 'https://www.cardone.com'
        rsp = requests.get(url=url, headers=headers)
        html = rsp.content.decode(errors='ignore')
        tree = etree.HTML(html)
        lis = tree.xpath('//div[@id="product-listing-container"]/ul/li')
        for li in lis:
            a = li.xpath('./article/figure/a[@href]')
            product_url = a[0].get('href')
            img = li.xpath('./article/figure/a/div/img[@src]')
            img_url = img[0].get('src')
            p = li.xpath('./article/div/div[1]/div[1]/p[2]/text()')
            part_number = p[0].replace(' ', '')
            part_number_ls.append(part_number)
            product_url_ls.append(product_url)
            img_url_ls.append(img_url)
    except:
        time.sleep(3)
        print(i)
        continue

df = pd.DataFrame(columns=['Part_Number',
                           'product_url',
                           'img_url'])
df['Part_Number'] = part_number_ls
df['product_url'] = product_url_ls
df['img_url'] = img_url_ls
df.to_excel('./Cardone_menu.xlsx', index=False)

