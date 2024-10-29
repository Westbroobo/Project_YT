"""
Filename:1.menu.py
Author: Westbroobo
Date: 2024/9/10
"""
import requests
from lxml import etree
import pandas as pd
import time

cookies = {
    'cf_clearance': '6EBthzmiWw0har7Ms9Q.9dhlaXelN5p_OKI4BDSAdRw-1725690818-1.2.1.1-EAAF737qbpLyhpqP.DyF9l4D7q9hIFQlSHN5fCRy3r6fS5XSu6z8MRqOpVGgfw9DmPOY0GLv1aqySY_T8M0vqFkJdIL6Wh9Ih8GQSkDBgPPdfhGN1nqLHByfImDHkb5oWzSj2VnmAImf602DVI9eyDz6GpbS761BsehTpSD.JVP6bysSGI9OZIa3QLiYf4EqamSe3jpQCbeH0tTSBgye8GYcR2JVQGi57GjCsCASH8z3jYdPl8kb_RytqBptNedts9PZyWCepq7PqcU2bdhjQwR1OYs65EeJZQjjrr19tF482IqyO6NWb9WqNqvqSNAH6Elm6k14FX6J0lo55z4IA2j0bs1JFefuv_NC7kjczSaED2tsfMZUDxrF5sbnQbzkONYFbsE2CuB0X6cCroB6Q4ky25vi1WXW5X8fjkcS380d416ZvatPtadCDcebpJEH',
    'kmtx_sync': '3893828442274565296',
    'kmtx_sync': '3893828442274565296',
    '_fbp': 'fb.1.1725690835852.43780976221083146',
    'INGRESSCOOKIE': '1725935102.938.14141.51617|f89e2d2acc6cd8c158ba7aaea6f7fb53',
    'clientCode': '243324',
    '_gcl_au': '1.1.308737845.1725935108',
    '_ga': 'GA1.1.1170940819.1725935105',
    '__cf_bm': 'w2LjVHNvCKO.CfKF5XhIeMZzpJ7DyKVgt71erXY.0zE-1725937795-1.0.1.1-MV8k.WOF_1BwFaYq6YJiHzXVmowO1KMCQ0wjldEtZXw2xd4qTN4wUaAHpew7S1E1wNKqeX64hZyp8W3pGiCbGYB7ETZdg34rLazU4LBE.Ug',
    'tb_visit_counter_direkt_de': 'eyJpdiI6IkNkUXlpcWR3VFJyTTI3eGY5NmJmN2c9PSIsInZhbHVlIjoiRzdqTE1CdVRYRkViMUFnNTBXRktBWnlHTitlSVcwaXR6eVNreXZUaTR0eWJ4a1F5U3FPdm8vcXFMODdvdlV2ayIsIm1hYyI6ImY0N2ZiZjYzZjhmNmJhYTExOGIzMDAxMGUxNmQ3YTBlNWE0MTcyODJmMTI1MjVjZTI5NTRjYTBiODA2NzIwNWYiLCJ0YWciOiIifQ%3D%3D',
    'kmtx_sync_pi': 'a64f3ee3-17da-4244-9b1e-0ad892a8d594',
    '_ga_DHWDNTWLEQ': 'GS1.1.1725937815.2.1.1725938025.59.0.65988160',
    'XSRF-TOKEN': 'eyJpdiI6IlphQmgwZVphazJ2M1NoVkFEdW1XR1E9PSIsInZhbHVlIjoiTFdOQksxeG9HTlQ4UXVKNTlaT1Q2Q1ZTUmMvaERFNy9DNnVBbkhrZWZpWlJiRXArU1RWWjY4Uzd5UkhPdDJTUHR2dGhST0hQZjN6TU4yYURSNG5FMHFHRWZmWitMdTRUbnQybnJYNDZiSjVUY1NGY1Awc2FsSVVJWUlOZlIwenQiLCJtYWMiOiJiNTQ1ZmIxOWQzNDQzOTZiNGNiNjgxYjllM2M1NDZmYjQ2YTM0NTBjMDJlYTcxYTAxMzk0NWUzN2E3MzU5MjRjIiwidGFnIjoiIn0%3D',
    'l': 'eyJpdiI6ImgwOFVTSDEzYTljQVh6MDYzVUZmMWc9PSIsInZhbHVlIjoiY0FDT0pZa25iZ283ZFREN0xZYnVCbjBuWllFM3pveVk3WGJGT01OdElnYlFXNlVBU2R2YkRvdjlJZFBwZ0VzL2NqdkttSFZkRHRNSnJ4RG84d2Z5M1Q2S0FPQ3ZRUlBrRmU4ekc1aVljRkFqMi9wR21LRkxIZGllUWpiYi9UV0EiLCJtYWMiOiJiZmMwODlmNmIwMGU3ODA2YjBiZTIwNDEzMWM2NGZmYzBlNTEyZGU5ZGJkNGM0NzU2NjJkZDgxNjRlYzU5Mzg0IiwidGFnIjoiIn0%3D',
    '_uetsid': 'e6fbd1c06f1b11ef871c91300f4033c2',
    '_uetvid': '26dcbdb06ce311ef8d2a756a0cf7b6c1',
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
part_number_ls = []
img_ls = []
href_ls = []

for pg in range(1, 5):
    params = {
        'keyword': 'Klimakompressor',
        'brand[]': '21',
        'pg': str(pg),
    }
    try:
        rsp = requests.get('https://www.autoteiledirekt.de/suche.html', params=params, cookies=cookies, headers=headers)
        tree = etree.HTML(rsp.text)
        product_card_wrappers = tree.xpath('//*[@class="product-card__wrapper"]')
        product_card_heads = tree.xpath('//*[@class="product-card__head"]')
        for card_w in product_card_wrappers:
            img = card_w.xpath('./div/div[2]/span/img')[0].get('src')
            img_ls.append(img)
        for card_h in product_card_heads:
            try:
                href = card_h.xpath('./div[1]/a')[0].get('href')
                part_number = card_h.xpath('./div[2]/div[1]/span/text()')[0]
            except:
                href = card_h.xpath('./div[1]/span')[0].get('data-link')
                part_number = card_h.xpath('./div[2]/div[1]/span/text()')[0]
            part_number_ls.append(part_number)
            href_ls.append(href)
        rsp.close()
    except:
        time.sleep(1)
        print(pg)
        continue

df = pd.DataFrame(columns=['Part_Number', 'img', 'href'])
df['Part_Number'] = part_number_ls
df['img'] = img_ls
df['href'] = href_ls
df.to_excel('./menu.xlsx', index=False)


