"""
Filename:1.eBay_item.py
Author: Westbroobo
Date: 2024/8/30
"""

from gevent import monkey, pool
monkey.patch_all(thread=False)
import requests
import re
import time
from tool import UA, Proxy
import pandas as pd
import math

cookies = {
    '__uzma': '6a946330-6f4e-4e0f-bf5b-7f2dc59681cc',
    '__uzmb': '1723596762',
    '__uzme': '9627',
    'cid': 'rtGJxMGrMTP6DvvZ%231787088840',
    '__ssds': '2',
    '__uzmaj2': 'cf401a82-2290-4762-bbff-c170c7639448',
    '__uzmbj2': '1723596775',
    '__uzmlj2': '1wFi4POLMnfGxtNJi/brATI9MbTWgWJarlSEdiFQoi8=',
    '_gcl_au': '1.1.1206382020.1724034475',
    '_pin_unauth': 'dWlkPU1EVTJaR1ZoT1RndE9ETXdZaTAwWmpSaUxXSXdNRGt0WVRnMk1tTXlaRFJqTlRZNA',
    '_fbp': 'fb.1.1724034477258.158101776588160977',
    'shs': 'BAQAAAZGG1Rg0AAaAAVUAD2idM4MyMjE4NjUxOTQxMDAzLDIhloZ2mR8IZTgTl6aj38ALmhL8EA**',
    'AMP_MKTG_f93443b04c': 'JTdCJTdE',
    '__gsas': 'ID=50a8dc273da81240:T=1725323526:RT=1725323526:S=ALNI_MaQMDqM4jlYWxEvg0dJdoR3wg-H0Q',
    '__ssuzjsr2': 'a9be2cd8e',
    'ak_bmsc': 'BF476594CFFF701C9AA91197C90583BD~000000000000000000000000000000~YAAQlVcyuLJnv7ORAQAAE4rTthj+PcMcQx38BVxZ8YGIJLPQ6ZEuKmVZC/hH7De5bz8OpygU7C1v260mOn1r7c0dOLWYRL3WACeE3XRYYZOB3L+YrsyAjjUdYWROOH0lmKv3urz9qlateP2M8lyY6YeWBLXmqx4ZgD+eNoi4CY3TBqjSaWovAED2T3zCXJKvfBZNOORunt2kaaLMGuv7Xukep1ltiZ/Ao/mdBjjGA4bzX6HyvynkB/oqhBc+JCjFzWHPOxdAwuUyOgp155krz6ez9rdhwXkMVz5dd7VD7qC39/dn/kBGAfF3zBmbXY6r9mT0PVJhwE08lEHQrOUpnr9h+b+3mQkcVkJIPsHPtmuadEeFnIZSQOtkB4DlvqH3UE+qgaA=',
    'utag_main__sn': '9',
    'utag_main_ses_id': '1725352052747%3Bexp-session',
    '__gads': 'ID=5b30965c3a097cc4:T=1725325695:RT=1725352492:S=ALNI_Ma8Miyz8jcu8d1osoulNDLcU8s4-w',
    '__gpi': 'UID=00000eea9fba1122:T=1725325695:RT=1725352492:S=ALNI_MbLQEiGoFpmv444j9G6vnYFDJNYhg',
    '__uzmcj2': '5163819661277',
    '__uzmdj2': '1725352665',
    '__uzmfj2': '7f6000d11bb8f3-0099-435f-9279-b809986d0d4517235967755241755889526-4e89d1afac3d3925196',
    'utag_main__ss': '0%3Bexp-session',
    'utag_main__se': '3%3Bexp-session',
    'utag_main__st': '1725354479953%3Bexp-session',
    'utag_main__pn': '3%3Bexp-session',
    'cto_bundle': 'Yt3AQF9QemhwcVY2QUN1UkVONW85NlNqWlB5NiUyRkJYbmFIQ2VVMCUyRkplJTJGNHRKOWVwTFQ3SGtyJTJCYjJYdzNaTGc1Rk5RYkgyJTJCaDlCJTJCQ1daWTBCVkpsU0lFWlJMUTFKRlI2ZWRtRWYlMkJlS0xBSWFFTHd5Qkc0R3BtNko5czRub0RudU1WWVl0UVpUbEclMkZJZUE2UUYzaWJsdDJwVFVnJTNEJTNE',
    '_uetsid': 'cf7d206069cf11ef9cf043a45a3e33a7|1lmnoy3|2|fov|0|1707',
    '_uetvid': 'af91df805dd211ef9a188581b088cdb8|1238edk|1725352684945|2|1|bat.bing.com/p/insights/c/e',
    '__deba': '9xUzzMmIDQpxF_hROW4vkKSPf9SdrgTuA_qZslhkPDlcCYrNxywqt6JxaMTpZMyrJGGSn4EAAKx72GOtZsqSrsfIp8YWLdGXVxFwpDOIJvrxA4VJ0ODuMtxWoLO0ACc5bAieeLuHEc8rx6cup6vwEw==',
    '__uzmc': '6136736777172',
    '__uzmd': '1725352737',
    '__uzmf': '7f6000d11bb8f3-0099-435f-9279-b809986d0d4517235967620891755975172-3bdc8c0677234835367',
    'ds2': 'asotr/b8_5azzzzzzz^',
    'ebay': '%5Epsi%3DA%2F1JtoeA*%5Ejs%3D1%5Edv%3D66d6ca2b%5Esbf%3D%23%5E',
    'dp1': 'bexpt/000172359687002767ac9a06^bl/US6a99323a^kms/in6a99323a^pbf/%230000e000e0000000808000000068b7feba^tzo/-1e066d6d94a^u1p/eWFuZy0xMDE0OTQ*6a99323a^u1f/yangteng6a99323a^',
    'ns1': 'BAQAAAZGG1Rg0AAaAAKUADWi3/royMzYyODgzMzM1LzA7vUq96esXjX7gp3ox+fG31ICzrHI*',
    's': 'CgAD4ACBm2By6NGU1ZjYyYmMxOTEwYWM2YTA2MGEzYTA5ZmZmOTExYTAA7gCPZtgcujMGaHR0cHM6Ly93d3cuZWJheS5kZS9zY2gvaS5odG1sP19mcm9tPVI0MCZfdHJrc2lkPXAyMzM0NTI0Lm01NzAubDEzMTMmX25rdz1FeGhhdXN0K01hbmlmb2xkKyZfc2FjYXQ9MCZfb2Rrdz0xNzE0MTc0MjAwJl9vc2FjYXQ9MCZMSF9QcmVmTG9jPTEHsfVDLQ**',
    'nonsession': 'BAQAAAZGG1Rg0AAaAABAAC2i3/rp5YW5nLTEwMTQ5NABAAAtot/66eWFuZy0xMDE0OTQAMwAOaLf+ujkxNzEwLTU0MTcsVVNBAAQAC2idM4N5YW5nLTEwMTQ5NAFkAAdqmTI6IzAwMDA4YQDKACBqmTI6NGU1ZjYyYmMxOTEwYWM2YTA2MGEzYTA5ZmZmOTExYTAAywADZtbSQjE0NgCcADhot/66blkrc0haMlByQm1kajZ3Vm5ZK3NFWjJQckEyZGo2TUhsb0NwQUpPQm9nbWRqNng5blkrc2VRPT0AnQAIaLf+ujAwMDAwMDAxeVwaFzaXu8AsFP6LMHr+p0ps21o*',
    'bm_sv': '535AED344C69638D2EE0F0E8A6F34C2A~YAAQVlcyuD4PupeRAQAALd8JtxiIH2B6pziRsG0FDAdfuFieGcgBaogn/YPgsMy37/sHUYD25yc6YqIlm/lTVOWdH4vMWotW2gJwqRGe+cG+CaOAFw++pkKZZ5l+REvBO5s/sGxzRZEz9FNL3UoidWiSJsQ8zvIij0IRUAOysQz0+JYIwh+MTVcRUxPdbivtwGCsGnbuBTh+Az0bHnnDm0DBvsHItfpb9NUwB+8L2ihlp4KNKiBQSbKcSKh2RQ==~1',
    'totp': '1725352773834.ikhi3KcKN/MoyfiyIWTjqQVHFKJBSa6/0lF9yA4WDgfN4a9FW82gb7pXZpWhOmgk7PpzYXU+3DfUsNHOBLf+pA==.6PdnjPVoBdQ8gZtGMBX3gYxJfbKcKwz6ijbgFZe4m7s',
    'AMP_f93443b04c': 'JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI2NDhiNTk4ZS1jMmEyLTQyMGYtYjViMC0zNTk4NTBkZWRiNmElMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzI1MzQxNjg4MDU4JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTcyNTM1Mjc3ODM4NSUyQyUyMmxhc3RFdmVudElkJTIyJTNBNDU0JTJDJTIycGFnZUNvdW50ZXIlMjIlM0ExMjglN0Q=',
}
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-full-version': '"128.0.6613.114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': UA.get_UA(),
    'referer': 'https://www.ebay.de/'
}
Item = []
Num = []
page = 1

