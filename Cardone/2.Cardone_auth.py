# -*- coding: utf-8 -*- 
# @Time ： 2024/7/29 10:51
# @Auth ： Westbroobo
# @File ：2.Cardone_auth.py

import requests
import pandas as pd
import time
from tool import UA
import re

df_menu = pd.read_excel('./Cardone_menu.xlsx', header=0)
urls = df_menu['product_url'].to_list()
Part_Number = df_menu['Part_Number'].to_list()
headers = UA.get_User_Agent_Requests()
headers['referer'] = 'https://www.cardone.com'
url_ls = []
auth_ls = []
part_ls = []
for url in urls:
    try:
        rsp_page = requests.get(url=url, headers=headers)
        url_theme_bundle = re.compile('<script src="(.+)"></script>').findall(rsp_page.text)[1]
        rsp_page.close()
        rsp_auth = requests.get(url=url_theme_bundle, headers=headers)
        auth = re.compile('auth=(.+?)\"}\\)').findall(rsp_auth.text)[0]
        url_ls.append(url)
        auth_ls.append(auth)
        part_number = Part_Number[urls.index(url)]
        part_ls.append(part_number)
        rsp_auth.close()
    except Exception as e:
        print(url)
        time.sleep(1)
        continue

df = pd.DataFrame(columns=['Part_Number', 'url', 'auth'])
df['Part_Number'] = part_ls
df['url'] = url_ls
df['auth'] = auth_ls
df.to_excel('./Cardone_auth.xlsx', index=False)





