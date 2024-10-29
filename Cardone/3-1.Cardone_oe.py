# -*- coding: utf-8 -*- 
# @Time ： 2024/7/29 14:03
# @Auth ： Westbroobo
# @File ：3-1.Cardone_oe.py


import requests
import pandas as pd
import time
from tool import UA

df_menu = pd.read_excel('./Cardone_auth.xlsx', header=0)
Part_Number = df_menu['Part_Number'].to_list()
Auth = df_menu['auth'].to_list()
headers = UA.get_User_Agent_Requests()
headers['referer'] = 'https://www.cardone.com'
part_ls = []
oes_ls = []
vehicle_ls = []
error_ = []
for part_number in Part_Number:
    try:
        auth = Auth[Part_Number.index(part_number)]
        url = 'https://productdesk-api.cellacore.net/legacy/cardone/FinishedGood/?' \
              'q=productDeskItemNumber.keyword:{}&size=1&useCache=true&auth={}'.format(part_number, auth)
        rsp = requests.get(url=url, headers=headers)
        data = rsp.json()
        list_oes = []
        try:
            CrossReferences = data[0]['CrossReferences']
            for crossReference in CrossReferences:
                if crossReference['referenceType'].strip() == 'OE Part':
                    list_oes.append(crossReference['reference'])
            oes = ';'.join(list(set(list_oes)))
        except:
            oes = ''
        try:
            vehicle = data[0]['ApplicationSummary'].replace('; ', '\n')
        except:
            vehicle = ''
        part_ls.append(part_number)
        oes_ls.append(oes)
        vehicle_ls.append(vehicle)
        rsp.close()
        print('success-{}, error-{}, processing-{}'.format(len(part_ls), len(error_), len(Part_Number)-len(part_ls)-len(error_)))
    except:
        error_.append(part_number)
        print('success-{}, error-{}, processing-{}'.format(len(part_ls), len(error_), len(Part_Number) - len(part_ls) - len(error_)))
        time.sleep(1)
        continue

df = pd.DataFrame(columns=['Part_Number', 'OE', 'Vehicle'])
df['Part_Number'] = part_ls
df['OE'] = oes_ls
df['Vehicle'] = vehicle_ls
df.to_excel('./Cardone_oe.xlsx', index=False)


