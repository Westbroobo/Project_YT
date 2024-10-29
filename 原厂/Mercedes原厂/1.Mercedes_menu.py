# -*- coding: utf-8 -*- 
# @Time ： 2024/8/14 17:48
# @Auth ： Westbroobo
# @File ：Mercedes_menu.py

import requests
from tool import UA
from lxml import etree
import pandas as pd
import time

df = pd.DataFrame(columns=['Part_Number', 'Title', 'Url'])
headers = UA.get_User_Agent_Requests()
headers['referer'] = 'https://www.mercedesbenzpartscenter.com/'

for page in range(1, 1019):
    url = 'https://www.mercedesbenzpartscenter.com/search?search_str=water%2Bcoolant%2Bhose&page={}' \
          '&year=&make=&model=&catalog_type=parts'.format(page)
    try:
        rsp = requests.get(url=url, headers=headers)
        tree = etree.HTML(rsp.text)
        div_row = tree.xpath('.//div[@class="catalog-product row "]')
        for div in div_row:
            href = div.xpath('./div[1]/a')[0].get('href')
            derail_url = 'https://www.mercedesbenzpartscenter.com' + href
            title = div.xpath('./div[2]/strong/a/text()')[0]
            part_number = div.xpath('./div[2]/div[1]/div/a/text()')[0]
            df_transit = pd.DataFrame([{'Part_Number': part_number, 'Title': title, 'Url': derail_url}])
            div_info = div.xpath('./div[2]/div[3]/div')
            for i in range(1, len(div_info)+1):
                row = div.xpath('./div[2]/div[3]/div[{}]/strong/text()'.format(i))[0]
                if row == 'Positions:' or row == 'Replaces:':
                    content = div.xpath('./div[2]/div[3]/div[{}]/text()'.format(i))[-1].strip()
                elif row == 'Fits:':
                    content = ''
                else:
                    content = div.xpath('./div[2]/div[3]/div[{}]/span/text()'.format(i))[0].strip()
                df_transit[row] = content
            df = pd.concat([df, df_transit], ignore_index=True).fillna('')
            rsp.close()
    except:
        print(page)
        time.sleep(1)
        continue
df.to_excel('./Mercedes_menu.xlsx', index=False)


