import xlsxwriter
import os

list_file = list(os.walk('./file/pic_right'))[0][2]
wb = xlsxwriter.Workbook('./PIC_r.xlsx')
ws = wb.add_worksheet('图片')
ws.set_column('A:A', 20)
ws.set_column('B:B', 15)
headings = ['文件名', '图片']
head_format = wb.add_format({'bold': 1, 'fg_color': 'cyan', 'align': 'center', 'font_name': u'微软雅黑', 'valign': 'vcenter'})
cell_format = wb.add_format({'bold': 0, 'align': 'center', 'font_name': u'微软雅黑', 'valign': 'vcenter'})
ws.write_row('A1', headings, head_format)

for k in range(len(list_file)):
    ws.set_row(k+1, 40)
    ws.write(k+1, 0, list_file[k], cell_format)
    ws.insert_image('B'+str(k+2), f'./file/pic_right/{list_file[k]}',
                    {'x_scale': 0.2, 'y_scale': 0.2})
wb.close()
