# -*- coding: utf-8 -*-
# @Time ： 2024/2/20 9:17
# @Auth ： Westbroobo
# @File ：down_pic_requests.py

import pandas as pd
import requests
import time
from tool import UA
import urllib3
urllib3.disable_warnings()

df_menu = pd.read_excel('./menu_img_r.xlsx')
Url = df_menu['img'].to_list()
Part_Number = df_menu['Part_Number'].to_list()
count = 0
for url in Url:
    index = Url.index(url)
    pic_num = Part_Number[index]
    session = requests.session()
    try:
        res = session.get(url, headers=UA.get_User_Agent_Requests(), verify=False)
        img = res.content
        with open(f'C:/Users/YangTeng/Pictures/新建文件夹/{pic_num}.jpg', 'wb') as f:
            f.write(img)
        res.close()
        f.close()
        count += 1
    except:
        print(pic_num)
        count += 1
        time.sleep(1)
        continue


