"""
Filename:eBay_pic.py
Author: Westbroobo
Date: 2024/9/20
"""

from gevent import monkey, pool
monkey.patch_all(thread=False)
import pandas as pd
import requests
from tool import UA, Proxy
from lxml import etree
import time

cookies = {
    '__uzma': '8efa63b2-5b59-482c-b4b5-9487d7862a23',
    '__uzmb': '1723596676',
    '__uzme': '5209',
    'cid': 'rBiPWaMlw0K7sOkA%23469222263',
    '__ssds': '2',
    '__uzmaj2': '9ed18687-3fb2-466d-a0db-180c7e6eca5e',
    '__uzmbj2': '1723596687',
    'utag_main__sn': '1',
    '_gcl_au': '1.1.1193484553.1723596701',
    '_fbp': 'fb.1.1723596701882.643149592300209675',
    '__uzmlj2': 'bJVcz5GtV5oJp3toDqqWMSPwdcPlcLIHD8QlMoEa3bg=',
    '__gsas': 'ID=151fc2379bf4647b:T=1723597742:RT=1723597742:S=ALNI_MbFXDC6BZ7uSb0mEzNmu72Sp4WLXg',
    '__gads': 'ID=8cd97c1e52c80d01:T=1725001318:RT=1726035902:S=ALNI_MYpF9ZolBeqKKzNiWci2T07KAGvIQ',
    '__gpi': 'UID=00000ee32c1e45ae:T=1725001318:RT=1726035902:S=ALNI_MYM8h0OXm4Jt16LhrRZ5jjV2p3NRg',
    '__eoi': 'ID=3941d8cfede7ca0b:T=1725001318:RT=1726035902:S=AA-AfjZtdd1vn3IPZZl_ynP5K3Pw',
    'AMP_MKTG_f93443b04c': 'JTdCJTdE',
    'shs': 'BAQAAAZHt1EgyAAaAAVUAD2idMzkyMjE4NjUxOTQxMDAzLDLS8qQ/kcLmTbE736VDjZzX51QNXw**',
    '__ssuzjsr2': 'a9be0cd8e',
    '__uzmcj2': '81837343391903',
    '__uzmdj2': '1726730539',
    '__uzmfj2': '7f60005a929bdc-3b5b-45e2-ab0b-761e825af44f17235966878213133851772-b9275320da47c0bc3430',
    'ak_bmsc': '9C0A2D6FBF0C9B0EB477B21D979EB5D1~000000000000000000000000000000~YAAQ7/fVF76kKcKRAQAA5ecYDRkezHZgSzSZ0vDEcCFYqT9Rh6Il+Mv3//reT7bcK6l/xVHsjKqDSw5HFqhCASPTIiI6+QEYIk2st9TcZiRn2c0Zuh7F4tWwZyiO3srGAIsyoFumMCUwjLbT/6LggfgBgfQ0mo1KslxMWpnw0hMjGb114GLWOIEQ4xzrl12az3rLQ1mtu8Jdy6v7iy6vG45x2s/0/oVQNRyUziG5VBvkGyPLwGDwVPprl49u17dTl3SHGj6EXY00l7TLhgfFHEl4VQnS/7obc1lwWJoDuDmVSb06l1Fg1OcapOZTObWLEn3QO1ip0tzV//bmUIVniIQih/gtN3b/mH+TqUFBh1xCZlnQqxSXqgjOnp307s+D3zIRAAhEKoy+',
    's': 'CgADuABhm7iSvMAZodHRwczovL3d3dy5lYmF5LmNvbS8HAPgAIGbuJKw0ZTVlMTM1ZTE5MTBhYWIzNmRjNTZmZThmZmZlM2M1N7hQNtE*',
    'ebay': '%5Ejs%3D1%5Esbf%3D%23000000%5E',
    '__uzmc': '94291682630946',
    '__uzmd': '1726796598',
    '__uzmf': '7f60005a929bdc-3b5b-45e2-ab0b-761e825af44f17235966765553199922215-09d024e11d282eee6826',
    'bm_sv': '74B46900F98F69E9F9653B54C4CBCAE7~YAAQ7/fVFzWpKcKRAQAAciMZDRnr+Xya2b4ZJ08EB8szLCRUbYjKuUKWiA8G3Au8Pe9gwCmYHAr6n5+kkCMzDRfHEUlVVE1QGpaTKYFpaa11rME5f0Pi9DpW0dNfcLhMZFJAAnQRJv3W3tSxO+8Q/Yoz066ueAkZBDdTK+fIWolQjkFUbCWuMqnrDpo5qfp3FvWMI8BIkOf4JrZ6mvbHICdF9LTqqpwm/uRXCRasHLvrCUs3wuD1S3lrlJqrZg==~1',
    'ns1': 'BAQAAAZBR14g6AAaAAKUADWjOBvMyMzYyODgzMzM1LzA78hUAHhojbGqVEFbh9pwHva1jvio*',
    'nonsession': 'BAQAAAZBR14g6AAaAAAQAC2idMzl5YW5nLTEwMTQ5NAAQAAtozgbzeWFuZy0xMDE0OTQAMwAOaM4G8zkxNzEwLTU0MTcsVVNBAEAAC2jOBvN5YW5nLTEwMTQ5NACcADhozgbzblkrc0haMlByQm1kajZ3Vm5ZK3NFWjJQckEyZGo2TUhsb0NwQUpPQm9nbWRqNng5blkrc2VRPT0AnQAIaM4G8zAwMDAwMDAxAMoAIGqvOnM0ZTVlMTM1ZTE5MTBhYWIzNmRjNTZmZThmZmZlM2M1NwDLAAJm7Np7MTEBZAAHaq86cyMwMDAwOGH+6KqIJqqZa5vgkkNtfszs1oRHLg**',
    'totp': '1726796705846.MIov6pE7v9aHVOrhgXviafqK9liMBoP3KdFpTwpk4hVnFEGVXVJ94X87FMAysPYywoDsqUmFR6/e9zYUxup/RA==.XMYN6I1dAkCuUSomMgov3RgCwK1fr6tOw6rXi2XYY8s',
    'dp1': 'bu1p/eWFuZy0xMDE0OTQ*6aaf3a73^kms/in6aaf3a73^pbf/#2000000e0002000000080800000046aaf3aaf^u1f/yangteng6aaf3a73^expt/000172359675500567ac9993^bl/USen-US6aaf3a73^',
    '__deba': '1Fadi3CXluLp-p12DChfMUqNu6HF_YPJqqLrsbpRXthmKpONFCylhahIGu_CkML3SCYfAZzbFpQ91kRcKVsu5La7ci_qb88uyoNVlijHlw3W6v-QdEo83d5arzxSi_HlbkZP38YN2ObMqXv073kLfw==',
    'AMP_f93443b04c': 'JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJiZmFmYTk5MC1hOTNlLTRiOTEtYmUzZC01MzVhYTE2NTQ5ZWUlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzI2Nzk2NjAxMjc4JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTcyNjc5NjcyNTU3MSUyQyUyMmxhc3RFdmVudElkJTIyJTNBNTI4NSUyQyUyMnBhZ2VDb3VudGVyJTIyJTNBNiU3RA==',
}
df_menu = pd.read_excel('./menu.xlsx', header=0)
list_item = df_menu['Item'].tolist()

