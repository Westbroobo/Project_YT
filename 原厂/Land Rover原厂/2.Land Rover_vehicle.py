# -*- coding: utf-8 -*- 
# @Time ： 2024/8/15 9:23
# @Auth ： Westbroobo
# @File ：2.Land Rover_vehicle.py

import requests
from tool import UA
from lxml import etree
import pandas as pd
import time


def list_cleand(lst):
    new_list = []
    lst.sort()
    for x, y in zip(lst, lst[1:]):
        if int(y) - int(x) > 1:
            new_list.append(lst[:lst.index(y)])
            lst = lst[lst.index(y):]
    new_list.append(lst)
    return new_list


df_menu = pd.read_excel('./Land Rover_menu.xlsx', header=0)
urls = df_menu['Url'].to_list()
headers = UA.get_User_Agent_Requests()
headers['referer'] = 'https://landrover.oempartsonline.com/'
url_ls = []
image_ls = []
vehicle_ls = []
vehicle_fitment_ls = []
for url in urls:
    try:
        rsp = requests.get(url=url, headers=headers)
        tree = etree.HTML(rsp.text)
        try:
            src = tree.xpath('.//img[@class="product-main-image centered"]')[0].get('src')
            image = 'http:' + src
        except:
            image = ''
        try:
            make_model_year_dict = {}
            make_model_year_ls = []
            table = tree.xpath('.//table[@class="fitment-table"]/tbody/tr')
            list_vehicle_fitment = []
            for tr in table:
                year = tr.xpath('./td[1]/text()')[0].strip()
                make = tr.xpath('./td[2]/text()')[0].strip()
                model = tr.xpath('./td[3]/text()')[0].strip()
                body_trim = tr.xpath('./td[4]/text()')[0].strip()
                engine = tr.xpath('./td[5]/text()')[0].strip()
                vehicle_fitment = year + ' ' + make + ' ' + model + ' ' + body_trim + ' ' + engine
                list_vehicle_fitment.append(vehicle_fitment)
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
            vehicle_fitments = '\n'.join(list_vehicle_fitment)
        except Exception as e:
            print(e)
            make_model_year = ''
            vehicle_fitments = ''
        url_ls.append(url)
        image_ls.append(image)
        vehicle_ls.append(make_model_year)
        vehicle_fitment_ls.append(vehicle_fitments)
    except:
        print(url)
        time.sleep(1)
        continue


df = pd.DataFrame(columns=['Url', 'Iamge', 'Vehicle_1', 'Vehicle_2'])
df['Url'] = url_ls
df['Iamge'] = image_ls
df['Vehicle_1'] = vehicle_ls
df['Vehicle_2'] = vehicle_fitment_ls
df.to_excel('./Land Rover_vehicle.xlsx', index=False)

