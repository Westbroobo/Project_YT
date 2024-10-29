# -*- coding: utf-8 -*- 
# @Time ： 2024/8/9 15:58
# @Auth ： Westbroobo
# @File ：2.Pic_Save.py

import os
import xlsxwriter
list_file = list(os.walk(r'C:/Users/YangTeng/Pictures/新建文件夹'))[0][2]
list_file = [f for f in list_file if not f.endswith('.tmp')]
wb = xlsxwriter.Workbook('./PIC.xlsx')
ws = wb.add_worksheet('Pic')
ws.set_column('A:A', 15)
ws.set_column('B:B', 15)
headings = ['文件名', '图片']
head_format = wb.add_format({'bold': 1, 'fg_color': 'cyan', 'align': 'center', 'font_name': u'微软雅黑', 'valign': 'vcenter'})
cell_format = wb.add_format({'bold': 0, 'align': 'center', 'font_name': u'微软雅黑', 'valign': 'vcenter'})
ws.write_row('A1', headings, head_format)

for k in range(len(list_file)):
    ws.set_row(k+1, 40)
    ws.write(k+1, 0, list_file[k].replace('.jpg', '').replace('.jfif', ''), cell_format)
    ws.insert_image('B'+str(k+2), f'C:/Users/YangTeng/Pictures/新建文件夹/{list_file[k]}',
                    {'x_scale': 0.2, 'y_scale': 0.2})
wb.close()
