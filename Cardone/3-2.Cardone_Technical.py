"""
Filename:3-2.Cardone_Technical.py
Author: Westbroobo
Date: 2024/9/27
"""

import requests
import pandas as pd
import time
from tool import UA
from lxml import etree
import json

df_menu = pd.read_excel('./Cardone_menu.xlsx', header=0)
Part_Number = df_menu['Part_Number'].to_list()
Url = df_menu['product_url'].to_list()
headers = UA.get_User_Agent_Requests()
headers['referer'] = 'https://www.cardone.com'

part_ls = []
technical_ls = []
error_ = []
for url in Url:
    part_number = Part_Number[Url.index(url)]
    try:
        rsp = requests.get(url=url, headers=headers)
        tree = etree.HTML(rsp.text)
        productView = tree.xpath('//*[@class="productView-table technical"]/div')
        list_ = []
        for view in productView:
            dict_ = {}
            key = view.xpath('./div[1]/text()')[0].strip()
            value = view.xpath('./div[2]/text()')[0].strip()
            dict_[key] = value
            list_.append(dict_)
        formatted_data = {str(index): item for index, item in enumerate(list_)}
        json_data = json.dumps(formatted_data)
        part_ls.append(part_number)
        technical_ls.append(json_data)
        rsp.close()
        print('success-{}, error-{}, processing-{}'.format(len(part_ls), len(error_),
                                                           len(Part_Number) - len(part_ls) - len(error_)))
    except:
        error_.append(url)
        print('success-{}, error-{}, processing-{}'.format(len(part_ls), len(error_),
                                                           len(Part_Number) - len(part_ls) - len(error_)))
        time.sleep(1)
        continue

df = pd.DataFrame(columns=['Part_Number', 'Technical'])
df['Part_Number'] = part_ls
df['Technical'] = technical_ls
df.to_excel('./Cardone_Technical.xlsx', index=False)



