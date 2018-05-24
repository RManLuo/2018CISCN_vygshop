import functools
from sshop.models import SiteConfig,db,User
import json
import tornado.web

def import_args(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        form_kwargs={k: self.get_argument(k) for k in self.request.arguments}
        form_kwargs.update(**kwargs)
        return method(self, *args, **form_kwargs)
    return wrapper

def template_kwargs_importer(*args):
    result=dict()
    for each in args:
        result.update(each)
    result.pop('self') # prevent error when calling
    return result

def read_config(config_name,default=None):
    try:
        sc=db.query(SiteConfig).filter(SiteConfig.name==config_name).one()
        return json.loads(sc.value)
    except:
        return default

def set_config(config_name,obj):
    try:
        sc=db.query(SiteConfig).filter(SiteConfig.name==config_name).one()
        sc.value=json.dumps(obj)
        db.commit()
    except:
        raise tornado.web.HTTPError(500)

def check_user_valid(method):
    """Decorate methods with this to require that the user is valid.
    Must put after @tornado.web.authenticated
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            if read_config('force_phone_check'):
                user=self.orm.query(User).filter(User.username == self.current_user).one()
                if not user.valid:
                    raise Exception
        except:
            if self.request.method in ("GET", "HEAD","POST"):
                url = '/user/check'
                self.redirect(url)
                return
        return method(self, *args, **kwargs)
    return wrapper

def check_user_admin(method):
    """Decorate methods with this to require that the user is admin.
    Must put after @tornado.web.authenticated
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.is_customer_service():
            raise tornado.web.HTTPError(404)
        return method(self, *args, **kwargs)
    return wrapper