import functools
from sshop.models import SiteConfig,db
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