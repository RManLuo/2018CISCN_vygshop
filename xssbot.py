#!/usr/bin/env python
# -*- coding:utf-8 -*-
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import os
import time
import requests
from pyquery import PyQuery as PQ
import string
import random,re

class WebChecker:
    def __init__(self, ip, port, csrfname='_xsrf'):
        self.ip = ip
        self.port = port
        self.url = 'http://%s:%s/' % (ip, port)
        self.username = 'AdMIn_for_CH3k3r'
        self.password = 'AdMIn_for_CH3k3r_es7kyJwufk'
        self.change_pass = '654321'
        self.mail = 'i@qvq.im'
        self.csrfname = csrfname
        self.integral = None
        self.session = requests.session()

    def _generate_randstr(self, len=10):
        return ''.join(random.sample(string.ascii_letters, len))

    def _get_uuid(self):
        res = self.session.get(self.url + 'login')
        dom = PQ(res.text)
        return dom('form canvas').attr('rel')

    def _get_answer(self):
        uuid = self._get_uuid()
        answer = {}
        with open('./sshop/captcha/ans/ans%s.txt' % uuid, 'r') as f:
            for line in f.readlines():
                if line != '\n':
                    ans = line.strip().split('=')
                    answer[ans[0].strip()] = ans[1].strip()
        x = random.randint(int(float(answer['ans_pos_x_1'])),
                           int(float(answer['ans_width_x_1']) + float(answer['ans_pos_x_1'])))
        y = random.randint(int(float(answer['ans_pos_y_1'])),
                           int(float(answer['ans_height_y_1']) + float(answer['ans_pos_y_1'])))
        return x, y

    def _get_user_integral(self):
        res = self.session.get(self.url + 'user')
        dom = PQ(res.text)
        res = dom('div.user-info').text()
        integral = re.search('(\d+\.\d+)', res).group()
        return integral

    def _get_token(self, html):
        dom = PQ(html)
        form = dom("form")
        token = str(PQ(form)("input[name=\"%s\"]" % self.csrfname).attr("value")).strip()
        return token

    def login_test(self):
        print 'login at:'+self.url+'login'
        rs = self.session.get(self.url + 'login')
        token = self._get_token(rs.text)
        x, y = self._get_answer()
        rs = self.session.post(url=self.url + 'login', data={
            self.csrfname: token,
            "username": self.username,
            "password": self.password,
            "captcha_x": x,
            "captcha_y": y
        })
        try:
            dom = PQ(rs.text)
            error = dom("div.alert.alert-danger")
            error = PQ(error).text().strip()
            if len(error):
                print "[-] Login failed."
                return False
        except:
            pass
        response = self.session.get('http://127.0.0.1:8233/user')
        #print response.text
        return self.session.cookies.get_dict()






def main():
    driver = webdriver.PhantomJS(executable_path="D:\ciscn_web\phantomjs.exe")  # driver 地址
    driver.set_page_load_timeout(10)  # 加载网页延迟时间
    driver.set_script_timeout(10)  # 加载脚本延迟时间
    while 1:
        try:
            driver.delete_all_cookies()
            check=WebChecker('127.0.0.1','8233','_xsrf')
            Cokie=check.login_test()
            driver.add_cookie({'name':'username','value':Cokie['username'],'domain':'127.0.0.1','path':'/'})
            driver.get("http://127.0.0.1:8233/user")
            time.sleep(5)
            if "AdMIn_for_CH3k3r" in driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/div[1]/div/h5').text:  # 检查是否登陆后台
                print 'login sucess'
                driver.get('http://127.0.0.1:8233/tickets')
                try:
                    elem_comments = driver.find_elements_by_css_selector('body > div > div.block > div > div.ticket-list > table > tbody > tr > td.ticket-name > a')  # 后台留言列表
                    coment_list=[]
                    for i in elem_comments:
                        coment_list.append(i.get_attribute('href'))
                    count=0
                    for coment in coment_list:

                        count=count+1
                        if count > 5:
                            break
                        print coment
                        try:
                            driver.get(coment) # 打开留言
                            time.sleep(3)
                        except:
                            pass
                        #print driver.page_source
                        print time.strftime("%Y-%m-%d %X", time.localtime())  # 输出当前时间

                        # 暂停两秒访问下一个
                    print 'finish this round'
                      # 全部访问结束，退出
                    time.sleep(2)  # 暂停10s访问下一轮

                except Exception as e:
                    print "[error] " + str(e)

            else:
                print time.strftime("%Y-%m-%d %X", time.localtime())
                print "[info] can't login in"

        except Exception as e:
            print "[error] " + str(e)
if __name__=='__main__':
    main()

