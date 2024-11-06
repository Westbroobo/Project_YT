"""
Filename:2.Detail.py
Author: Westbroobo
Date: 2024/11/5
"""
from gevent import monkey, pool
monkey.patch_all(thread=False)
import time
from curl_cffi import requests
from tool import UA, Proxy
from lxml import etree
import pandas as pd
import json

df_menu = pd.read_excel('./menu.xlsx')
Url = df_menu['Url'].to_list()
url_ls = []
vehicle_ls = []
product_details_ls = []
features_ls = []
json_ls = []

def fetch_data(url):
    num = 20
    for test in range(num):
        try:
            headers = {
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': UA.get_UA(),
                'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
                'sec-ch-ua-arch': '"x86"',
                'sec-ch-ua-bitness': '"64"',
                'sec-ch-ua-full-version': '"130.0.6723.71"',
                'sec-ch-ua-full-version-list': '"Chromium";v="130.0.6723.71", "Google Chrome";v="130.0.6723.71", "Not?A_Brand";v="99.0.0.0"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"10.0.0"',
            }
            rsp = requests.get(url=url, impersonate="chrome101", headers=headers, proxies=Proxy.get_Proxy_Requests())
            status_code = rsp.status_code
            tree = etree.HTML(rsp.text)
            try:
                trs = tree.xpath('//*[@id="applications"]/div/div/div[1]/table/tr')
                content = []
                make = ''
                for tr in trs[1:]:
                    td_ = len(tr.xpath('./td'))
                    if td_ == 3:
                        make = tr.xpath('./td[1]/text()')[0]
                        model = tr.xpath('./td[2]/text()')[0]
                        year = tr.xpath('./td[3]/text()')[0]
                    else:
                        model = tr.xpath('./td[1]/text()')[0]
                        year = tr.xpath('./td[2]/text()')[0]
                    if ', ' in year:
                        list_year = year.split(', ')
                        make_model_year = make + ' ' + model + ' ' + list_year[0]
                        content.append(make_model_year)
                        make_model_year = make + ' ' + model + ' ' + list_year[1]
                        content.append(make_model_year)
                    else:
                        make_model_year = make + ' ' + model + ' ' + year
                        content.append(make_model_year)
                vehicle = '\n'.join(content).replace('  ', ' ')
            except:
                vehicle = ''
            try:
                product_details = tree.xpath('//*[@id="product-details"]/div[1]/div[1]/div[1]/p/text()')[0]
            except:
                product_details = ''
            try:
                lis = tree.xpath('//*[@id="product-details"]/div[1]/div[1]/div[1]/ul/li')
                feature_ls = []
                for li in lis:
                    feature = li.xpath('./text()')[0]
                    feature_ls.append(feature)
                features = '\n'.join(feature_ls)
            except:
                features = ''
            try:
                prod_offer_items = tree.xpath('//*[@class="prod-offer-item"]')
                list_ = []
                for p_o_item in prod_offer_items:
                    dict_ = {}
                    key = p_o_item.xpath('./div[1]/text()')[0]
                    try:
                        value = p_o_item.xpath('./div[2]/a/span/text()')[0]
                    except:
                        value = p_o_item.xpath('./div[2]/text()')[0]
                    dict_[key] = value
                    list_.append(dict_)
                formatted_data = {str(index): item for index, item in enumerate(list_)}
                json_data = json.dumps(formatted_data)
            except:
                json_data = ''
            url_ls.append(url)
            vehicle_ls.append(vehicle)
            product_details_ls.append(product_details)
            features_ls.append(features)
            json_ls.append(json_data)
            rsp.close()
            if status_code == 200:
                print('{}【尝试次数：{}】-success'.format(url, test + 1))
                break
        except Exception as e:
            # print(e)
            time.sleep(0.3)
            if test == num - 1:
                print('{}【尝试次数：{}】-error'.format(url, test))
                continue

pool = pool.Pool(10)
for url in Url:
    pool.spawn(fetch_data, url)
pool.join()
df = pd.DataFrame(columns=['Url', 'Vehicle', 'Product Details', 'Features', 'Json_Data'])
df['Url'] = url_ls
df['Vehicle'] = vehicle_ls
df['Product Details'] = product_details_ls
df['Features'] = features_ls
df['Json_Data'] = json_ls
df.to_excel('./Detail.xlsx', index=False)

