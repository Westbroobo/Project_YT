"""
Filename:3.SMP_Pic.py
Author: Westbroobo
Date: 2024/9/27
"""

import requests
from tool import UA
import pandas as pd

df_menu = pd.read_excel('./SMP_menu.xlsx', header=0)
Part_Number = df_menu['Part Number'].to_list()
img_ls = []
for partNum in Part_Number:
    url = f'https://ecatalog.smpcorp.com/V2/STD/api/image/getimage?partNum={partNum}&brand=STI&zoomFactor=186'
    rsp = requests.get(url=url, headers=UA.get_User_Agent_Requests())
    img = rsp.text.replace('"', '')
    rsp.close()
    if img == '':
        url = f'https://ecatalog.smpcorp.com/V2/STD/api/image/getimage?partNum={partNum}&brand=STD&zoomFactor=186'
        rsp = requests.get(url=url, headers=UA.get_User_Agent_Requests())
        img = rsp.text.replace('"', '')
        rsp.close()
    img_ls.append(img)

df_menu['Img'] = img_ls
df_menu.to_excel('./SMP_menu.xlsx', index=False)


