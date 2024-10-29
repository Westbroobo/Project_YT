# -*- coding: utf-8 -*- 
# @Time ： 2024/6/29 14:17
# @Auth ： Westbroobo
# @File ：2.Rockauto_detail_proxy.py

import gevent
from gevent import monkey, pool
monkey.patch_all(thread=False)
import time
import requests
from lxml import etree
from tool import UA, Proxy
from fake_useragent import UserAgent
import re
import json
import pandas as pd
import xlsxwriter
start = time.perf_counter()
df_menu = pd.read_excel('./Rockauto_menu.xlsx', header=0, dtype=str).fillna('')

# 新建表格储存数据
# date_number = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
# type_code = url_menu.split(',')[-1]
# file_name = re.search('parts\/(.+){}'.format(type_code), url_menu).group(1).replace(',', '-').\
#                 replace('+', ' ').replace('/', ' ').replace('   ', '&') + date_number
# file_name = '【Rockauto】' + file_name[0].upper() + file_name[1:]
# print(file_name)
urls = df_menu['Url'].to_list()
wb = xlsxwriter.Workbook('./Rockauto_detail.xlsx')
ws = wb.add_worksheet('Sheet1')
ws.set_column('A:A', 15)
ws.set_column('B:B', 18)
ws.set_column('C:C', 25)
ws.set_column('D:D', 45)
ws.set_column('E:E', 18)
headings = ['Brand', 'Part_Number', 'Vehicle', 'Pic', 'OE', 'Note']
head_format = wb.add_format({
    'bold': 1,
    'fg_color': 'cyan',
    'align': 'center',
    'font_name': '等线',
    'size': 10,
    'valign': 'vcenter',
    'border': 1
})
cell_format = wb.add_format({
    'bold': 0,
    'align': 'center',
    'font_name': '等线',
    'size': 9,
    'valign': 'vcenter',
    'text_wrap': True,
    'border': 1
})
ws.write_row('A1', headings, head_format)
ws.freeze_panes(1, 0)
ws.set_row(0, 20)


def fetch_data(url, k):
    for test in range(200):
        try:
            rsp = requests.get(url=url, headers=UA.get_User_Agent_Requests(), proxies=Proxy.get_Proxy_Requests())
            status_code_1 = rsp.status_code
            tree_1 = etree.HTML(rsp.text)
            brand = tree_1.xpath('./descendant::span[@class="listing-final-manufacturer "]/text()')[0]
            part_number = tree_1.xpath('./descendant::div[@class="listing-text-row-moreinfo-truck"]/'
                                       'span[@title="Buyer\'s Guide"]/text()')[0]
            oes = tree_1.xpath('./descendant::span[@title="Replaces these Alternate/ OE Part Numbers"]/text()')
            oe = ';'.join(oes).replace(', ', ';')
            notes = tree_1.xpath('./descendant::div[@class="listing-text-row-moreinfo-truck"]'
                                 '/span[@class="span-link-underline-remover"]/text()')
            note = ';'.join(notes).replace(', ', ';')
            try:
                src = 'https://www.rockauto.com' + \
                      tree_1.xpath('./descendant::img[@class=" listing-inline-image"]/@src')[0]
            except IndexError:
                src = ''
            href = tree_1.xpath('./descendant::a[@class="ra-btn ra-btn-moreinfo"]/@href')[0]
            part_key = '"' + re.search(r'pk=(\d+)', href).group(1) + '"'
            part_type = '"' + url.split(',')[-1] + '"'
            wh_part_num = '"' + brand + ' ' + part_number + '"'
            opts = '{"0-0-0-1": {' + '''
                      "warehouse": "72901",
                      "whpartnum": {},
                      "optionlist": "0",
                      "paramcode": "0",
                      "notekey": "0",
                      "multiple": "1"
                      '''.format(wh_part_num) + '}}'
            listing_data_essential = '{' + '''
                  "groupindex": "0",
                  "carcode": 0,
                  "parttype": {},
                  "partkey": {},
                  "opts": {}
                  '''.format(part_type, part_key, opts) + '}'
            listing_data_supplemental = '{' + '''
                  "partnumber": {},
                  "catalogname": {},
                  "belongstolisting": "0",
                  "sortgroup": 0,
                  "sortgrouptext": "",
                  "paramdesc": "",
                  "showhide": {}
                '''.format('"' + part_number + '"', '"' + brand + '"', {}) + '}'
            payload = '{"partData": {' + '''
                "groupindex": "74",
                "listing_data_essential": {},
                "listing_data_supplemental": {},
                "OptKey": "0-0-0-1"
            '''.format(listing_data_essential, listing_data_supplemental) + '}}'
            payload = payload.replace('\n', '').replace('  ', '')
            data = {
                'func': 'getbuyersguide',
                'payload': payload,
                'api_json_request': '1',
                'sctchecked': '0',
                'scbeenloaded': 'false',
                'curCartGroupID': '',
            }
            headers = {
                'Accept': 'text/plain, */*; q=0.01',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': 'https://www.rockauto.com',
                'Referer': 'https://www.rockauto.com/en/parts/dayco,PB1019N,harmonic+balancer,5512',
                'User-Agent': str(UserAgent(path="E:/BaiduNetdiskDownload/ua.json").random),
                'X-Requested-With': 'XMLHttpRequest',
            }
            response = requests.post('https://www.rockauto.com/catalog/catalogapi.php', headers=headers,
                                     data=data, proxies=Proxy.get_Proxy_Requests())
            status_code_2 = response.status_code
            json_data = json.loads(response.text)
            body = json_data['buyersguidepieces']['body']
            tree_2 = etree.HTML(body)

            try:
                trs = tree_2.xpath('./descendant::div[@class="buyersguide-nested"]/div/table/tr')
                content = ''
                for tr in trs:
                    content += tr.xpath('./td[1]/text()')[0] + ' ' + tr.xpath('./td[2]/text()')[0] + ' ' + \
                               tr.xpath('./td[3]/text()')[0] + '\n'
                vehicle = content[:-1]
            except IndexError:
                vehicle = ''

            ws.set_row(k + 1, 20)
            ws.write(k + 1, 0, brand, cell_format)
            ws.write(k + 1, 1, part_number, cell_format)
            ws.write(k + 1, 2, vehicle, cell_format)
            ws.write(k + 1, 3, src, cell_format)
            ws.write(k + 1, 4, oe, cell_format)
            ws.write(k + 1, 5, note, cell_format)
            if status_code_1 == 200 and status_code_2 == 200:
                print('{}【尝试次数：{}】-success'.format(part_number, test+1))
                break
        except Exception as e:
            # print(f"Error processing URL {url}: {e}")
            time.sleep(0.3)
            continue


# jobs = [gevent.spawn(fetch_data, url, k) for k, url in enumerate(urls)]
# gevent.joinall(jobs)
pool = pool.Pool(15)
for k, url in enumerate(urls):
    pool.spawn(fetch_data, url, k)
pool.join()
wb.close()
end = time.perf_counter()
print(end-start)
