# -*- coding: utf-8 -*- 
# @Time ： 2024/8/9 10:38
# @Auth ： Westbroobo
# @File ：1.Pic_Download.py


from gevent import monkey, pool
monkey.patch_all(thread=False)
import pandas as pd
import requests
import time
from tool import UA, Proxy
import urllib3
import os
urllib3.disable_warnings()

headers = UA.get_User_Agent_Requests()
df_menu = pd.read_excel('./menu_img.xlsx')
Url = df_menu['img'].to_list()
Part_Number = df_menu['Part_Number'].to_list()


def fetch_data(url):
    num = 100
    for test in range(num):
        index = Url.index(url)
        pic_num = Part_Number[index]
        session = requests.session()
        try:
            res = session.get(url, headers=headers, proxies=Proxy.get_Proxy_Requests(), verify=False)
            status_code = res.status_code
            img = res.content
            with open(f'C:/Users/YangTeng/Pictures/新建文件夹/{pic_num}.jpg', 'wb') as f:
                f.write(img)
            res.close()
            f.close()
            list_file = list(os.walk(r'C:/Users/YangTeng/Pictures/新建文件夹'))[0][2]
            list_file = [ff for ff in list_file if not ff.endswith('.tmp')]
            if status_code == 200:
                print('{}【尝试次数：{}】-success，进度：{}/{}'.
                      format(pic_num, test+1, len(list_file), len(Url)))
                break
        except:
            time.sleep(1)
            continue


pool = pool.Pool(15)
for url in Url:
    pool.spawn(fetch_data, url)
pool.join()


