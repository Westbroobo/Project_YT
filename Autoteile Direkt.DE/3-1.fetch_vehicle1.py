"""
Filename:3-1.fetch_vehicle1.py
Author: Westbroobo
Date: 2024/9/10
"""

import time
import requests
from lxml import etree
import pandas as pd

cookies = {
    'cf_clearance': '6EBthzmiWw0har7Ms9Q.9dhlaXelN5p_OKI4BDSAdRw-1725690818-1.2.1.1-EAAF737qbpLyhpqP.DyF9l4D7q9hIFQlSHN5fCRy3r6fS5XSu6z8MRqOpVGgfw9DmPOY0GLv1aqySY_T8M0vqFkJdIL6Wh9Ih8GQSkDBgPPdfhGN1nqLHByfImDHkb5oWzSj2VnmAImf602DVI9eyDz6GpbS761BsehTpSD.JVP6bysSGI9OZIa3QLiYf4EqamSe3jpQCbeH0tTSBgye8GYcR2JVQGi57GjCsCASH8z3jYdPl8kb_RytqBptNedts9PZyWCepq7PqcU2bdhjQwR1OYs65EeJZQjjrr19tF482IqyO6NWb9WqNqvqSNAH6Elm6k14FX6J0lo55z4IA2j0bs1JFefuv_NC7kjczSaED2tsfMZUDxrF5sbnQbzkONYFbsE2CuB0X6cCroB6Q4ky25vi1WXW5X8fjkcS380d416ZvatPtadCDcebpJEH',
    'kmtx_sync': '3893828442274565296',
    'kmtx_sync': '3893828442274565296',
    '_fbp': 'fb.1.1725690835852.43780976221083146',
    'INGRESSCOOKIE': '1725935102.938.14141.51617|f89e2d2acc6cd8c158ba7aaea6f7fb53',
    'clientCode': '243324',
    '_gcl_au': '1.1.308737845.1725935108',
    '_ga': 'GA1.1.1170940819.1725935105',
    'tb_visit_counter_direkt_de': 'eyJpdiI6Ild3TjdlYU5rUGtXWDdLclQxeG1kTnc9PSIsInZhbHVlIjoidFZzN05OQ0c0eERFeHFrNnNINVk2UVAwNDZvZmw5WnZ5VFhWWjlCOWIraTFQb3d2K0dKcmxHUGdqQkZ3WHprayIsIm1hYyI6IjNhMTZmMmJhNDRhNmNlYWQ2OGQ3YjMxMjZjOGQzZDA5ODg5MDFjMTI4MDdlYzlmMGVkZDhkNjQxMTA3ZDg5YmEiLCJ0YWciOiIifQ%3D%3D',
    '__cf_bm': 'lq2G3LcYWD5mhLwRiTAyxQ4hoxejdtRkO1ibaZi_3b8-1725947143-1.0.1.1-P3pN1vxx_s7XWmmUSWEUtYD0EfUPXHWBTyxT03hjmHTvCRpXQ5iTub8du47r0URcEhtTIcvI.kbd.1jNs63rcvfLnm0bKIlzHjF._ecCPnk',
    'kmtx_sync_pi': '99be6966-4d98-4036-8a78-9768bd240cdb',
    '_uetsid': 'e6fbd1c06f1b11ef871c91300f4033c2',
    '_uetvid': '26dcbdb06ce311ef8d2a756a0cf7b6c1',
    '_ga_DHWDNTWLEQ': 'GS1.1.1725947154.3.1.1725947538.50.0.1794647297',
    'XSRF-TOKEN': 'eyJpdiI6InRtRWdQWHNDNWdMak9FdDNpbHNOUGc9PSIsInZhbHVlIjoiQjZpaG1MQ2dLY1FZRHVOMEpORlBTbGZZaFM5RnpwMXV2aDMzZDRFUnVrNHZXTk1ENk5VOFBWYjREVE1LemxwZVdhek1zNGc5aThOYjZLRXNraUlSSk5jM2lCVnNtNFpEeCtRc0RlVTlVanMyeStSbEkvV0ZGbERiZ1NOZTRvR2YiLCJtYWMiOiI0MDA3N2VhNjI0NWZhNzdjZGFkMTIxNjJjZDhjNDI5MjQzYjYwYjBiOTI0NGY1NDZmYTZmYzFlNTQ0ZGZlNjU0IiwidGFnIjoiIn0%3D',
    'l': 'eyJpdiI6IldnWTFUWlNEVDJkRldrdTZoQ1NKeHc9PSIsInZhbHVlIjoiNVBob2ZaQTM4Z1gwUW5TYnljZ3V5MU1XYWVNTHhDajF5dFBIeWZPakZkZFZnZ21ZS3lPSm4wRnZCaGhMalducTZaU2V2Z2ZUQU9pdU1vYzVXdkdyakZGMmswbWhJRUh2WkN5eFRKRDYxSGNQelZTRG4xK0xRaytwZUVHMC8zTUciLCJtYWMiOiJmMzA1YzUzYmViMmE0NGQ0ZmRkNzNiYWMyNmNiNWMzNzliMjViMWI3ZTVlNTI3MTM3NTEzOTUzNWI1Y2ZlNjk5IiwidGFnIjoiIn0%3D',
}
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"128.0.6613.120"',
    'sec-ch-ua-full-version-list': '"Chromium";v="128.0.6613.120", "Not;A=Brand";v="24.0.0.0", "Google Chrome";v="128.0.6613.120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}
df_ = pd.read_excel('./detail.xlsx')
ProductId = df_['Product Id'].tolist()
Vehicle_Make = df_['Vehicle_Make'].tolist()

df_make = pd.DataFrame(columns=['Product Id', 'Make', 'Make ID', 'Model'])
error_ = []
success = 0
for productId in ProductId:
    try:
        vehicle_make =  Vehicle_Make[ProductId.index(productId)]
        for item in eval(vehicle_make):
            makerId = eval(vehicle_make)[item]
            url_make = f'https://www.autoteiledirekt.de/ajax/product/related-auto?productId={productId}&makerId={makerId}'
            rsp = requests.get(url=url_make, headers=headers, cookies=cookies)
            tree = etree.HTML(rsp.text)
            lis = tree.xpath('//li[@class="compatibility__model"]')
            dict__ = {}
            for li in lis:
                model = li.xpath('./div/text()')[0].strip()
                model_id = li.xpath('./div')[0].get('data-model-id')
                dict__[model] = model_id
            df_transit = pd.DataFrame([{'Product Id': productId, 'Make': item, 'Make ID': makerId, 'Model': str(dict__)}])
            df_make = pd.concat([df_make, df_transit], ignore_index=True)
            rsp.close()
        success += 1
        print('success-{}, error-{}, processing-{}'.format(success, len(error_), len(ProductId) - success - len(error_)))
    except:
        error_.append(productId)
        print('success-{}, error-{}, processing-{}'.format(success, len(error_), len(ProductId) - success - len(error_)))
        time.sleep(1)
        continue

df_make.to_excel('./Vehicle_1.xlsx', index=False)




