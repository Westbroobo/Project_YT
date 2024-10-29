"""
Filename:2.MAVAL.py
Author: Westbroobo
Date: 2024/9/13
"""

import re
import requests
import pandas as pd
import time
from tool import UA

df = pd.DataFrame(columns=['Part Number', 'Vehicle', 'OE', 'BBB INDUSTRIES', 'CARDONE'])
df_menu = pd.read_excel('./MAVAL_menu.xlsx', header=0)
Part_Number = df_menu['Part Number'].to_list()
Url = df_menu['Url'].to_list()
error_ = []
for url in Url:
    part_number = Part_Number[Url.index(url)]
    headers = UA.get_User_Agent_Requests()
    headers['referer'] = 'https://mavalgear.com/'
    try:
        rsp = requests.get(url=url, headers=headers)
        # print(rsp.text)
        try:
            description = re.findall('Application Info:(.+?)Instructions', rsp.text)[-1].strip().replace('\\n', '')
        except:
            description = re.findall('Application Info:(.+?)\\"\\,', rsp.text)[-1].strip().replace('\\n', '')
            print(description)
        application_info = description.split('Interchange:')[0]
        interchange = re.findall('Interchange: (.+?)BBB', description)[0].replace(', ', ';').strip()
        try:
            bbb_number = re.findall('BBB Cross-Reference: (.+?)Cardone', description)[0].replace(', ', ';').strip()
        except:
            bbb_number = ''
        try:
            cardone_number = re.findall('Cardone Cross-Reference: (.*)', description)[0].replace(', ', ';').strip()
        except:
            cardone_number = ''
        df_transit = pd.DataFrame([{'Part Number': part_number, 'Vehicle': application_info, 'OE': interchange,
                                    'BBB INDUSTRIES': bbb_number, 'CARDONE': cardone_number}])
        df = pd.concat([df, df_transit], ignore_index=True).fillna('')
        print('success-{}, error-{}, processing-{}'.format(len(df), len(error_), len(Part_Number) - len(df) - len(error_)))
    except:
        error_.append(part_number)
        print('success-{}, error-{}, processing-{}'.format(len(df), len(error_), len(Part_Number) - len(df) - len(error_)))
        time.sleep(1)
        continue

df.to_excel('./MAVAL.xlsx', index=False)
