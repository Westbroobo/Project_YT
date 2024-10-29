# -*- coding: utf-8 -*- 
# @Time ： 2024/7/10 9:08
# @Auth ： Westbroobo
# @File ：save_pic_irregular.py

import os
from PIL import Image
import xlsxwriter

list_file = list(os.walk(r'C:/Users/YangTeng/Pictures/新建文件夹'))[0][2]
list_file = [f for f in list_file if not f.endswith('.tmp')]
wb = xlsxwriter.Workbook('PIC.xlsx')
ws = wb.add_worksheet('Pic')
ws.set_column('A:A', 15)
ws.set_column('B:B', 15)
headings = ['文件名', '图片']
head_format = wb.add_format({'bold': 1, 'fg_color': 'cyan', 'align': 'center', 'font_name': u'微软雅黑', 'valign': 'vcenter'})
cell_format = wb.add_format({'bold': 0, 'align': 'center', 'font_name': u'微软雅黑', 'valign': 'vcenter'})
ws.write_row('A1', headings, head_format)

row = 1
supported_formats = ['jpg', 'jpeg', 'png', 'bmp', 'gif']
for file_name in list_file:
    file_path = os.path.join(r'C:/Users/YangTeng/Pictures/新建文件夹', file_name)
    file_extension = file_name.split('.')[-1].lower()
    if file_extension in supported_formats:
        try:
            # 打开图片验证格式
            img = Image.open(file_path)
            img.verify()  # 验证文件是否为有效图片
            img = Image.open(file_path)  # 重新打开图片
            img = img.convert('RGB')  # 转换为RGB模式（某些图片可能是RGBA模式）
            png_path = file_path.rsplit('.', 1)[0] + '.png'
            img.save(png_path, 'PNG')

            ws.set_row(row, 40)
            ws.write(row, 0, file_name.rsplit('.', 1)[0], cell_format)
            ws.insert_image(f'B{row + 1}', png_path, {'x_scale': 0.2, 'y_scale': 0.2})
            row += 1
        except Exception as e:
            print(f"{file_name} 不是有效图片格式或不受支持: {e}")

wb.close()


