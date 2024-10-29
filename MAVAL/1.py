"""
Filename:2.MAVAL.py
Author: Westbroobo
Date: 2024/9/13
"""

import re
import requests
import pandas as pd
import time
from lxml import etree
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
        tree = etree.HTML(rsp.text)
        p_tags = tree.xpath('//*[@class="product__description rte quick-add-hidden"]/p')[1:5]
        try:
            application_info = p_tags[0].xpath('./b/text()')[0]
            if application_info == 'Application Info: ' or application_info == 'Application Info: ':
                try:
                    application_info = p_tags[0].xpath('./b/span/text()')[0].strip()
                except:
                    application_info = p_tags[0].xpath('./text()')[0].strip()
            else:
                application_info = application_info.replace('Application Info:', '').strip()
        except:
            application_info = ''

        try:
            interchange = p_tags[1].xpath('./b/text()')[0]
            if interchange == 'Interchange: ' or interchange == 'Interchange: ':
                interchange = p_tags[1].xpath('./text()')[0].strip().replace(', ', ';')
            else:
                interchange = interchange.replace('Interchange:', '').strip().replace(', ', ';')
        except:
            interchange = ''

        try:
            bbb_number = p_tags[2].xpath('./b/text()')[0]
            if bbb_number == 'BBB Cross-Reference: ' or bbb_number == 'BBB Cross-Reference: ':
                bbb_number = p_tags[2].xpath('./b/span/text()')[0].strip().replace(', ', ';')
            else:
                bbb_number = bbb_number.replace('BBB Cross-Reference:', '').strip().replace(', ', ';')
        except:
            bbb_number = ''

        try:
            cardone_number = p_tags[3].xpath('./b/text()')[0]
            if cardone_number == 'Cardone Cross-Reference: ' or cardone_number == 'Cardone Cross-Reference: ':
                cardone_number = p_tags[3].xpath('./b/span/text()')[0].strip().replace(', ', ';')
            else:
                cardone_number = cardone_number.replace('Cardone Cross-Reference:', '').strip().replace(', ', ';')
        except:
            cardone_number = ''
        df_transit = pd.DataFrame([{'Part Number': part_number, 'Vehicle': application_info, 'OE': interchange,
                                    'BBB INDUSTRIES': bbb_number, 'CARDONE': cardone_number}])
        df = pd.concat([df, df_transit], ignore_index=True).fillna('')
        print('success-{}, error-{}, processing-{}'.format(len(df), len(error_), len(Part_Number) - len(df) - len(error_)))

    except Exception as e:
        # print(e)
        error_.append(part_number)
        print('success-{}, error-{}, processing-{}'.format(len(df), len(error_), len(Part_Number) - len(df) - len(error_)))
        time.sleep(1)
        continue

df.to_excel('./MAVAL.xlsx', index=False)
