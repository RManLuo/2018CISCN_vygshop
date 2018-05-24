from Shop import *
from User import *
from Captcha import *
from Ticket import *
from Settings import *

handlers = [

    (r'/', ShopIndexHandler),
    (r'/shop', ShopListHandler),
    (r'/info/(\d+)', ShopDetailHandler),
    (r'/seckill', SecKillHandler),
    (r'/shopcar', ShopCarHandler),
    (r'/shopcar/add', ShopCarAddHandler),
    (r'/pay', ShopPayHandler),

    (r'/captcha', CaptchaHandler),

    (r'/user', UserInfoHandler),
    (r'/user/(\d+)', UserIntroHandler),
    (r'/user/change', changePasswordHandler),
    (r'/pass/reset', ResetPasswordHanlder),
    (r'/user/check',UserCheckHandler),
    (r'/user/check/regen', UserCheckRegenHandler),

    (r'/login', UserLoginHanlder),
    (r'/logout', UserLogoutHandler),
    (r'/register', RegisterHandler),

    (r'/tickets', TicketIndexHandler),
    (r'/tickets/create', TicketCreateHandler),
    (r'/tickets/(\d+)', TicketDetailHandler),

    (r'/settings/sms',SettingsSMSHandler),
]