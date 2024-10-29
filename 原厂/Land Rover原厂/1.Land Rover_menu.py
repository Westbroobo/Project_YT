# -*- coding: utf-8 -*- 
# @Time ： 2024/8/14 18:02
# @Auth ： Westbroobo
# @File ：1.Land Rover_menu.py

import requests
from tool import UA
from lxml import etree
import pandas as pd
import time

df = pd.DataFrame(columns=['Part_Number', 'Title', 'Url'])
headers = UA.get_User_Agent_Requests()
headers['referer'] = 'https://landrover.oempartsonline.com/'

for page in range(3, 4):
    url = 'https://landrover.oempartsonline.com/search?search_str=radiator%2Bhose&page={}' \
          '&year=&make=&model=&catalog_type=parts'.format(page)
    try:
        rsp = requests.get(url=url, headers=headers)
        tree = etree.HTML(rsp.text)
        div_row = tree.xpath('.//div[@class="catalog-product marketplace-product row "]')
        for div in div_row:

            href = div.xpath('./div[1]/a')[0].get('href')
            derail_url = 'https://landrover.oempartsonline.com' + href
            title = div.xpath('./div[2]/div[1]/strong/a/text()')[0]
            try:
                part_number = div.xpath('./div[2]/div[1]/div[3]/div/a/text()')[0]
            except:
                part_number = ''
            df_transit = pd.DataFrame([{'Part_Number': part_number, 'Title': title, 'Url': derail_url}])
            div_info = div.xpath('./div[2]/div[1]/div[5]/div')
            for i in range(1, len(div_info)+1):
                row = div.xpath('./div[2]/div[1]/div[5]/div[{}]/strong/text()'.format(i))[0]
                if row == 'Positions:' or row == 'Replaces:':
                    content = div.xpath('./div[2]/div[1]/div[5]/div[{}]/text()'.format(i))[-1].strip()
                elif row == 'Fits:':
                    content = ''
                else:
                    content = div.xpath('./div[2]/div[1]/div[5]/div[{}]/span/text()'.format(i))[0].strip()
                df_transit[row] = content
            df = pd.concat([df, df_transit], ignore_index=True).fillna('')
            rsp.close()
    except Exception as e:
        print(page, e)
        time.sleep(1)
        continue
df.to_excel('./Land Rover_menu.xlsx', index=False)



