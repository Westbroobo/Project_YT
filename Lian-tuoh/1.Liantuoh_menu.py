# -*- coding: utf-8 -*- 
# @Time ： 2024/8/7 17:05
# @Auth ： Westbroobo
# @File ：1.Liantuoh_menu.py

from tool import UA
import requests
from lxml import etree
import pandas as pd
import time
headers = UA.get_User_Agent_Requests()
headers['referer'] = 'http://www.lian-tuoh.com.tw'
part_ls = []
url_ls = []
img_ls = []
model_ls = []
Parts_No_ls = []
Parts_link_ls = []
for page in range(1, 158):
    try:
        url = 'http://www.lian-tuoh.com.tw/products/list/235/page:{}.html'.format(page)
        rsp = requests.get(url=url, headers=headers)
        tree = etree.HTML(rsp.text)
        groups = tree.xpath('.//div[@class="item-group"]/div')
        for group in groups:
            part_number = group.xpath('./a/div/h3/text()')[0]
            href = group.xpath('./a')[0].get('href')
            detail_url = 'http://www.lian-tuoh.com.tw' + href
            src = group.xpath('./a/figure/img')[0].get('src')
            img = 'http://www.lian-tuoh.com.tw' + src
            brs = group.xpath('./a/div/p/text()')
            index_part_no = -1
            for br in brs:
                if 'Parts No' in br:
                    index_part_no = brs.index(br)
                    break
            if int(index_part_no) == 0 and len(brs) == 1:
                Parts_No = brs[index_part_no].replace('\n', '').replace('Parts No. :', '').replace(' ', '')
                Parts_link = ''
                model = ''
            elif int(index_part_no) == 0 and len(brs) == 2:
                Parts_No = brs[index_part_no].replace('\n', '').replace('Parts No. :', '').replace(' ', '')
                Parts_link = brs[1].replace('\n', '').replace('Partslink:', '')
                model = ''
            elif index_part_no == -1:
                Parts_No = ''
                Parts_link = ''
                model = ''.join(brs)
            elif int(index_part_no)+2 == len(brs):
                model = ''.join(brs[:-2])
                Parts_No = brs[-2].replace('\n', '').replace('Parts No. :', '').replace(' ', '')
                Parts_link = brs[-1].replace('\n', '').replace('Partslink:', '')
            else:
                model = ''.join(brs[:-1])
                Parts_No = brs[index_part_no].replace('\n', '').replace('Parts No. :', '').replace(' ', '')
                Parts_link = ''
            part_ls.append(part_number)
            url_ls.append(detail_url)
            img_ls.append(img)
            Parts_No_ls.append(Parts_No)
            Parts_link_ls.append(Parts_link)
            model_ls.append(model)
        rsp.close()
    except Exception as e:
        time.sleep(1)
        print(page)
        continue


df = pd.DataFrame(columns=['SKU',
                           'Parts_No',
                           'Parts_link',
                           'Model',
                           'product_url',
                           'img_url'])
df['SKU'] = part_ls
df['Parts_No'] = Parts_No_ls
df['Parts_link'] = Parts_link_ls
df['Model'] = model_ls
df['product_url'] = url_ls
df['img_url'] = img_ls
df.to_excel('./Liantuoh_menu.xlsx', index=False)




