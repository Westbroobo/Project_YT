"""
Filename:2.WVE.py
Author: Westbroobo
Date: 2024/9/4
"""

import requests, re, json
from tool import UA
import pandas as pd
import time

df = pd.DataFrame(columns=['Part Number', 'Location', 'Image', 'Buyer Guide', 'Attributes'])
df_cargo = pd.read_excel('./WVE_cargo.xlsx')
cargos = df_cargo['cargo'].tolist()
error_ = []
for cargo in cargos:
    try:
        headers = UA.get_User_Agent_Requests()
        headers['refer'] = 'https://wellsve.com/'
        url = 'https://www.showmethepartsdb2.com/bin/ShowMeConnect.exe?cargo=' + cargo
        rsp = requests.get(url=url, headers=headers)
        part_no = re.findall('<part_no>(.+?)</part_no>', rsp.text)[0]
        location = re.findall('<location>(.+?)</location>', rsp.text)[0]
        images = re.findall('<id>(.+?)</id>', rsp.text)
        apps = re.findall('<app>(.+?)</app>', rsp.text)
        partattributes = re.findall('<partattributes>(.+?)</partattributes>', rsp.text)
        list_content = []
        for app in apps:
            make = re.findall('<make>(.+?)</make>', app)[0]
            model = re.findall('<model>(.+?)</model>', app)[0]
            year = re.findall('<year>(.+?)</year>', app)[0]
            engine = re.findall('<engine>(.+?)</engine>', app)[0]
            parttype = re.findall('<parttype>(.+?)</parttype>', app)[0]
            content = make + ' ' + model + ' ' + year + ' ' + engine + ' ' + parttype
            list_content.append(content)
        buyer_guide = '\n'.join(list_content)

        list_ = []
        for part in partattributes:
            dict_ = {}
            attribute = re.findall('<attribute>(.+?)</attribute>', part)[0]
            value = re.findall('<value>(.+?)</value>', part)[0].replace('&amp', '').replace(';lt;b;gt;', '').replace(';lt;/b;gt;', '')
            dict_[attribute] = value
            list_.append(dict_)
        formatted_data = {str(index): item for index, item in enumerate(list_)}
        json_data = json.dumps(formatted_data)

        df_transit = pd.DataFrame([{'Part Number': part_no, 'Location': location, 'Image': images,
                                    'Buyer Guide': buyer_guide, 'Attributes': json_data}])
        df = pd.concat([df, df_transit], ignore_index=True).fillna('')
        rsp.close()
        print('success-{}, error-{}, processing-{}'.format(len(df), len(error_), len(cargos) - len(df) - len(error_)))
    except:
        error_.append(cargo)
        time.sleep(1)
        print('success-{}, error-{}, processing-{}'.format(len(df), len(error_), len(cargos)-len(df)-len(error_)))
        continue

df.to_excel('./WVE.xlsx', index=False)


