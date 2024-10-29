"""
Filename:3-1.fetch_vehicle1.py
Author: Westbroobo
Date: 2024/9/6
"""

from gevent import monkey, pool
monkey.patch_all(thread=False)
import requests
from tool import UA, Proxy
from lxml import etree
import pandas as pd
import time

ls_search = []
ls_category = []
ls_brand = []
ls_part = []
ls_oe = []
ls_note = []
ls_img = []
ls_url = []

def fetch_data(p):
    num = 100
    for test in range(num):
        try:
            partnum_search = str(p)
            url = 'https://www.rockauto.com/en/partsearch/?partnum={}'.format(partnum_search)
            rsp = requests.get(url=url, headers=UA.get_User_Agent_Requests(), proxies=Proxy.get_Proxy_Requests())
            status_code = rsp.status_code
            tree = etree.HTML(rsp.text)
            nnormal = tree.xpath('./descendant::td[@class="nlabel"]/a/text()')[0]
            listing_container = tree.xpath('//div[@class="listing-container-border"]/div/table/tbody')
            if len(listing_container) == 0:
                ls_search.append(partnum_search)
                ls_category.append('-')
                ls_brand.append('-')
                ls_part.append('-')
                ls_oe.append('-')
                ls_note.append('-')
                ls_img.append('-')
                ls_url.append(url)
            else:
                for tbody in listing_container[1:]:
                    brand = tbody.xpath('./descendant::span[@class="listing-final-manufacturer "]/text()')[0]
                    part_number = tbody.xpath('./descendant::div[@class="listing-text-row-moreinfo-truck"]/span[@title="Buyer\'s Guide"]/text()')[0]
                    category = tbody.xpath('./descendant::div[@class="listing-text-row"]/span/span/text()')[0].replace('Category:', '').strip()
                    oes = tbody.xpath('./descendant::span[@title="Replaces these Alternate/ OE Part Numbers"]/text()')
                    oe = ';'.join(oes).replace(', ', ';')
                    notes = tbody.xpath('./descendant::div[@class="listing-text-row-moreinfo-truck"]'
                                         '/span[@class="span-link-underline-remover"]/text()')
                    note = ';'.join(notes).replace(', ', ';')
                    try:
                        src = 'https://www.rockauto.com' + \
                              tbody.xpath('./descendant::img[@class=" listing-inline-image"]/@src')[0]
                    except IndexError:
                        src = ''
                    ls_search.append(partnum_search)
                    ls_category.append(category)
                    ls_brand.append(brand)
                    ls_part.append(part_number)
                    ls_oe.append(oe)
                    ls_note.append(note)
                    ls_img.append(src)
                    ls_url.append(url)
            if status_code == 200:
                rsp.close()
                ls_partnum_search = list(set(ls_search))
                print('{}【尝试次数：{}】-success，进度：{}/{}'.
                      format(p, test + 1, len(ls_partnum_search), len(partnums)))
                break
        except Exception as e:
            time.sleep(0.3)
            if test == num-1:
                print('{}【尝试次数：{}】-error'.format(p, test))
            continue

df = pd.read_excel('./search_number.xlsx')
partnums = df['Search Number'].tolist()
pool = pool.Pool(15)
for p in partnums:
    pool.spawn(fetch_data, p)
pool.join()

df_ = pd.DataFrame(columns=['Search_Number', 'Category', 'Brand', 'Part_Number', 'OE', 'Note', 'Img', 'Url'])
df_['Search_Number'] = ls_search
df_['Category'] = ls_category
df_['Brand'] = ls_brand
df_['Part_Number'] = ls_part
df_['OE'] = ls_oe
df_['Note'] = ls_note
df_['Img'] = ls_img
df_['Url'] = ls_url

df_.to_excel('./search_result.xlsx', index=False)


