import tornado.web


class CaptchaHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        # hey gay
        # file = open(self.application.jpgs_path + '/ques%s.jpg' % self.application.decrypt(self.application.uuid),'rb')
        file = open(self.application.jpgs_path + '/ques%s.jpg' % self.application.real_uuid, 'rb')
        self.write(file.read())
        file.close()
        self.set_header('Content-Type', 'image/jpeg')