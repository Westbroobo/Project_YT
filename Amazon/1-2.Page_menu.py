"""
Filename:1-2.Page_menu.py
Author: Westbroobo
Date: 2024/8/29
"""

import requests
from tool import UA
from lxml import etree
import pandas as pd
import time

ASIN = []
Num = []
cookies = {
    'session-id': '133-9846465-1707349',
    'session-id-time': '2082787201l',
    'i18n-prefs': 'USD',
    'ubid-main': '131-3295320-4720951',
    'lc-main': 'en_US',
    'JSESSIONID': 'C282E0117159BA6C797B0B2ECCD8FF8D',
    'session-token': 'xrsRGIBvxmG6iMAz9XbaoCSSQoxs2YiqbAT2FVtoay38wAreFFOxRuX8TVdvsUWwm4B/Zk5hZC0tcdptZQcNIUCUbCpEYZdw1vXOX2bIOy1A2FdsOhCtGOJxyMEqvRDAmKMK3DnggZSmSrvZarEJZD30fBIWLsu/om3gAsVhwQ2AhDbzFNf/xl9EYGTFMh6g3xLfSawhcUObfBwBjHKG3sAR1Fj5vs+WD99Qo+YKC+hp5V3o6T9VDWxP9d3iKNwQ95xRy/t+C1leLoRIRkJA6AtydMMHyC47BjkvqXrmAnYUk/cwhiM5pSwaqOPUK95EqxRtvr5NMS2Ze7yyQZ2FdDRe2HFTrb8v',
    'csm-hit': 'adb:adblk_no&t:1724829606579&tb:FP4AD84KR307XJV7B6DM+s-FP4AD84KR307XJV7B6DM|1724829606579',
}
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'device-memory': '8',
    'downlink': '1.3',
    'dpr': '1',
    'ect': '3g',
    'priority': 'u=0, i',
    'rtt': '300',
    'sec-ch-device-memory': '8',
    'sec-ch-dpr': '1',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-ch-viewport-width': '499',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': UA.get_UA(),
    'viewport-width': '499',
}
page = 20
for p in range(1, page+1):
    try:
        url = 'https://www.amazon.com/s?k=BH+SENS+tpms+sensor&page={}&crid=G21IJI59BUU0&qid=1725007564&sprefix=bh+sens+tpms+sensor%2Caps%2C526&ref=sr_pg_{}'.format(p, p)
        rsp = requests.get(url=url, cookies=cookies, headers=headers)
        tree = etree.HTML(rsp.text)
        search_results = tree.xpath('//*[@class="s-main-slot s-result-list s-search-results sg-row"]/div')
        num = 0
        for div in search_results:
            asin = div.get('data-asin')
            if asin != '':
                num += 1
                ASIN.append(asin)
                Num.append(num)
        rsp.close()
    except:
        time.sleep(1)
        print(p)
        continue


df = pd.DataFrame(columns=['No.', 'ASIN'])
df['No.'] = Num
df['ASIN'] = ASIN
df.to_excel('./menu.xlsx', index=False)


