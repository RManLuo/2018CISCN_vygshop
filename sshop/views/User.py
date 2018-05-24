import tornado.web
from sqlalchemy.orm.exc import NoResultFound
from sshop.base import BaseHandler
from sshop.models import User
import bcrypt
import random
import re
from tools import *
import requests

class UserLoginHanlder(BaseHandler):
    def get(self, *args, **kwargs):
        self.application._generate_captcha()
        return self.render('login.html', ques=self.application.question, uuid=self.application.uuid)

    def post(self,*args,**kwargs):
        if not self.check_captcha():
            return self.render('login.html', danger=1, ques=self.application.question, uuid=self.application.uuid)
        username = self.get_argument('username')
        password = self.get_argument('password')
        if username and password:
            try:
                user = self.orm.query(User).filter(User.username == username).one()
            except NoResultFound:
                return self.render('login.html', danger=1, ques=self.application.question, uuid=self.application.uuid)
            if user.check(password):
                self.set_secure_cookie('username', user.username)
                self.redirect('/user')
            else:
                return self.render('login.html', danger=1, ques=self.application.question, uuid=self.application.uuid)


class RegisterHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.application._generate_captcha()
        return self.render('register.html', ques=self.application.question, uuid=self.application.uuid)

    def post(self, *args, **kwargs):
        if not self.check_captcha():
            return self.render('register.html', danger=1, ques=self.application.question, uuid=self.application.uuid)
        username = self.get_argument('username')
        mail = self.get_argument('mail')
        password = self.get_argument('password')
        password_confirm = self.get_argument('password_confirm')
        invite_user = self.get_argument('invite_user')
        phone_number = ''

        if password != password_confirm:
            return self.render('register.html', danger=1, ques=self.application.question, uuid=self.application.uuid)
        if mail and username and password:
            try:
                # have user
                user = self.orm.query(User).filter(User.username == username).one()
                return self.render('register.html', danger=1, ques=self.application.question,uuid=self.application.uuid)
            except NoResultFound:
                check_code = "%04d" % random.randint(0, 9999)
                user=User(username=username, mail=mail,check_code=check_code,phone_number=phone_number,
                                  password=bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()))
                self.orm.add(user)

                print(check_code)

                self.orm.commit()
                try:
                    inviteUser = self.orm.query(User).filter(User.username == invite_user)\
                        .filter(User.username != username).one()
                    inviteUser.integral += 10
                    user.inviter_id=inviteUser.id
                    self.orm.commit()
                except NoResultFound:
                    pass
                self.redirect('/login')
        else:
            return self.render('register.html', danger=1, ques=self.application.question, uuid=self.application.uuid)


class ResetPasswordHanlder(BaseHandler):
    def get(self, *args, **kwargs):
        self.application._generate_captcha()
        return self.render('reset.html', ques=self.application.question, uuid=self.application.uuid)

    def post(self, *args, **kwargs):
        if not self.check_captcha():
            return self.render('reset.html', danger=1, ques=self.application.question, uuid=self.application.uuid)
        return self.redirect('/login')


class changePasswordHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        return self.render('change.html')

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        old_password = self.get_argument('old_password')
        password = self.get_argument('password')
        password_confirm = self.get_argument('password_confirm')
        print old_password, password, password_confirm
        user = self.orm.query(User).filter(User.username == self.current_user).one()
        if password == password_confirm:
            if user.check(old_password):
                user.password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
                self.orm.commit()
                return self.render('change.html', success=1)
        return self.render('change.html', danger=1)


class UserInfoHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        user = self.orm.query(User).filter(User.username == self.current_user).one()
        return self.render('user.html', user=user)


class UserLogoutHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.clear_cookie('username')
        self.redirect('/login')

class UserCheckHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        # get regenerate
        user = self.orm.query(User).filter(User.username == self.current_user).one()
        return self.render('usercheck.html', user=user)

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        code = self.get_argument('code')
        print code
        user = self.orm.query(User).filter(User.username == self.current_user).one()
        if user.check_code==code:
            user.valid=True
            try:
                inviteUser = self.orm.query(User).filter(User.id==user.inviter_id).one()
                inviteUser.integral += 10
            except NoResultFound:
                pass
            self.orm.commit()
            return self.redirect('/user')
        return self.render('usercheck.html', user=user, danger=1)

class UserCheckRegenHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        # get regenerate
        user = self.orm.query(User).filter(User.username == self.current_user).one()
        user.check_code="%04d"%random.randint(0, 9999)
        print(user.check_code)
        self.orm.commit()
        c=read_config('sms_settings')
        api_url=c["api_url"]
        method=c["method"]
        name=c["name"]
        template=c["template"]
        text = template.format(tel=user.phone_number, code='1234')
        try:
            if method == '0':
                requests.get(api_url, params={name: text})
            if method == '1':
                requests.post(api_url, data={name: text})
        except Exception,e:
            print str(e)
        return self.redirect('/user/check')

class UserIntroHandler(BaseHandler):
    @tornado.web.authenticated
    @import_args
    def get(self,id, *args, **kwargs):
        try:
            user=self.orm.query(User).filter(User.id==id).one()
        except:
            raise tornado.web.HTTPError(404)
        return self.render('userinfo.html',user=user,**kwargs)