"""
Filename:2.SMP_Detail.py
Author: Westbroobo
Date: 2024/9/10
"""

import requests
import json
import pandas as pd
import time
from tool import UA
from tqdm import tqdm

df_menu = pd.read_excel('./SMP_menu.xlsx', header=0)
Part_Number = df_menu['Part Number'].to_list()
df = pd.DataFrame(columns=['Part Number', 'Buyer Guide', 'Part Specifications'])
error_ = []
for p in tqdm(Part_Number, desc='进度', ncols=100):
    url = 'https://ecatalog.smpcorp.com/V2/STD/api/part/partselect?part={}&func=PART&vid='.format(p)
    headers = UA.get_User_Agent_Requests()
    try:
        rsp = requests.get(url=url, headers=headers)
        html = rsp.content.decode(errors='ignore')
        json_object = json.loads(html)
        basePart = json_object["pd"]["basePart"]
        content = []
        for spec in json_object["pp"]["buyersGuides"]:
            buyersGuideDesc = spec["buyersGuideDesc"]
            content.append(buyersGuideDesc)
        vehicle = '\n'.join(content)
        list_ = []
        for spec in json_object["pp"]["partSpecs"]:
            dict_ = {}
            attributeName_en = spec["attributeName_en"]
            siteValue_en = spec["siteValue_en"]
            dict_[attributeName_en] = siteValue_en
            list_.append(dict_)
        formatted_data = {str(index): item for index, item in enumerate(list_)}
        json_data = json.dumps(formatted_data)
        df_transit = pd.DataFrame([{'Part Number': basePart, 'Buyer Guide': vehicle, 'Part Specifications': json_data}])
        df = pd.concat([df, df_transit], ignore_index=True).fillna('')
        rsp.close()
    except Exception as e:
        error_.append(p)
        time.sleep(1)
        continue

df.to_excel('./SMP_detail.xlsx', index=False)

