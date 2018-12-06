#!/usr/bin/env python
# coding: utf-8

# In[51]:

print("Import package.........")
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from numpy import nan as NaN
import os
import time
from selenium.webdriver.chrome.options import Options
import json


# In[52]:

print("Init data_xpath.........")

data_xpath={"Tên người dùng":[],"SĐT":[],"Địa chỉ":[],"Khu vực":[],"Mặt hàng":[],"Giá":[],"Mô tả":[],"Thời gian đăng":[],"Loại tin":[]}


# In[53]:


data_xpath['Tên người dùng']='//*[@id="app"]/div[2]/main/article/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/div/div[2]/div[1]'
data_xpath['Giá']='//*[@id="app"]/div[2]/main/article/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/span[1]/span[1]'
data_xpath['Mặt hàng']='//*[@id="app"]/div[2]/main/article/div[1]/div[2]/div[1]/div[2]/div[1]/h1'
data_xpath['Mô tả']='//*[@id="app"]/div[2]/main/article/div[1]/div[2]/div[1]/div[2]/p'
data_xpath['SĐT']='//*[@id="app"]/div[2]/main/article/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/h4/strong'
data_xpath['Địa chỉ']='//*[@id="app"]/div[2]/main/article/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/div/div[2]/div[2]/span'
data_xpath['Thời gian đăng']='//*[@id="app"]/div[2]/main/article/div[1]/div[2]/div[1]/div[1]/div[2]/span'
data_xpath['Khu vực']='//*[@id="app"]/div[2]/main/article/div[1]/div[2]/div[1]/div[2]/div[4]/div/div[2]/div'
data_xpath['Loại tin']='//*[@id="app"]/div[2]/main/article/div[1]/div[2]/div[1]/div[2]/div[3]/div/div/div/div[2]/span'


# In[54]:


def Crawl_item(i):
    data={}
    data['Stt']="Item "+str(i)+" page "+str(page)
    try:
        Id=browser.current_url.split('/')[5].split('.')[0]
        data['Id']=Id
    except:
        data['Id']=NaN
    try:
        data['Tên người dùng']=browser.find_element_by_xpath(data_xpath['Tên người dùng']).text
    except:
        data['Tên người dùng']=NaN
    try:
        data['SĐT']=browser.find_element_by_id("sms_btn").get_attribute("href").split('sms:')[1]
    except:
        data['SĐT']=NaN
    try:
        data['Địa chỉ']=browser.find_element_by_xpath(data_xpath['Địa chỉ']).text
    except:
        data['Địa chỉ']=NaN
    try:
        data['Khu vực']=browser.find_element_by_xpath(data_xpath['Khu vực']).text
    except:
        data['Khu vực']=NaN
    try:
        data['Giá']=browser.find_element_by_xpath(data_xpath['Giá']).text
    except:
        data['Giá']=NaN
    try:
        data['Mô tả']=browser.find_element_by_xpath(data_xpath['Mô tả']).text
    except:
        data['Mô tả']=NaN
    try:
        data['Mặt hàng']=browser.find_element_by_xpath(data_xpath['Mặt hàng']).text
    except:
        data['Mặt hàng']=NaN
    try:
        data['Loại tin']=browser.find_element_by_xpath(data_xpath['Loại tin']).text
    except:
        data['Loại tin']='Cần bán'
    try:
        data['Thời gian đăng']=browser.find_element_by_xpath(data_xpath['Thời gian đăng']).text
    except:
        data['Thời gian đăng']=NaN
    data['Url']=browser.current_url
    line = json.dumps(dict(data), ensure_ascii=False)+"\n"
    file.write(line)


# In[56]:


# chrome_options = webdriver.ChromeOptions()
# prefs = {"profile.managed_default_content_settings.images": 2}
# chrome_options.add_experimental_option("prefs", prefs)
# browser = webdriver.Chrome(chrome_options=chrome_options)
# browser.maximize_window()


# In[57]:

print("Setting chrome.........")

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
print("Opening chrome.........")
browser = webdriver.Chrome(chrome_options=chrome_options)


# In[58]:


file = open("Data.json", "w",encoding='utf-8')


# In[59]:
print("Starting crawl.........")


for page in range(1,700):
    page_link="https://www.chotot.com/ha-noi/quan-hai-ba-trung/mua-ban?page={0}".format(page)
    browser.get(page_link)
    time.sleep(5)
    Item_links=browser.find_elements_by_xpath("""//*[@id="app"]/div[2]/main/div/div/div[1]/main/div/div[1]/div[6]/div/div[2]/ul/div/li/a""")
    links_element=[]
    for link in Item_links:
        links_element.append(link.get_attribute("href"))
    for i in range(0,20):
        start = time.time()
        try:
            browser.get(links_element[i])
        except:
        	continue
        time.sleep(1)
        print("Crawl item ",i," in page ",page,"....",end=' ')
        Crawl_item(i)
        print("Done in ",time.time() - start,"s.")
    time.sleep(2)


# In[60]:


file.close()


# In[ ]:





# In[ ]:



