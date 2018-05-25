# coding:utf-8
import tornado.web
from sqlalchemy.orm.exc import NoResultFound
from sshop.base import BaseHandler
from sshop.models import SMSHistory
import requests, json
from Shop import check_user_valid
from tools import *

class SettingsSMSHandler(BaseHandler):
    # only admin can access this
    @tornado.web.authenticated
    @check_user_admin
    def get(self,*args,**kwargs):
        force_phone_check = read_config('force_phone_check')
        c = read_config('sms_settings')
        return self.render('settings_sms.html',force_phone_check=force_phone_check,**c)

    @tornado.web.authenticated
    @check_user_admin
    @import_args
    def post(self,force_phone_check,api_url,method,name,template, *args, **kwargs):
        if force_phone_check:
            set_config('force_phone_check',True)
            c = read_config('sms_settings')
            if api_url: # means change value
                try:
                    set_config('sms_settings', {"api_url": api_url,
                                                "method": method,

                                                "name": name,
                                                "template": template
                                                })
                    self.orm.commit()
                except Exception, e:
                    return self.render('settings_sms.html',force_phone_check=force_phone_check, danger=1, reason=str(e),**c)
            return self.render('settings_sms.html', force_phone_check=force_phone_check,success=1,**c)
        else:
            set_config('force_phone_check', False)
            return self.render('settings_sms.html',  force_phone_check=force_phone_check,success=1)

class SMSHistoryHandler(BaseHandler):
    @tornado.web.authenticated
    @check_user_admin
    def get(self):
        return self.render('sms_history.html',history=self.orm.query(SMSHistory))