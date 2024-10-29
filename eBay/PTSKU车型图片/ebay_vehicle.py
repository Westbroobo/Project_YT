"""
Filename:ebay_vehicle.py
Author: Westbroobo
Date: 2024/9/29
"""

from gevent import monkey, pool
monkey.patch_all(thread=False)
import requests
from tool import UA, Proxy
import time
import pandas as pd
from openpyxl import Workbook, load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

df = pd.DataFrame(columns=['No.', 'Item', 'Vehicle', 'Engine', 'Vehicle_Engine'])
wb = Workbook()
ws = wb.active
ws.title = "Data"
header_font = Font(name='等线', size=10, bold=True)
font = Font(name='等线', size=9)
alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
border = Border(left=Side(border_style='thin'),
                right=Side(border_style='thin'),
                top=Side(border_style='thin'),
                bottom=Side(border_style='thin'))
fill = PatternFill(start_color="95B3D7", end_color="95B3D7", fill_type="solid")
for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), 1):
    ws.append(row)
ws.row_dimensions[1].height = 20
ws.column_dimensions['A'].width = 8
ws.column_dimensions['B'].width = 12
ws.column_dimensions['C'].width = 30
ws.column_dimensions['D'].width = 25
ws.column_dimensions['E'].width = 65
ws.freeze_panes = "A2"
for cell in ws[1]:
    cell.font = header_font
    cell.fill = fill
    cell.alignment = alignment
    cell.border = border
wb.save('eBay_vehicle.xlsx')

df_menu = pd.read_excel('./menu.xlsx',header=0)
items = df_menu['Item'].tolist()

def list_cleand(lst):
    new_list = []
    lst.sort()
    for x, y in zip(lst, lst[1:]):
        if int(y) - int(x) > 1:
            new_list.append(lst[:lst.index(y)])
            lst = lst[lst.index(y):]
    new_list.append(lst)
    return new_list

def fetch_vehicle(rows, list_table_title, make_model_year_dict, year_make_model_engine_ls, engine_ls):
    try:
        index_year = list_table_title.index('Year')
        index_make = list_table_title.index('Make')
        index_model = list_table_title.index('Model')
        index_engine = list_table_title.index('Engine')
        for row in rows:
            cells = row["cells"]
            year = int(cells[index_year]["textSpans"][0]["text"])
            make = cells[index_make]["textSpans"][0]["text"]
            model = cells[index_model]["textSpans"][0]["text"]
            engine = cells[index_engine]["textSpans"][0]["text"]
            year_make_model_engine = str(year) + ' ' + make + ' ' + model + ' ' + engine
            if year_make_model_engine not in year_make_model_engine_ls:
                year_make_model_engine_ls.append(year_make_model_engine)
            if 'Trim' in list_table_title and 'L' in engine:
                engine_ls.append(engine.split(' ')[0])
            if 'Variant' in list_table_title and 'cc' in engine:
                engine_ls.append(engine.split(' ')[0])
            if make not in make_model_year_dict:
                make_model_year_dict[make] = {model: [year]}
            else:
                if model not in make_model_year_dict[make]:
                    make_model_year_dict[make][model] = [year]
                else:
                    make_model_year_dict[make][model].append(year)
            make_model_year_dict[make][model] = list(set(make_model_year_dict[make][model]))
        return make_model_year_dict, year_make_model_engine_ls, engine_ls
    except:
        index_year = list_table_title.index('Baujahr')
        index_make = list_table_title.index('Marke')
        index_model = list_table_title.index('Modell')
        index_engine = list_table_title.index('Typ')
        for row in rows:
            cells = row["cells"]
            year = cells[index_year]["textSpans"][0]["text"]
            make = cells[index_make]["textSpans"][0]["text"]
            model = cells[index_model]["textSpans"][0]["text"]
            engine = cells[index_engine]["textSpans"][0]["text"]
            year_make_model_engine = make + ' ' + model + ' ' + year + ' ' + engine
            if year_make_model_engine not in year_make_model_engine_ls:
                year_make_model_engine_ls.append(year_make_model_engine)
            engine_ls.append(engine)
            year_ = year.split('-')
            year_1 = year_[0][:4]
            year_2 = year_[-1][:4]
            year__ = [y for y in range(int(year_1), int(year_2)+1)]
            if make not in make_model_year_dict:
                make_model_year_dict[make] = {model: year__}
            else:
                if model not in make_model_year_dict[make]:
                    make_model_year_dict[make][model] = year__
                else:
                    for y_ in year__:
                        make_model_year_dict[make][model].append(y_)
            make_model_year_dict[make][model] = list(set(make_model_year_dict[make][model]))
        return make_model_year_dict, year_make_model_engine_ls, engine_ls

