#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :test.py
# @Time      :2023/10/21 10:41:45
# @Author    :Wang Hao

from selenium import webdriver
from selenium.webdriver.common.by import By

wd = webdriver.Chrome()
wd.implicitly_wait(5)
wd.get('http://ydfwpt.cug.edu.cn/index.html')
def choose_seat():
    element = wd.find_element(By.XPATH, "/html/body/div/ul/li[1]/a")
    element.click()
    element = wd.find_element(By.XPATH, "//*[@id='proDataList']/li[1]/a/dl/dt/div")
    element.click()

    element = wd.find_element(By.XPATH, "//*[@id='reserve']")
    element.click()

    element = wd.find_element(By.XPATH, "//*[@id='fullcourt']/li[5]/span[17]")
    element.click()

    element = wd.find_element(By.XPATH, "//*[@id='confirmbutton']")
    element.click()

    # 如果到这一步出现登录状态, 则需要提前设置好cookies，或者直接账号密码登录，否则不需要
    # current_handle = wd.current_window_handle
    print(wd.title.find("登录"))
    if wd.title.find("登录") != -1:
        # 设置用户名
        user = wd.find_element(By.XPATH, "//*[@id='form1']/ul/li[1]/input")
        pwd = wd.find_element(By.XPATH, "//*[@id='usermm']")
        user.send_keys('1202211216')
        pwd.send_keys("060030")
        btn = wd.find_element(By.XPATH, "//*[@id='login']/button")
        btn.click()
        return False
    print("请手动支付")
    return True
        # 设置登录密码
# 需要判断当前是否可以抢票
if not choose_seat():
    choose_seat()
else:
    print("请手动支付")
pass