"""
Filename:5.Cardone_search.py
Author: Westbroobo
Date: 2024/9/13
"""

import requests
import pandas as pd
import time
import re
from tool import UA

df_menu = pd.read_excel('./Cardone_menu.xlsx', header=0)
Part_Number = df_menu['Part_Number'].to_list()
type_ls = []
part_ls = []
count = 0
for part_number in Part_Number:
    try:
        headers = UA.get_User_Agent_Requests()
        headers['referer'] = 'https://www.cardone.com'
        params = {
            'search_query': str(part_number),
            'f': str(part_number),
            'sort': 'relevance',
        }
        rsp = requests.get('https://www.cardone.com/search.php', params=params, headers=headers)
        t = re.findall('<strong>Type:(.+?)</p>', rsp.text)
        if len(t) != 0:
            type_ = t[0].split('</strong>')[-1]
        else:
            type_ = ''
        part_ls.append(part_number)
        type_ls.append(type_)
        rsp.close()
        count += 1
        print(count)
    except:
        count += 1
        print(part_number, count)
        time.sleep(1)
        continue

df = pd.DataFrame(columns=['Part_Number', 'Type'])
df['Part_Number'] = part_ls
df['Type'] = type_ls
df.to_excel('./Cardone_type.xlsx', index=False)


