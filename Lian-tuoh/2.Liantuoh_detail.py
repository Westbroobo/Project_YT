# -*- coding: utf-8 -*- 
# @Time ： 2024/8/8 8:47
# @Auth ： Westbroobo
# @File ：2.Liantuoh_detail.py

from tool import UA
import requests
from lxml import etree
import pandas as pd
import time
df = pd.DataFrame(columns=['Url', 'Vehicle'])
headers = UA.get_User_Agent_Requests()
headers['referer'] = 'http://www.lian-tuoh.com.tw'
df_menu = pd.read_excel('./Liantuoh_menu.xlsx', header=0)
urls = df_menu['product_url'].to_list()
skus = df_menu['SKU'].to_list()


def list_cleand(lst):
    new_list = []
    lst.sort()
    for x, y in zip(lst, lst[1:]):
        if y - x > 1:
            new_list.append(lst[:lst.index(y)])
            lst = lst[lst.index(y):]
    new_list.append(lst)
    return new_list


for url in urls:
    try:
        rsp = requests.get(url=url, headers=headers)
        tree = etree.HTML(rsp.text)
        trs_vehicle = tree.xpath('.//div[@class="php-other-tables"]/div[1]/table[1]/tbody/tr')
        trs_description = tree.xpath('.//div[@class="sec-part editor"]/div[1]/table[1]/tbody/tr')
        make_model_year_dict = {}
        make_model_year_ls = []
        try:
            for tr_v in trs_vehicle:
                make = tr_v.xpath('./td[1]/text()')[0]
                model = tr_v.xpath('./td[2]/text()')[0]
                year = int(tr_v.xpath('./td[3]/text()')[0])
                if make not in make_model_year_dict:
                    make_model_year_dict[make] = {model: [year]}
                else:
                    if model not in make_model_year_dict[make]:
                        make_model_year_dict[make][model] = [year]
                    else:
                        make_model_year_dict[make][model].append(year)
                make_model_year_dict[make][model] = list(set(make_model_year_dict[make][model]))
            for make in make_model_year_dict:
                for model in make_model_year_dict[make]:
                    if len(make_model_year_dict[make][model]) == 1:
                        content = make + ' ' + model + ' ' + str(make_model_year_dict[make][model][0])
                        make_model_year_ls.append(content)
                    elif int(max(make_model_year_dict[make][model])) - int(min(make_model_year_dict[make][model])) == len(
                            make_model_year_dict[make][model]) - 1:
                        content = make + ' ' + model + ' ' + str(min(make_model_year_dict[make][model])) \
                                  + '-' + str(max(make_model_year_dict[make][model]))
                        make_model_year_ls.append(content)
                    else:
                        new_list = list_cleand(make_model_year_dict[make][model])
                        for n in new_list:
                            if len(n) == 1:
                                content = make + ' ' + model + ' ' + str(n[0])
                                make_model_year_ls.append(content)
                            else:
                                content = make + ' ' + model + ' ' + str(min(n)) + '-' + str(max(n))
                                make_model_year_ls.append(content)
            make_model_year_ls = list(set(make_model_year_ls))
            make_model_year_ls.sort()
            make_model_year = '\n'.join(make_model_year_ls)
        except:
            make_model_year = ''
        df_transit = pd.DataFrame([{'Url': url, 'Vehicle': make_model_year}])
        for tr_d in trs_description:
            title = tr_d.xpath('./td[1]/text()')[0]
            parameter = tr_d.xpath('./td[2]/text()')[0]
            df_transit[title] = parameter
        df = pd.concat([df, df_transit], ignore_index=True).fillna('')
    except Exception as e:
        print(url, e)
        time.sleep(1)
        continue

df.to_excel('./Liantuoh_detail.xlsx', index=False)


