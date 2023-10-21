#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :autoBook.py
# @Time      :2023/10/21 13:39:46
# @Author    :Wang Hao
import datetime
import time
import json
import selenium

from time import sleep, time
from time import sleep

from json import loads

from selenium import webdriver
from selenium.webdriver.common.by import By

"""
枚举类型
"""
TIME_MAX = 22
TIME_MIN = 10

class Badminton(object):
    def __init__(self, user_name, pwd, target_url, login_url):
         self.user_name = user_name
         self.pwd = pwd
         self.target_url = target_url
         self.login_url = login_url
    def login(self):
        print("---开始登录---")
        self.wd = webdriver.Chrome()
        # 隐式等待
        self.wd.implicitly_wait(5)
        self.wd.get(self.login_url)
        if self.wd.title.find("登录") != -1:
            # 设置用户名和密码
            user = self.wd.find_element(By.XPATH, "//*[@id='form1']/ul/li[1]/input")
            pwd = self.wd.find_element(By.XPATH, "//*[@id='usermm']")
            user.send_keys(self.user_name)
            pwd.send_keys(self.pwd)
            btn = self.wd.find_element(By.XPATH, "//*[@id='login']/button")
            btn.click()
        print("---登录成功---")
    def come_to_select(self):
        element = self.wd.find_element(By.XPATH, "/html/body/div/ul/li[1]/a")
        element.click()
        element = self.wd.find_element(By.XPATH, "//*[@id='proDataList']/li[1]/a/dl/dt/div")
        element.click()

        element = self.wd.find_element(By.XPATH, "//*[@id='reserve']")
        element.click()

    def check_site(self, time_slots, time1, time2, site):
        print(time1, time2, site)
        if time1 < TIME_MAX - time_slots or time2 < TIME_MAX - time_slots:
             return False, None, None
        site1 = self.wd.find_element(By.XPATH, "//*[@id='fullcourt']/li["+ str(time1 - TIME_MAX + time_slots + 1) + "]/span["+ str(site) +"]")
        site2 = self.wd.find_element(By.XPATH, "//*[@id='fullcourt']/li["+ str(time2 - TIME_MAX + time_slots + 1) + "]/span["+ str(site) +"]")
        # 如果两个场都没有被出售，则返回True，否则返回False
        print(site1.get_attribute('innerText'))
        print(site2.get_attribute('innerText'))
        flag1 = site1.get_attribute('innerText').find("已售")
        flag2 = site2.get_attribute('innerHTML').find("已售")
        if flag1 != -1 or flag2 != -1:
            # 如果存在一个不行，需要取消点击
            self.choose_site(site1, site2)
            return False, None, None
        return True, site1, site2
    def choose_site(self, site1, site2):
         site1.click()
         site2.click()
    def confirm_order(self):
        confirm = self.wd.find_element(By.XPATH, "//*[@id='confirmbutton']")
        confirm.click()
    def select(self):
        # 首先需要判断当前选择的场地是属于第几行第几列
        # 直接通过全部时间段来确定
        fullcourt = self.wd.find_elements(By.XPATH, "//*[@id='fullcourt']/*")
        print(len(fullcourt))
        time_slots = len(fullcourt)
        # 开始遍历想要占的场地
        f = open("sites.txt")
        flag = False
        for site in f.readlines():
            site = site.split()
            valid, site1, site2 = self.check_site(time_slots, int(site[0]), int(site[1]), int(site[2]))
            if valid:
                self.choose_site(site1, site2)
                self.confirm_order()
                flag = True
            else:
                continue
        if flag:
            print("---请及时支付---")
        else:
            print("---您预定的座位已经没有---")
        
    def book(self):
        self.login()
        self.come_to_select()
        print("---开始选择场地---")
        self.select()


if __name__ == '__main__':
    # startTime = datetime.datetime(2019, 9, 25, 9, 17, 7)  #定时功能：2019-9-25 09:17:07秒开抢
    # print('程序还未开始...')
    # while datetime.datetime.now() < startTime:
    #     sleep(1)
    # print('开始预定 %s' % startTime)
    # print('正在执行...')
    try:
        with open('./conf.json', 'r', encoding='utf-8') as f:
                    config = loads(f.read())
        bad = Badminton(config["user"], config["pwd"], config["target_url"], config["login_url"])
        bad.book()
    except Exception as e:  
        print(e)
        raise Exception("***错误：初始化失败，请检查配置文件***")