def fetch_data(p):
    Test = 1
    for test in range(Test):
        try:
            url = 'https://www.ebay.de/sch/i.html?_from=R40&_nkw=Exhaust+Manifold+&_sacat=0&LH_PrefLoc=1&_ipg=60'
            # url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=radiator&_sacat=0&_ipg=240&_pgn={}'.format(p)
            rsp = requests.get(url=url, cookies=cookies, headers=headers, proxies=Proxy.get_Proxy_Requests())
            print(rsp.text)
            status_code = rsp.status_code
            MC = re.findall('window.\\$MC\\|\\|\\[\\]\\).concat\\((.+?)</script>', rsp.text)
            mainSearchContext = re.findall('mainSearchContext(.+?)variant', MC[0])
            itemId = re.findall('itemId\":(.+?),', mainSearchContext[0])
            num = len(Item)
            for item in itemId:
                num += 1
                Item.append(item)
                Num.append(num)
            if status_code == 200:
                rsp.close()
                print('第{}页【尝试次数：{}】-success，进度：{}/{}'.
                      format(p, test + 1, math.ceil(len(Item)/240), page))
                break
        except Exception as e:
            print(e)
            time.sleep(0.3)
            if test == Test-1:
                print('第{}页【尝试次数：{}】-error'.format(p, test))
            continue

pool = pool.Pool(15)
for p in range(1, page+1):
    pool.spawn(fetch_data, p)
pool.join()

df = pd.DataFrame(columns=['No.', 'Item'])
df['No.'] = Num
df['Item'] = Item
df.to_excel('./menu.xlsx', index=False)


