import tornado.web
from models import db
from sshop.models import User
from settings import *
from views.tools import *

class BaseHandler(tornado.web.RequestHandler):
    @property
    def orm(self):
        return db()

    def on_finish(self):
        db.remove()

    def get_current_user(self):
        return self.get_secure_cookie("username")

    def get_current_user_obj(self):
        return self.orm.query(User).filter(User.username==self.get_current_user()).one()

    def is_customer_service(self):
        if self.get_current_user():
            return self.get_current_user_obj().permission >= customer_service_permission_level
        else:
            return False

    def is_super_admin(self):
        if self.get_current_user():
            return self.get_current_user_obj().permission >= super_admin_permission_level
        else:
            return False

    def check_captcha(self):
        try:
            x = float(self.get_argument('captcha_x'))
            y = float(self.get_argument('captcha_y'))
            if x and y:
                # hey gay
                # uuid = self.application.decrypt(self.application.uuid)
                uuid= self.application.real_uuid
                answer = self.application._get_ans(uuid)
                print x,y,uuid, answer
                self.application._generate_captcha() # regen to make post method
                if float(answer['ans_pos_x_1']) <= x <= (float(answer['ans_width_x_1']) + float(answer['ans_pos_x_1'])):
                    if float(answer['ans_pos_y_1']) <= y <= (
                            float(answer['ans_height_y_1']) + float(answer['ans_pos_y_1'])):
                        return True
                return False
        except Exception as ex:
            print str(ex)
            return False

    def render(self, template_name, **kwargs):
        modes=dict()
        modes['super_admin_mode']=True if self.is_super_admin() else False
        modes['customer_service_mode'] = True if self.is_customer_service() else False
        super(BaseHandler, self).render(template_name=template_name,**template_kwargs_importer(modes,kwargs))

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('404.html')
        elif status_code == 403:
            self.render('403.html')
        else:
            super(BaseHandler, self).write_error(status_code, **kwargs)