ls_item = []
ls_img = []
def fetch_data(item):
    num = 10
    for test in range(num):
        try:
            url = 'https://www.ebay.com/itm/' + str(item)
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control': 'max-age=0',
                'priority': 'u=0, i',
                'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                'sec-ch-ua-full-version': '"129.0.6668.58"',
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
            rsp = requests.get(url=url, cookies=cookies, headers=headers, proxies=Proxy.get_Proxy_Requests())
            status_code = rsp.status_code
            tree = etree.HTML(rsp.text)
            img = tree.xpath('//*[@class="ux-image-carousel-item image-treatment active  image"]/img')[0].get('data-zoom-src')
            while not img:
                img = tree.xpath('//*[@class="ux-image-carousel-item image-treatment active  image"]/img')[0].get('src')
            ls_item.append(item)
            ls_img.append(img)
            if status_code == 200:
                print('{}【尝试次数：{}】-success，进度：{}/{}'.
                      format(item, test + 1, len(ls_item), len(list_item)))
                rsp.close()
                break
        except Exception as e:
            if test == num - 1:
                print('{}【尝试次数：{}】-error'.format(item, test + 1))
            time.sleep(1)
            continue

pool = pool.Pool(15)
for item in list_item:
    pool.spawn(fetch_data, item)
pool.join()


df = pd.DataFrame(columns=['Item', 'Img'])
df['Item'] = ls_item
df['Img'] = ls_img
df.to_excel('./eBay_pic.xlsx', index=False)


