# -*- coding: utf-8 -*- 
# @Time ： 2024/6/29 11:01
# @Auth ： Westbroobo
# @File ：1.Rockauto_menu.py

import requests
import pandas as pd
from bs4 import BeautifulSoup
from tool import UA
import re

url = 'https://www.rockauto.com/en/parts/standard+motor+products,mass+air+flow+(maf)+sensor,5128'
rsp = requests.get(url=url, headers=UA.get_User_Agent_Requests())
html = rsp.content.decode(errors='ignore')
soup = BeautifulSoup(html, 'lxml')
a_tags = soup.find_all('a', class_='navlabellink nvoffset nnormal')
Part_Number = []
Url = []
for a in a_tags:
    text = re.compile(r'<a.+?\>(.+?)\<.*>').findall(str(a))
    href = re.compile(r'<a.+?href=\"(.+?)\".*>').findall(str(a))
    Part_Number.append(text[0])
    Url.append('https://www.rockauto.com' + href[0])
df = pd.DataFrame(columns=['Part_Number', 'Url'])
df['Part_Number'] = Part_Number
df['Url'] = Url
df.to_excel('./Rockauto_menu.xlsx', index=False)


