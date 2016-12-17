#!/usr/bin/python
# -*- coding: utf-8 -*-
import selenium
from selenium import webdriver
import os

from selenium import webdriver
chromedriver = "C:\\Users\JasonXiaohan\AppData\Local\Google\Chrome\Application\chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
driver =  webdriver.Chrome(chromedriver)
driver.get("http://www.mafengwo.cn/gonglve/")
# driver.maximize_window()
elems=driver.find_elements_by_xpath('//*[@class="nav-panel rank-panel"]/ol')
for e in elems:
    for li in e.find_element_by_xpath("//li"):
        print(li.text)
# //*[@id="slide_box"]/li[4]/a/img
# result = [row.find_elements_by_xpath('//a')[0].get_attribute("href") for row in elem.find_elements_by_xpath('//*[@id="slide_box"]/li') if row.find_elements_by_xpath('//a/img/src') !=None
#           ]
# print(elem)


driver.quit()




