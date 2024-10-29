"""
Filename:1.SMP_menu.py
Author: Westbroobo
Date: 2024/9/10
"""

import requests, json
from tool import UA
import pandas as pd

list_part_number = []
page = 4
for i in range(page):
    start = i*96
    url = (f'https://ecatalog.smpcorp.com/V2/STD/api/part/partsearch?filter=Mass%20Air%20Flow%20(MAF)%20Sensors'
           f'&filterType=n&searchType=p&imageSize=80&start={start}&limit=96&sort=6&catFilter=-All-&yearFilter=-All-&'
           f'makeFilter=-All-&modelFilter=-All-&engineFilter=-All-&attrCodeFilter=-All-&attrValueFilter=-All-&'
           f'plkEngineMakeFilter=-All-&plkEngineModelFilter=-All-&plkEngineDispFilter=-All-')
    rsp = requests.get(url=url, headers=UA.get_User_Agent_Requests())
    html = rsp.content.decode(errors='ignore')
    json_object = json.loads(html)
    for j in json_object:
        basePart = j["basePart"]
        list_part_number.append(basePart)

df = pd.DataFrame(columns=['Part Number'])
df['Part Number'] = list_part_number
df.to_excel('./SMP_menu.xlsx', index=False)