def dict_to_str(make_model_year_dict):
    make_model_year_ls = []
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
    return make_model_year

cookies = {
    '__uzma': '8efa63b2-5b59-482c-b4b5-9487d7862a23',
    '__uzmb': '1723596676',
    '__uzme': '5209',
    'AMP_MKTG_f93443b04c': 'JTdCJTdE',
    'cid': 'rBiPWaMlw0K7sOkA%23469222263',
    '__ssds': '2',
    '__uzmaj2': '9ed18687-3fb2-466d-a0db-180c7e6eca5e',
    '__uzmbj2': '1723596687',
    'utag_main__sn': '1',
    '_gcl_au': '1.1.1193484553.1723596701',
    '_fbp': 'fb.1.1723596701882.643149592300209675',
    '__uzmlj2': 'bJVcz5GtV5oJp3toDqqWMSPwdcPlcLIHD8QlMoEa3bg=',
    '__gsas': 'ID=151fc2379bf4647b:T=1723597742:RT=1723597742:S=ALNI_MbFXDC6BZ7uSb0mEzNmu72Sp4WLXg',
    'shs': 'BAQAAAZGG1Rg0AAaAAVUAD2idMzkyMjE4NjUxOTQxMDAzLDKN9yHc8y2CBeYlJzVICPkpT7TxnQ**',
    '__ssuzjsr2': 'a9be2cd8e',
    '__uzmcj2': '86533135768362',
    '__uzmdj2': '1725005787',
    '__uzmfj2': '7f60005a929bdc-3b5b-45e2-ab0b-761e825af44f17235966878211409099289-a843813f13acece91354',
    '__gads': 'ID=8cd97c1e52c80d01:T=1725001318:RT=1725005895:S=ALNI_MYpF9ZolBeqKKzNiWci2T07KAGvIQ',
    '__gpi': 'UID=00000ee32c1e45ae:T=1725001318:RT=1725005895:S=ALNI_MYM8h0OXm4Jt16LhrRZ5jjV2p3NRg',
    '__eoi': 'ID=3941d8cfede7ca0b:T=1725001318:RT=1725005895:S=AA-AfjZtdd1vn3IPZZl_ynP5K3Pw',
    's': 'CgADuABhm1n9GMAZodHRwczovL3d3dy5lYmF5LmNvbS8HAPgAIGbWXBw0ZTVlMTM1ZTE5MTBhYWIzNmRjNTZmZThmZmZlM2M1N9nBn2M*',
    'ak_bmsc': '74A8D75BFAC6739116175352586A0F8C~000000000000000000000000000000~YAAQBopFyz2Azo6RAQAAQTRRsRgSn/py04k2NVoBWErusHb+mOIjH1FEr11+HhYlr0vXeg5rB2jOXmFEY1vFrhfEMp6Fl4GUNDO6yiY4xBeRendpJWEm/BoxCpz4QXEaa1NYzlB6Pmd7qfZTmIeVGjX8its6aPesgkwiOBR18kr3bLkHsNDiy2jhrLuE0NiwzQSNdIms8h6brsbvRu0gZuyaKpzpXHdW0fSJaOCNo/AV7RJq+luR30ddkXsff4M6NVXQv+a7L4X2C/9ES8Qc/IL7hkGa45qNQnGYsvRwjftmjosh/ic8Sz5hD5gwtTIYpzoUBUhNaejz2F2bN/FPAqLyZpsiUFVTto5YzZ3KMKNRDdh3D2/Hwkc8ONhjymcvZn/esabwyrs=',
    'AMP_f93443b04c': 'JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJiZmFmYTk5MC1hOTNlLTRiOTEtYmUzZC01MzVhYTE2NTQ5ZWUlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzI1MjU2MzcyNTM1JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTcyNTI1ODUzOTQ1MSUyQyUyMmxhc3RFdmVudElkJTIyJTNBMTUyOCUyQyUyMnBhZ2VDb3VudGVyJTIyJTNBNDMlN0Q=',
    '__deba': 'BSMonH9oZbLeqKowEqQYzzh14CYEYhn-nbgo0vRe3XmlwV1WiunkOzf3T6k7mzH6I2i1hbzWKfbBPKjzqLTdRLa7ci_qb88uyoNVlijHlw3W6v-QdEo83d5arzxSi_HlbkZP38YN2ObMqXv073kLfw==',
    '__uzmc': '64113247630187',
    '__uzmd': '1725258543',
    '__uzmf': '7f60005a929bdc-3b5b-45e2-ab0b-761e825af44f17235966765551661866717-346fb62dee35856e2476',
    'ns1': 'BAQAAAZBR14g6AAaAAKUADWi2kM0yMzYyODgzMzM1LzA7Z484hScH+8tBCCzoU9NF1kSnYLQ*',
    'dp1': 'bu1p/eWFuZy0xMDE0OTQ*6a97c44d^kms/in6a97c44d^pbf/%232000000e00020000000808000000468b690cd^u1f/yangteng6a97c44d^expt/000172359675500567ac9993^bl/USen-US6a97c44d^',
    'nonsession': 'BAQAAAZBR14g6AAaAAAQAC2idMzl5YW5nLTEwMTQ5NAAQAAtotpDNeWFuZy0xMDE0OTQAMwAOaLaQzTkxNzEwLTU0MTcsVVNBAEAAC2i2kM15YW5nLTEwMTQ5NACcADhotpDNblkrc0haMlByQm1kajZ3Vm5ZK3NFWjJQckEyZGo2TUhsb0NwQUpPQm9nbWRqNng5blkrc2VRPT0AnQAIaLaQzTAwMDAwMDAxAMoAIGqXxE00ZTVlMTM1ZTE5MTBhYWIzNmRjNTZmZThmZmZlM2M1NwDLAAJm1WRVMjYBZAAHapfETSMwMDAwOGGkUKsMI9fzc4viZFyV1w3KL8+/Kg**',
    'bm_sv': '46926929DBE7BF475345FE528C4CF74B~YAAQ1uNH0kkHxZCRAQAA0XZ0sRgcko6RBdXR5QeqLx1VobTJEu9vkWbDRzkqqJ7oCqfRRPmxsB8ciTqr3PCmXl1UIXy4BJgXGQbzwyj5chlJ2DZ6sAsIFbVJUKoILXEJMrCQRfxbHM983X9ogGNGPoD8sHUNO95Lj7Sz8z5GdQtgdl/xgdcN8v9JClQa/j/l5KXyXdsMvwdIg/1gEsWyWEoMDkgfvfLrHIzOFbJjhA5dnMlINhKtDVLFsgGcl1I=~1',
    'ebay': '%5Ejs%3D1%5Esbf%3D%23000000%5Epsi%3DAbCjZL8w*%5E',
    'ds2': 'sotr/bGvQkzzzzzzz^',
    'totp': '1725259089800.qodO7Kr4ur60/LVF67WxAQlf2fhLhSQS2SGVgL/PS2fSmtPw86Vgc/cbicjddKxW8RZE144+uUMPCyoHDMJvrA==.XMYN6I1dAkCuUSomMgov3RgCwK1fr6tOw6rXi2XYY8s',
}

