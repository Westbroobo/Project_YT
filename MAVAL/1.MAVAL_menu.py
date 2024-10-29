"""
Filename:1.MAVAL_menu.py
Author: Westbroobo
Date: 2024/9/10
"""

import requests
from tool import UA
from lxml import etree
import pandas as pd

df = pd.DataFrame(columns=['Part Number', 'Title', 'Img', 'Url'])
for page in range(1,51):
    headers = UA.get_User_Agent_Requests()
    headers['referer'] = 'https://mavalgear.com/'
    url = 'https://mavalgear.com/collections/rack-and-pinions?page={}'.format(page)
    rsp = requests.get(url=url, headers=headers)
    tree = etree.HTML(rsp.text)
    card_wrapper = tree.xpath('//*[@class="card-wrapper product-card-wrapper underline-links-hover"]')
    for card in card_wrapper:
        src = card.xpath('./div/div[1]/div[1]/div[1]/img')[0].get('src')
        img = 'https:' + src
        title = card.xpath('./div/div[2]/div[1]/h3/a/text()')[0].strip()
        href = card.xpath('./div/div[2]/div[1]/h3/a')[0].get('href').strip()
        detail_url = 'https://mavalgear.com' + href
        part_number = title.split('-')[-1].strip()
        df_transit = pd.DataFrame([{'Part Number': part_number, 'Title': title, 'Img': img, 'Url': detail_url}])
        df = pd.concat([df, df_transit], ignore_index=True).fillna('')
    rsp.close()

df.to_excel('./MAVAL_menu.xlsx', index=False)




