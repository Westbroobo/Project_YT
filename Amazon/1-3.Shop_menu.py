"""
Filename:1-3.Shop_menu.py
Author: Westbroobo
Date: 2024/8/29
"""

import requests
from tool import UA
import pandas as pd
import re

ASIN = []
Num = []
cookies = {
    'session-id': '133-9846465-1707349',
    'session-id-time': '2082787201l',
    'i18n-prefs': 'USD',
    'ubid-main': '131-3295320-4720951',
    'lc-main': 'en_US',
    'JSESSIONID': 'C282E0117159BA6C797B0B2ECCD8FF8D',
    'session-token': 'n2MeBbcDVGT1asmM6ubKFzm3WoB10xia7EayjtB3XSi5BypXxkbRFsyp38SSKyBXae9Rjcdq9qC26OheDZjSVnygiK7T9tRBNibvm+rkS8QLfPokf+shc3OF7ZFMICmd3a8dk25MgP0sY9hbNhhpXhb5yCXcizxPDoiY1JExQ0py7Z5YiE4W3Aq6LFpHla74G88Eto7vy5pinsELLYIvUa47zpvN6zZnmlhUIofXG6fzWA/V9cS441vMjknCx4vGiWW2c0vpoNRj/E69ZWdfB5bmIUgDLHpWDiM5AutR28lGQWBsAiY7+is8G2rham5F//bVLeK928ROZusNYNhkTyqXWZk6MdRV',
    'csm-hit': 'adb:adblk_no&t:1724833245491&tb:QDWPRFBF4B9VPW6AZXFT+b-71Y9X1KBSE048VY8TKM8|1724833245491',
}
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'device-memory': '8',
    'downlink': '4.85',
    'dpr': '1',
    'ect': '4g',
    'priority': 'u=0, i',
    'rtt': '250',
    'sec-ch-device-memory': '8',
    'sec-ch-dpr': '1',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-ch-viewport-width': '890',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': UA.get_UA(),
    'viewport-width': '890',
}

params = {
    'ref_': 'ast_bln',
    'store_ref': 'bl_ast_dp_brandLogo_sto',
    'terms': 'Air Conditional Control Panel',
}

rsp = requests.get(
    'https://www.amazon.com/stores/page/DE4F28F0-3AD5-43E6-B2E4-501862B521E0/search',
    params=params,
    cookies=cookies,
    headers=headers,
)
str_ASINList = re.compile('ASINList\":\\[(.+?)],').findall(rsp.text)
ASINList = str_ASINList[0].split(',')
num = 0
for asin in ASINList:
    num += 1
    asin = asin.replace('"', '')
    ASIN.append(asin)
    Num.append(num)

df = pd.DataFrame(columns=['No.', 'ASIN'])
df['No.'] = Num
df['ASIN'] = ASIN
df.to_excel('./menu.xlsx', index=False)