def fetch_data(url, item):
    list_table_title = []
    make_model_year_dict = {}
    year_make_model_engine_ls = []
    engine_ls = []
    headers = {
        'accept': 'application/json',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'content-type': 'application/json',
        'origin': 'https://www.ebay.com',
        'priority': 'u=1, i',
        'referer': url,
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-full-version': '"128.0.6613.113"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': UA.get_UA(),
        'x-ebay-answers-request': 'pageci=8150e95c-7213-4f7a-98bb-585598255d75,parentrq=b16c28a01910ab7e0f393b0dffebf16b',
        'x-ebay-c-correlation-session': 'operationId=4429486',
        'x-ebay-c-tracking-config': 'viewTrackingEnabled=true,perfTrackingEnabled=true,navTrackingEnabled=true,navsrcTrackingEnabled=true,swipeTrackingEnabled=false,showDialogTrackingEnabled=true',
    }
    json_data = {
            'scopedContext': {
                'catalogDetails': {
                    'itemId': str(item),
                    'categoryId': '33602',
                    'marketplaceId': 'EBAY-US',
                },
            },
        }
    session = requests.session()
    for i in range(0, 10000, 20):
        num = 100
        e_ = ''
        for test in range(num):
            params = {
                'module_groups': 'PART_FINDER',
                'referrer': 'VIEWITEM',
                'offset': str(i),
                'module': 'COMPATIBILITY_TABLE',
            }
            try:
                rsp = session.post('https://www.ebay.com/g/api/finders', params=params, cookies=cookies,
                                         headers=headers, json=json_data, proxies=Proxy.get_Proxy_Requests())
                status_code = rsp.status_code
                data = rsp.json()
                if i == 0:
                    titles = data["modules"]["COMPATIBILITY_TABLE"]["paginatedTable"]["header"]["cells"]
                    for title in titles:
                        list_table_title.append(title["textSpans"][0]["text"])
                rows = data["modules"]["COMPATIBILITY_TABLE"]["paginatedTable"]["rows"]
                if status_code == 200:
                    break
            except Exception as e:
                if type(e) == requests.exceptions.JSONDecodeError:
                    e_ = e
                    break
                time.sleep(0.3)
                continue
        if type(e_) == requests.exceptions.JSONDecodeError:
            session.close()
            break
        if test == num - 1:
            print('{}【尝试次数：{}】-error'.format(item, test+1))
            break
        if len(rows) == 0:
            session.close()
            break
        make_model_year_dict, year_make_model_engine_ls, engine_ls = fetch_vehicle(rows, list_table_title,
                                                                                   make_model_year_dict,
                                                                                   year_make_model_engine_ls, engine_ls)
    if test != num - 1:
        vehicle = dict_to_str(make_model_year_dict)
        vehicle_engine = '\n'.join(year_make_model_engine_ls).strip()
        engine_ls = list(set(engine_ls))
        engine_ls.sort()
        engine_all = '\n'.join(engine_ls)
        wb = load_workbook(filename='./eBay_vehicle.xlsx')
        ws = wb['Data']
        serial = ws.max_row
        ws.append([serial, str(item), vehicle, engine_all, vehicle_engine])
        last_row = ws.max_row
        ws.row_dimensions[last_row].height = 20
        for col in range(1, 6):
            cell = ws.cell(row=last_row, column=col)
            cell.font = font
            cell.alignment = alignment
            cell.border = border
        wb.save(filename='./eBay_vehicle.xlsx')
        wb.close()
        print('{}-success，进度：{}/{}'.format(item, serial, len(items)))

pool = pool.Pool(15)
for item in items:
    url = 'https://www.ebay.com/itm/' + str(item)
    pool.spawn(fetch_data, url, item)
pool.join()


