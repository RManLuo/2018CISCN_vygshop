# coding:utf-8
import os
import string
import bcrypt
import random
from datetime import date
import json

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.sqlite import FLOAT, VARCHAR, INTEGER, BOOLEAN
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from settings import connect_str

BaseModel = declarative_base()
engine = create_engine(connect_str, echo=True, pool_recycle=3600)
db = scoped_session(sessionmaker(bind=engine))


class Commodity(BaseModel):
    __tablename__ = 'commoditys'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(200), unique=True, nullable=False)
    desc = Column(VARCHAR(500), default='no description')
    amount = Column(INTEGER, default=10)
    price = Column(FLOAT, nullable=False)

    def __repr__(self):
        return '<Commodity: %s>' % self.name

    def __price__(self):
        return self.price


class User(BaseModel):
    __tablename__ = 'user'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    username = Column(VARCHAR(50))
    mail = Column(VARCHAR(50))
    password = Column(VARCHAR(60))
    integral = Column(FLOAT, default=1000)
    valid = Column(BOOLEAN(), default=False)
    check_code = Column(VARCHAR(10))
    phone_number = Column(VARCHAR(20))
    permission = Column(INTEGER ,default=0)
    inviter_id = Column(INTEGER, ForeignKey('user.id'))

    def check(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf8'))

    def __repr__(self):
        return '<User: %s>' % self.username

    def pay(self, num):
        res = (self.integral - num) if (self.integral - num) else False
        if res >= 0:
            return res
        else:
            return False

    def __integral__(self):
        return self.integral


class Shopcar(BaseModel):
    __tablename__ = 'shopcar'

    id = Column(INTEGER, primary_key=True, autoincrement=True)


class Ticket(BaseModel):
    __tablename__ = 'ticket'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(140))
    html = Column(VARCHAR(2000))
    markdown = Column(VARCHAR(500))
    sender = Column(INTEGER, ForeignKey("user.id"))

    sender_obj = relationship('User')


class SiteConfig(BaseModel):
    __tablename__ = 'site_config'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(140))
    value = Column(VARCHAR(2000))


if __name__ == "__main__":
    BaseModel.metadata.create_all(engine)
    v = json.dumps({"api_url": os.environ.get('api_url'),
                    "method": "1",
                    "name": "data",
                    "template": '''<root>
    <tel>{tel}</tel>
    <text>【VYG乐购】您的验证码为： {code}</text>
</root>'''})
    db.add(SiteConfig(name='sms_settings', value=v))
    db.add(SiteConfig(name='force_phone_check',value='false'))
    for i in xrange(49):
        name = ''.join(random.sample(string.ascii_letters, 16))
        desc = ''.join(random.sample(string.ascii_letters * 5, 100))
        price = random.randint(10, 200)
        db.add(Commodity(name=name, desc=desc, price=price))
    db.add(Commodity(name='Flag', desc="If you buy it, you can trigger some special function.", price=2048, amount=1))
    # hey, don't worry, only checker know these users! I promise!
    db.add(User(username='AdMIn_for_CH3k3r', mail='gay@it.edu.cn', check_code='6666', phone_number='0', integral=-2333,
                permission=7, valid=True,
                password=bcrypt.hashpw('AdMIn_for_CH3k3r_es7kyJwufk'.encode('utf8'), bcrypt.gensalt())))

    db.add(User(username='ItouMakoto', mail='ItouMakoto@it.edu.cn', check_code='6666', phone_number='0', integral=-2333,
                permission=0, valid=True,
                password='Flag{23333}'))
    db.add(Ticket(title=u'点击获得flag',markdown=u'不存在的2333\n\n别人笑我死得早，我笑别人日的少',
                  html=u'<p>不存在的2333</p><p>别人笑我死得早，我笑别人日的少</p>',sender=2))

    db.commit()
