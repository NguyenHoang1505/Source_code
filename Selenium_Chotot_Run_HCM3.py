#!/usr/bin/env python
# coding: utf-8

# In[111]:


print("Import package..........")
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from numpy import nan as NaN
import os
import time
from selenium.webdriver.chrome.options import Options
import json


# In[112]:


print("Init xpath..........")
data_xpath={"Tên người dùng":[],"SĐT":[],"Địa chỉ":[],"Khu vực":[],"Mặt hàng":[],"Giá":[],"Mô tả":[],"Thời gian đăng":[],"Loại tin":[]}
data_xpath['Tên người dùng']='//*[@id="app"]/div[2]/main/article/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/div/div[2]/div[1]'
data_xpath['Giá']='//*[@id="app"]/div[2]/main/article/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/span[1]/span[1]'
data_xpath['Mặt hàng']='//*[@id="app"]/div[2]/main/article/div[1]/div[2]/div[1]/div[2]/div[1]/h1'
data_xpath['Mô tả']='//*[@id="app"]/div[2]/main/article/div[1]/div[2]/div[1]/div[2]/p'
data_xpath['SĐT']='//*[@id="app"]/div[2]/main/article/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/h4/strong'
data_xpath['Địa chỉ']='//*[@id="app"]/div[2]/main/article/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/div/div[2]/div[2]/span'
data_xpath['Thời gian đăng']='//*[@id="app"]/div[2]/main/article/div[1]/div[2]/div[1]/div[1]/div[2]/span'
data_xpath['Khu vực']='//*[@id="app"]/div[2]/main/article/div[1]/div[2]/div[1]/div[2]/div[4]/div/div[2]/div'
data_xpath['Loại tin']='//*[@id="app"]/div[2]/main/article/div[1]/div[2]/div[1]/div[2]/div[3]/div/div/div/div[2]/span'


# In[113]:


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


# In[114]:


# chrome_options = webdriver.ChromeOptions()
# prefs = {"profile.managed_default_content_settings.images": 2}
# chrome_options.add_experimental_option("prefs", prefs)
# browser = webdriver.Chrome(chrome_options=chrome_options)
# browser.maximize_window()


# In[115]:


print("Setting chorme..........")
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
browser = webdriver.Chrome(chrome_options=chrome_options)


# In[116]:


print("Starting crawl..........")
Quan={'quan-tan-binh','quan-tan-phu','quan-thu-duc','huyen-binh-chanh','huyen-can-gio','huyen-cu-chi','huyen-hoc-mon','huyen-nha-be'}
for quan in Quan:
    file = open("Data_{0}.json".format(quan), "w",encoding='utf-8')
    max_page=10000
    for page in range(1,max_page):
        #Browser mở từng page trên chotot.Mỗi page có 20 item
        page_link="https://www.chotot.com/tp-ho-chi-minh/{0}/mua-ban?page={1}".format(quan,page)
        browser.get(page_link)
        time.sleep(3)
        Item_links=browser.find_elements_by_xpath("""//*[@id="app"]/div[2]/main/div/div/div[1]/main/div/div[1]/div[6]/div/div[2]/ul/div/li/a""")
        links_element=[]
        #Lấy link của từng item
        for link in Item_links:
            links_element.append(link.get_attribute("href"))
        #Crawl dữ liệu của 20 item
        for i in range(0,20):
            start = time.time()
            try:
                browser.get(links_element[i])
            except:
                continue
            time.sleep(1)
            print("Crawl item ",i," in page ",page," quan: ",quan,"....", end=' ')

            Crawl_item(i)
            print("Done in ",time.time() - start,"s.")
        time.sleep(1)
        browser.get(page_link)
        time.sleep(1)
        try:
            next_page=browser.find_element_by_class_name("last")
        except:
            print("Error")
            break
    file.close()

