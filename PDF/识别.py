import os
import easyocr
import pandas as pd

reader = easyocr.Reader(['en'])
list_file = list(os.walk('./file/part_right'))[0][2]
if '.DS_Store' in list_file:
   list_file.remove('.DS_Store')


file_name_ls = []
result_ls = []
for i in range(len(list_file)):
   result = reader.readtext('./file/part_right/' + list_file[i], detail=0)
   str_concat = '\n'.join(result)
   result_ls.append(str_concat)
   file_name_ls.append(list_file[i])

df = pd.DataFrame(columns=['文件名', '信息'])
df['文件名'] = file_name_ls
df['信息'] = result_ls
df.to_excel('./right_message.xlsx', index=False)

