# coding:utf-8
import tornado.web
from sqlalchemy.orm.exc import NoResultFound
from sshop.base import BaseHandler
from sshop.models import Commodity, User, Ticket, SiteConfig
import requests, json
from Shop import check_user_valid
from tools import *

class SettingsSMSHandler(BaseHandler):
    @tornado.web.authenticated
    @check_user_valid
    def get(self,*args,**kwargs):
        force_phone_check = read_config('force_phone_check')
        c = read_config('sms_settings')
        return self.render('settings_sms.html',force_phone_check=force_phone_check,**c)

    @tornado.web.authenticated
    @check_user_valid
    @import_args
    def post(self,force_phone_check=None,api_url=None,method=None,name=None,template=None,test_tel=None, *args, **kwargs):
        if force_phone_check:
            set_config('force_phone_check',True)
            c = read_config('sms_settings')
            if api_url: # means change value
                try:
                    text = template.format(tel=test_tel, code='1234')
                    if method == '0':
                        requests.get(api_url, params={name: text})
                    if method == '1':
                        requests.post(api_url, data={name: text})
                except Exception, e:
                    return self.render('settings_sms.html', danger=1, reason=str(e),**c)
                else:
                    set_config('sms_settings',{"api_url": api_url,
                                          "method": method,

                                          "name": name,
                                          "template": template
                                          })
                    self.orm.commit()
            return self.render('settings_sms.html', force_phone_check=force_phone_check,success=1,**c)
        else:
            set_config('force_phone_check', False)
            return self.render('settings_sms.html',  force_phone_check=force_phone_check,success=1)
