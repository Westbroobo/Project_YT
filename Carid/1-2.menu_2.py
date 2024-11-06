"""
Filename:1-2.menu_2.py
Author: Westbroobo
Date: 2024/11/5
"""

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

option = ChromeOptions()
option.add_experimental_option('useAutomationExtension', False)
option.add_argument('--disable-blink-features=AutomationControlled')
option.add_argument('--disable-dev-shm-usage')
option.add_argument('--disable-gpu')
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_argument('--no-sandbox')
option.add_argument('User-Agent=Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36')
# option.add_argument('--headless')
option.page_load_strategy = 'normal'
option.page_load_strategy = 'eager'
option.binary_location = 'G:/Chrome-bin107/chrome.exe'
service = Service(executable_path=r'./chromedriver.exe')
title_ls = []
img_ls = []
href_ls = []
for page in range(6, 11):
    browser = webdriver.Chrome(service=service)
    browser.maximize_window()
    url = 'https://www.carid.com/valeo/wiper-blades/?page={}#prod-list'.format(page)
    browser.get(url=url)
    wait = WebDriverWait(browser, 60)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="js-product-list-item"]')))
    items = browser.find_elements(By.XPATH, '//*[@class="js-product-list-item"]')
    if len(items) > 30:
        items = items[:30]
    for item in items:
        img = item.find_element(By.XPATH, './div[1]/img').get_attribute('data-src')
        href = item.find_element(By.XPATH, './/div[@class="lst-main"]/div[1]/a').get_attribute('href')
        title = item.find_element(By.XPATH, './/div[@class="lst-main"]/div[1]/a').text
        title_ls.append(title)
        img_ls.append(img)
        href_ls.append(href)
    browser.quit()
df = pd.DataFrame(columns=['Title', 'Img', 'Url'])
df['Title'] = title_ls
df['Img'] = img_ls
df['Url'] = href_ls
df.to_excel('./menu.xlsx', index=False)

