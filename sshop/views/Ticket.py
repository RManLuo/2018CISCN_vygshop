#coding:utf-8
import tornado.web
from sqlalchemy.orm.exc import NoResultFound
from sshop.base import BaseHandler
from sshop.models import Commodity, User, Ticket
from sshop.settings import limit,on_seckill
from tools import import_args
from Shop import check_user_valid
import bleach,markdown

class TicketIndexHandler(BaseHandler):
    @tornado.web.authenticated
    @check_user_valid
    def get(self,*args,**kwargs):
        page = self.get_argument('page', 1)
        page = int(page) if int(page) else 1
        if self.is_admin():
            rule= True
        else:
            rule = (Ticket.sender_obj == self.get_current_user_obj())
        tickets = self.orm.query(Ticket) \
            .filter(rule)\
            .order_by(Ticket.id.desc()) \
            .limit(limit).offset((page - 1) * limit).all()
        return self.render('tickets.html', tickets=tickets, preview=page - 1, next=page + 1, limit=limit)

class TicketDetailHandler(BaseHandler):
    @tornado.web.authenticated
    @check_user_valid
    def get(self,id=1,*args,**kwargs):
        try:
            ticket=self.orm.query(Ticket).filter(Ticket.id==int(id)).one()
            if (not self.is_admin()) and ticket.sender_obj!=self.get_current_user_obj():
                raise Exception
            return self.render('ticket_detail.html',ticket=ticket)
        except:
            return self.redirect('/tickets')

class TicketCreateHandler(BaseHandler):
    @tornado.web.authenticated
    @check_user_valid
    def get(self,*args,**kwargs):
        return self.render('ticket_create.html')

    @tornado.web.authenticated
    @check_user_valid
    def post(self,*args,**kwargs):
        title = self.get_argument('title')
        markdown_input = self.get_argument('wmd-input')
        sender = self.get_current_user_obj().id
        markdown_input_bleach = bleach.linkify(bleach.clean(markdown_input, strip=True))
        self.orm.add(Ticket(title=title, markdown=markdown_input, sender=sender, html=markdown.markdown(markdown_input_bleach)))
        self.orm.commit()
        return self.redirect('/tickets')