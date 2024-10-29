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
    '__uzma': '8efa63b2-5b59-482c-b4b5-9487d7862a23',
    '__uzmb': '1723596676',
    '__uzme': '5209',
    'AMP_MKTG_f93443b04c': 'JTdCJTdE',
    'cid': 'rBiPWaMlw0K7sOkA%23469222263',
    '__ssds': '2',
    '__uzmaj2': '9ed18687-3fb2-466d-a0db-180c7e6eca5e',
    '__uzmbj2': '1723596687',
    'utag_main__sn': '1',
    '_gcl_au': '1.1.1193484553.1723596701',
    '_fbp': 'fb.1.1723596701882.643149592300209675',
    '__uzmlj2': 'bJVcz5GtV5oJp3toDqqWMSPwdcPlcLIHD8QlMoEa3bg=',
    '__gsas': 'ID=151fc2379bf4647b:T=1723597742:RT=1723597742:S=ALNI_MbFXDC6BZ7uSb0mEzNmu72Sp4WLXg',
    'shs': 'BAQAAAZGG1Rg0AAaAAVUAD2idMzkyMjE4NjUxOTQxMDAzLDKN9yHc8y2CBeYlJzVICPkpT7TxnQ**',
    'ak_bmsc': '113EC7763B5248F409151FE955F0BF30~000000000000000000000000000000~YAAQXlcyuFt2lI6RAQAABBEWohjItBkG+04fSw9oxo2/PgsYJUp0XyyTmevJ1p4DbIjIxwP2kvKEBXH1Q4ce3Ftv1JvKWk5EsEDTAVU/SwovyvQEfI8Rn+7EWVViDxZku17Ar4KbqW7ZX01WXnhksbdXjPhS3RmlrGgqd3Mm0wXoNpdRefU4UFDf0dNfCQsjJt5onSRqL6Ulsu6ZyZreLB42WTlR4cMMObu/milltB6iv7+/TqeU5314T3No7pTsPY/YeMjp3vBjnx8bQU23032QS/6BWmLj0aycnmTerxdQb+lNuXbr+7V0NVFKp28SKrl3dz8lzjSDkyZLH5YjPIrBH8fKdCqI+xKu5zj9c75ao5y4PcWyARObK8cMIIqsIUlo2E2f',
    '__ssuzjsr2': 'a9be2cd8e',
    '__uzmcj2': '97288133918544',
    '__uzmdj2': '1725001314',
    '__uzmfj2': '7f60005a929bdc-3b5b-45e2-ab0b-761e825af44f17235966878211404627103-af68cd7f3d10d4321336',
    '__deba': 'BSMonH9oZbLeqKowEqQYz4rl_p1bEt2kdJr5buVGsMIwa-kr0DSdNiC8kwzPDL3bsA9sjxKW-LXTAvet5oksGLa7ci_qb88uyoNVlijHlw3W6v-QdEo83d5arzxSi_HlbkZP38YN2ObMqXv073kLfw==',
    '__uzmc': '63895237731720',
    '__uzmd': '1725001316',
    '__uzmf': '7f60005a929bdc-3b5b-45e2-ab0b-761e825af44f17235966765551404640189-2e74c101e43d4b0d2377',
    '__gads': 'ID=8cd97c1e52c80d01:T=1725001318:RT=1725001318:S=ALNI_MYpF9ZolBeqKKzNiWci2T07KAGvIQ',
    '__gpi': 'UID=00000ee32c1e45ae:T=1725001318:RT=1725001318:S=ALNI_MYM8h0OXm4Jt16LhrRZ5jjV2p3NRg',
    '__eoi': 'ID=3941d8cfede7ca0b:T=1725001318:RT=1725001318:S=AA-AfjZtdd1vn3IPZZl_ynP5K3Pw',
    's': 'CgAD4ACBm0sBBNGU1ZTEzNWUxOTEwYWFiMzZkYzU2ZmU4ZmZmZTNjNTeB1WC8',
    'bm_sv': 'BE44A029F864CE5584A147BF44B09083~YAAQXlcyuIXklI6RAQAAwI8Zohg62CmU2ko7FD+RJ15fjz/4y+ctjAgc9UYyz5jkQrT3lIx0FpyjZCLw1VhIsAaFzRxl2P5YaIQeTkm/KEGACJUFziHeW7VgCTtzQussQi89pkCzAVliAnhoMiJhMJtf7TrZ11MMgJtGwnMNHuYcpP4nk7ePXugdY9e4lcNg8jG/rV51sd6/IXEsOuetNKIDRP4K628nJBvUNdVhP2LmkZYzNoZoO35VnwGga8g=~1',
    'ebay': '%5Ejs%3D1%5Esbf%3D%23000000%5Epsi%3DAFy3P3Yo*%5E',
    'dp1': 'bu1p/eWFuZy0xMDE0OTQ*6a93d61a^kms/in6a93d61a^pbf/%232000000e000e0000000808000000468b2a29a^u1f/yangteng6a93d61a^expt/000172359675500567ac9993^bl/USen-US6a93d61a^',
    'ns1': 'BAQAAAZBR14g6AAaAAKUADWiyopoyMzYyODgzMzM1LzA7GZ0Q1NSegBuWNhSQQwLIliX0wKQ*',
    'nonsession': 'BAQAAAZBR14g6AAaAAAQAC2idMzl5YW5nLTEwMTQ5NAAQAAtosqKaeWFuZy0xMDE0OTQAMwAOaLKimjkxNzEwLTU0MTcsVVNBAEAAC2iyopp5YW5nLTEwMTQ5NACcADhosqKablkrc0haMlByQm1kajZ3Vm5ZK3NFWjJQckEyZGo2TUhsb0NwQUpPQm9nbWRqNng5blkrc2VRPT0AnQAIaLKimjAwMDAwMDAxAMoAIGqT1ho0ZTVlMTM1ZTE5MTBhYWIzNmRjNTZmZThmZmZlM2M1NwDLAAJm0XYiMjMBZAAHapPWGiMwMDAwOGGg77EADynjNIfZ5omDKnPh+/8SZg**',
    'ds2': 'asotr/b8_5azzzzzzz^',
    'totp': '1725001636607.GfUXkvQPaiXJk1AJQoBnEGypzpVwcDPR8OT4bPzslYK/BknB3kPikfwjQ9dkrb3JXk2h6g9d5YBvhLFoOh7GTQ==.XMYN6I1dAkCuUSomMgov3RgCwK1fr6tOw6rXi2XYY8s',
    'AMP_f93443b04c': 'JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJiZmFmYTk5MC1hOTNlLTRiOTEtYmUzZC01MzVhYTE2NTQ5ZWUlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzI1MDAxMjQ0NTY3JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTcyNTAwMTY0NjMwNCUyQyUyMmxhc3RFdmVudElkJTIyJTNBMTA2NiUyQyUyMnBhZ2VDb3VudGVyJTIyJTNBOSU3RA==',
}
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-full-version': '"128.0.6613.113"',
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
    'referer': 'https://www.ebay.com/'
}
Item = []
Num = []
page = 1

def fetch_data(p):
    Test = 5
    for test in range(Test):
        try:
            url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=radiator&_sacat=0&_odkw=68003557AA&_osacat=0&_ipg=240'
            # url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=radiator&_sacat=0&_ipg=240&_pgn={}'.format(p)
            rsp = requests.get(url=url, cookies=cookies, headers=headers, proxies=Proxy.get_Proxy_Requests())
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


