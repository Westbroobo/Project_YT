# -*- coding: utf-8 -*- 
# @Time ： 2024/2/27 16:59
# @Auth ： Westbroobo
# @File ：download_pic_selenium.py

import urllib3
import pandas as pd
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver import ChromeOptions
import asyncio
urllib3.disable_warnings()

df_menu = pd.read_excel('./menu_img.xlsx')
Url = df_menu['img'].to_list()
Part_Number = df_menu['Part_Number'].to_list()
option = ChromeOptions()
option.add_experimental_option('useAutomationExtension', False)
option.add_argument('--disable-blink-features=AutomationControlled')
option.add_argument('--disable-dev-shm-usage')
option.add_argument('--disable-gpu')
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_argument('user-agent=' + str(UserAgent(path="E:/BaiduNetdiskDownload/ua.json").random))
option.add_argument('--no-sandbox')
option.page_load_strategy = 'normal'
option.page_load_strategy = 'eager'
option.binary_location = 'E:/Chrome-bin107/chrome.exe'
browser = webdriver.Chrome(executable_path=r'E:/采购工作/workplace-2/tool/chromedriver.exe', options=option)
browser.maximize_window()


async def pic_down(url):
    browser.get(url=url)
    index = Url.index(url)
    pic_num = Part_Number[index]
    js_script = """
        var link = document.createElement('a');
        link.href = arguments[0];
        link.download = '{}';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        """.format(pic_num)
    browser.execute_script(js_script, url)

# 最后手动关闭浏览器以预留时间下载完成
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = [pic_down(url) for url in Url]
    loop.run_until_complete(asyncio.gather(*tasks))
