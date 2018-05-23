import functools

def import_args(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        form_kwargs={k: self.get_argument(k) for k in self.request.arguments}
        form_kwargs.update(**kwargs)
        return method(self, *args, **form_kwargs)
    return wrapper