#coding:utf-8
import tornado.web
from sqlalchemy.orm.exc import NoResultFound
from sshop.base import BaseHandler
from sshop.models import Commodity, User, Ticket
from sshop.settings import limit,on_seckill
import functools
from Shop import check_user_valid

class TicketIndexHandler(BaseHandler):
    @tornado.web.authenticated
    @check_user_valid
    def get(self):
        page = self.get_argument('page', 1)
        page = int(page) if int(page) else 1
        tickets = self.orm.query(Ticket) \
            .filter(Ticket.sender_obj==self.get_current_user_obj())\
            .order_by(Ticket.id.desc()) \
            .limit(limit).offset((page - 1) * limit).all()
        return self.render('tickets.html', tickets=tickets, preview=page - 1, next=page + 1, limit=limit)

class TicketDetailHandler(BaseHandler):
    def get(self,id=1):
        try:
            ticket=self.orm.query(Ticket).filter(Ticket.id==int(id))\
                .filter(Ticket.sender_obj==self.get_current_user_obj()).one()
            return self.render('ticket_detail.html',ticket=ticket)
        except:
            return self.redirect('/tickets')
