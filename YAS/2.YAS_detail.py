"""
Filename:2.YAS_detail.py
Author: Westbroobo
Date: 2024/10/22
"""
import requests, json
from lxml import etree
from tool import UA
import pandas as pd

df = pd.DataFrame(columns=['Url', 'Data'])
df_menu = pd.read_excel('./YAS_menu.xlsx')
urls = df_menu['Url'].tolist()
for url in urls:
    rsp = requests.get(url=url, headers=UA.get_User_Agent_Requests())
    tree = etree.HTML(rsp.text)
    trs = tree.xpath('//*[@class="mation-box"]/table/tr')
    list_ = []
    for tr in trs:
        dict_ = {}
        key = tr.xpath('./th/text()')[0].strip().replace('\u200e', '')
        value = tr.xpath('./td/text()')[0].strip().replace('\u200e', '')
        dict_[key] = value
        list_.append(dict_)
    formatted_data = {str(index): item for index, item in enumerate(list_)}
    json_data = json.dumps(formatted_data)
    df_transit = pd.DataFrame([{'Url': url, 'Data': json_data}])
    df = pd.concat([df, df_transit], ignore_index=True).fillna('')
    rsp.close()

df.to_excel('./YAS_detail.xlsx', index=False)

