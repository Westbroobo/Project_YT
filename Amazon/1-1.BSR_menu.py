"""
Filename:1-1.BSR_menu.py
Author: Westbroobo
Date: 2024/8/29
"""

import requests
import re
from tool import UA
import pandas as pd

ASIN = []
Num = []
for pg in range(1, 3):
    url = ('https://www.amazon.com/Best-Sellers-Automotive-Automotive-Replacement-Fuel-Tank-Caps/'
           'zgbs/automotive/15723051/ref=zg_bs_pg_2_automotive?_encoding=UTF8&pg={}').format(pg)
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'session-id=133-9846465-1707349; session-id-time=2082787201l; i18n-prefs=USD; ubid-main=131-3295320-4720951; lc-main=en_US; skin=noskin; session-token=/aoNUXJ6HsW857xH+f0wx3eM7Rb2aHdCsrNg9jAyZMrYVOOyn3y7nluAuMlNtrWHuKrS6WpeCEZsX9QUcCQCEsAlN76yRyDNGeLl+lRYxwxYobqgRj1jVlyRlGSOqwDPMyIf02ebZOrKSTdg4UlnotMt0LfMqNznjk3QqzX9wt1BX9A/HNiDOgu38ZcMVJ1b5UMNHtcdVtN2EAYyhFIHCCTx/L0RRWoiVVHof4lrSVuS7FAnuNQf9aoGuDKM/ns+f47RC+1lA0kNXKDI0tamXpKAz3kIrJPSTD/D2sbv+i0u2WYYmFQDWXSibsYQKHD9mAqfPutzxEvjmgUlJmLC3e6HZ5Q7Lf4y; csm-hit=adb:adblk_no&t:1726032926587&tb:3ZYJVKG19SAM3DHBTH87+s-T65500VHB4Q8JKRWTBMG|1726032926587',
        'device-memory': '8',
        'downlink': '10',
        'dpr': '1',
        'ect': '4g',
        'priority': 'u=0, i',
        'rtt': '250',
        'sec-ch-device-memory': '8',
        'sec-ch-dpr': '1',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-ch-viewport-width': '703',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': UA.get_UA(),
        'viewport-width': '703',
    }
    rsp = requests.get(url=url, headers=headers)
    page_text = rsp.text
    CardsClient = re.compile(r'<!--CardsClient--><div id=(.+?)data-index-offset').findall(str(page_text))
    renders = re.compile('&quot;:&quot;(.+?);,&quot;render.zg.bsms.currentSalesRank&quot;').findall(str(CardsClient[0]))
    for render in renders:
        num = render.split('&quot')[-2].replace(';', '')
        asin = render.split('&quot')[-8].replace(';', '')
        Num.append(num)
        ASIN.append(asin)
df = pd.DataFrame(columns=['No.', 'ASIN'])
df['No.'] = Num
df['ASIN'] = ASIN
df.to_excel('./menu.xlsx', index=False)


