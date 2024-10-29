import pandas as pd
df_menu = pd.read_excel('./abc.xlsx', header=0)
other = df_menu['其他'].to_list()

for i in other:
    try:
        ls = i.split('OE')
        print(ls[0])
    except:
        ls = ['']
        print(ls[0])

#
# import os
#
# path = r"C:\Users\YangTeng\Desktop\新建文件夹\Juin-Daw-_-Quad-Sigma-Catalogue.jpg"
# file_name_list = os.listdir(path)
# file_name = str(file_name_list)
# file_name = file_name.replace("[", "").replace("]", "").replace("'", "").replace(",", "\n").replace(" ", "")
# f = open(path + "\\" + "文件list.txt", "a")
# f.write(file_name)