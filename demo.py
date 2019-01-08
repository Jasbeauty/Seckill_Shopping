#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2018/10/18 4:13 PM
# @Author: jasmine sun
# @File  : demo.py


# selenium: web端自动化测试框架
import time
import json

from selenium import webdriver
from selenium.webdriver import ActionChains

chrome_driver = '/usr/local/bin/chromedriver'
driver = webdriver.Chrome(chrome_driver)
driver.get('https://login.taobao.com')


def login_by_qcode():
    qcode = driver.find_element_by_id("J_QRCodeImg")

    action = ActionChains(driver)
    action.reset_actions()
    action.move_to_element(qcode)
    action.move_by_offset(20, -20).click()
    action.perform()

    while True:
        url = driver.current_url

        if not url.startswith("https://login.taobao.com"):
            cookies = driver.get_cookies()
            res = ""
            for cookie in cookies:
                res += cookie.get('name') + '=' + cookie.get('value') + ';'

            res = res[:-1]
            print(res)
            break

        try:
            refresh = driver.find_element_by_class_name("J_QRCodeRefresh")
            refresh.click()
        except:
            pass

        time.sleep(6)

    # driver.quit()


def login_by_cookie():
    # 初次建立连接，随后方可修改cookie
    driver.get('https://login.taobao.com/member/login.jhtml')
    # 获取cookie并通过json模块将dict转化成str
    dictCookies = driver.get_cookies()
    jsonCookies = json.dumps(dictCookies)
    # 登录完成后，将cookie保存到本地文件
    with open('cookies.json', 'w') as f:
        f.write(jsonCookies)

    # 读取登录时存储到本地的cookie
    with open('cookies.json', 'r', encoding='utf-8') as f:
        listCookies = json.loads(f.read())

    cookie_dict = {}
    for i in listCookies:
        cookie_dict[i['name']] = i['value']

    print(cookie_dict)

    for cookie in listCookies:
        driver.add_cookie({
            'domain': '.taobao.com',  # 此处xxx.com前，需要带点
            'name': cookie['name'],
            'value': cookie['value'],
            'path': '/',
            'expires': None
        })
    # 再次访问页面，便可实现免登陆访问
    driver.get('https://login.taobao.com/member/login.jhtml')


def enter_seckill_page(url):
    driver.get(url)


def confirm_seckill():
    is_seckill = True
    while True:
        try:
            # 未开团
            driver.find_element_by_class_name('J_JuSMSRemind')
            is_seckill = False
        except Exception as e:
            print("we are now can seckill!")
            is_seckill = True

        if not is_seckill:
            time.sleep(6)
            enter_seckill_page(
                'https://detail.ju.taobao.com/home.htm?spm=608.2291429.102212b.1.39c24f845jKYSt&id=10000103865737&item_id=577390088186')
        else:
            submit = driver.find_element_by_class_name('J_BuySubmit')
            submit.click()
            break


if __name__ == '__main__':
    # login_by_qcode()
    # enter_seckill_page('https://detail.ju.taobao.com/home.htm?spm=608.2291429.102212b.1.39c24f845jKYSt&id=10000103865737&item_id=577390088186')
    # confirm_seckill()
    login_by_cookie()
