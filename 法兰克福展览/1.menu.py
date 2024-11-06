"""
Filename:1.menu.py
Author: Westbroobo
Date: 2024/11/5
"""
# 1-237
from gevent import monkey, pool
monkey.patch_all(thread=False)
import requests, re, time
import pandas as pd
from tool import UA, Proxy
df = pd.DataFrame(columns=['CompanyName', 'ExhibitorUrlRewrite', 'Pstands', 'PageNumber'])

def fetch_data(pageNumber):
    global df
    num = 50
    for test in range(num):
        try:
            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Origin': 'https://automechanika-shanghai.hk.messefrankfurt.com',
                'Referer': 'https://automechanika-shanghai.hk.messefrankfurt.com/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
                'User-Agent': UA.get_UA(),
                'apikey': 'LXnMWcYQhipLAS7rImEzmZ3CkrU033FMha9cwVSngG4vbufTsAOCQQ==',
                'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }
            params = {
                'language': 'zh-CN',
                'q': '',
                'orderBy': 'name',
                'pageNumber': pageNumber,
                'pageSize': '25',
                'orSearchFallback': 'false',
                'showJumpLabels': 'true',
                'findEventVariable': 'AUTOMECHANIKASHANGHAI',
            }
            rsp = requests.get(
                'https://api.messefrankfurt.com/service/esb_api/exhibitor-service/api/2.1/public/exhibitor/search',
                params=params,
                headers=headers,
                proxies=Proxy.get_Proxy_Requests()
            )
            status_code = rsp.status_code
            companyName = re.findall('\"presentationName\":\"(.+?)\",', rsp.text)
            exhibitorUrlRewrite = re.findall('\"exhibitorUrlRewrite\":\"(.+?)\",', rsp.text)
            pstands = re.findall('\"pstands\":\\[(.+?)]', rsp.text)
            # hallAndLevel = re.findall('\"hallAndLevel\":\"(.+?)\",', rsp.text)
            # firstBoothNumber = re.findall('\"firstBoothNumber\":(.+?)\",', rsp.text)
            df_transit = pd.DataFrame(columns=['CompanyName', 'ExhibitorUrlRewrite', 'Pstands', 'PageNumber'])
            df_transit['CompanyName'] = companyName
            df_transit['ExhibitorUrlRewrite'] = exhibitorUrlRewrite
            df_transit['Pstands'] = pstands
            df_transit['PageNumber'] = [pageNumber for i in range(len(df_transit))]
            df = pd.concat([df, df_transit], ignore_index=True)
            rsp.close()
            if status_code == 200:
                print('page：{}【尝试次数：{}】-success'.format(pageNumber, test + 1))
                break
        except Exception as e:
            time.sleep(0.3)
            # print(e)
            if test == num - 1:
                print('page：{}【尝试次数：{}】-error'.format(pageNumber, test))
                continue
pool = pool.Pool(10)
for pageNumber in range(1, 100):
    pool.spawn(fetch_data, pageNumber)
pool.join()
df.to_excel('./menu.xlsx', index=False)

