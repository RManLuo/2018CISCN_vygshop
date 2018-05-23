# coding:utf-8
import tornado.web
from sqlalchemy.orm.exc import NoResultFound
from sshop.base import BaseHandler
from sshop.models import Commodity, User, Ticket, SiteConfig
import requests, json
from Shop import check_user_valid
from tools import import_args

class SettingsSMSHandler(BaseHandler):
    @tornado.web.authenticated
    @check_user_valid
    def get(self):
        c = self.orm.query(SiteConfig).filter(SiteConfig.name=='sms_settings').one()
        return self.render('settings_sms.html',**json.loads(c.value))

    @tornado.web.authenticated
    @check_user_valid
    @import_args
    def post(self,api_url,method,name,template,test_tel, *args, **kwargs):
        c = self.orm.query(SiteConfig).filter(SiteConfig.name=='sms_settings').one()
        try:
            text = template.format(tel=test_tel, code='1234')
            if method == '0':
                requests.get(api_url, params={name: text})
            if method == '1':
                requests.post(api_url, data={name: text})
        except Exception, e:
            return self.render('settings_sms.html', danger=1, reason=str(e),**json.loads(c.value))
        else:
            c.value = json.dumps({"api_url": api_url,
                                  "method": method,

                                  "name": name,
                                  "template": template
                                  })
            self.orm.commit()
            return self.render('settings_sms.html', success=1,**json.loads(c.value))

