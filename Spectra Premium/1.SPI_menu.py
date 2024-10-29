# -*- coding: utf-8 -*- 
# @Time ： 2024/8/2 9:36
# @Auth ： Westbroobo
# @File ：1.SPI_menu.py

from tool import UA, Proxy
import requests
from lxml import etree
import pandas as pd
import time

df = pd.DataFrame(columns=['Part_Number', 'Url', 'Img'])

headers = UA.get_User_Agent_Requests()
headers['referer'] = 'https://ecat.spectrapremium.com/en/parts'
proxies = Proxy.get_Proxy_Requests()

for page in range(1, 6):
    try:
        url = 'https://ecat.spectrapremium.com/en/parts?line=electronic_throttle_bodies&universal=0&' \
              'hide-exclusives-canadian-market=0&page={}&sort=popularity&limit=50'.format(page)
        rsp = requests.get(url=url, headers=headers, proxies=proxies)
        tree = etree.HTML(rsp.text)
        articles = tree.xpath('.//section[@class="grille-produits"]/article[@class="tuile-produit"]')
        list_title_fixed = ['No', 'Part_Number', 'Url', 'Img']
        for article in articles:
            part_number = article.xpath('./div[1]/div[1]/h2/a/text()')[0]
            href = article.xpath('./div[1]/div[1]/h2/a')[0].get('href')
            detail_url = 'https://ecat.spectrapremium.com/' + href
            src = article.xpath('./div[1]/div[2]/div[2]/a/img')[0].get('src')
            img = 'https://ecat.spectrapremium.com/' + src
            df_transit = pd.DataFrame([{'Part_Number': part_number, 'Url': detail_url, 'Img': img}])
            spec_num = len(article.xpath('./div[1]/div[1]/dl/div'))
            for spec in range(1, spec_num+1):
                dt = article.xpath('./div[1]/div[1]/dl/div[{}]/dt/text()'.format(spec))[0]
                dd = article.xpath('./div[1]/div[1]/dl/div[{}]/dd/text()'.format(spec))[0]
                df_transit[dt] = dd
            df = pd.concat([df, df_transit], ignore_index=True).fillna('')
    except:
        print(page)
        time.sleep(1)
        continue
df.to_excel('./SPI_menu.xlsx', index=False)




