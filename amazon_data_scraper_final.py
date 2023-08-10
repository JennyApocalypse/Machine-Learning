# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import lxml
import lxml.html as lh
from time import sleep
from bs4 import BeautifulSoup


output = open('Flipkart Scraper.csv','a',newline='',encoding = 'utf-8-sig')
writer = csv.writer(output)
chrome_path = r"C:\Users\prero\Downloads\chromedriver_win32\chromedriver.exe"
driver=webdriver.Chrome(chrome_path)
url='https://www.flipkart.com/'
driver.get(url)
print(url)
sleep(2)

input_field=driver.find_element_by_xpath('//input[@class="_3704LK"]')
input_field.send_keys('gaming laptop')
sleep(5)
##SEARCH BUTTON
search_enter=driver.find_element_by_xpath('//button[@type="submit"]')
search_enter.click()
sleep(3)
html=driver.page_source
doc1=lh.fromstring(html)
try:
    no=doc1.xpath('//div[@class="_2MImiq"]/span[1]/text()')
    page = no[0].replace("Page 1 of ","")
    page = int(page)
    print(page)
except:
    page=1
main_url = driver.current_url
    
for i in range(1,page+1):    
    c_url = main_url+'&page='+str(i)
    driver.get(c_url)
    sleep(3)
    total_height=int(driver.execute_script("return document.body.scrollHeight"))
    for i in range(1,total_height,5):
        driver.execute_script("window.scrollTo(0, {});".format(i))
    sleep(3)
    page_html = driver.page_source
    soup=BeautifulSoup(page_html,'html.parser')
    doc=lh.fromstring(page_html)
    results = soup.findAll('div',attrs={'class':'_4ddWXP'})
    for data in results:
        name = data.find('a', attrs={'class':'s1Q9rs'}).text
        desc = data.find('div', attrs={'class':'_3Djpdu'}).text
        new_price = data.find('div', attrs = {'class':'_30jeq3'}).text
        try:
            old_price = data.find('div', attrs = {'class':'_3I9_wc'}).text
        except:
            old_price = ''
        try:
            reviews = data.find('span',attrs = {'class':'_2_R_DZ'})
            reviews = reviews.text
        except:
            reviews = ''
        try:
            rating = data.find('div',attrs = {'class':'_3LWZlK'})
            rating = rating.text
        except:
            rating = ''
        try:
            discount = data.find('div',attrs = {'class':'_3Ay6Sb'}).text
        except:
            discount = ''
        writer.writerow([name, desc, rating, reviews, new_price, old_price, discount])

driver.close()
output.close()