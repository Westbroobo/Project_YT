# -*- coding: utf-8 -*- 
# @Time ： 2024/8/13 15:32
# @Auth ： Westbroobo
# @File ：style.py


from tool import UA
import requests
from lxml import etree
import pandas as pd
import time
df = pd.DataFrame(columns=['Url', 'Style'])
headers = UA.get_User_Agent_Requests()
headers['referer'] = 'http://www.lian-tuoh.com.tw'
df_menu = pd.read_excel('./Liantuoh_menu.xlsx', header=0)
urls = df_menu['product_url'].to_list()
skus = df_menu['SKU'].to_list()
for url in urls:
    try:
        rsp = requests.get(url=url, headers=headers)
        tree = etree.HTML(rsp.text)
        div_style = tree.xpath('.//div[@class="sec-part editor"]')
        if len(div_style) == 1:
            style = ''
        else:
            style = div_style[-1].xpath('./div[1]/table[1]/tr/td/text()')[0]
        df_transit = pd.DataFrame([{'Url': url, 'Style': style}])
        df = pd.concat([df, df_transit], ignore_index=True).fillna('')
    except Exception as e:
        print(url, e)
        time.sleep(1)
        continue

df.to_excel('./Liantuoh_style.xlsx', index=False)
