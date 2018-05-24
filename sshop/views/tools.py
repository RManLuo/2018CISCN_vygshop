import functools

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