#!python
#cython: language_level=3, always_allow_keywords=True
from .db import db_exchsrv
from sqlalchemy.sql import func


class TransActions(db_exchsrv.Model):
    __tablename__ = 'transactions'
    __bind_key__ = 'exchsrv'
    id = db_exchsrv.Column(db_exchsrv.Integer, primary_key=True)
    trans_id = db_exchsrv.Column(db_exchsrv.String(32))
    trans_status = db_exchsrv.Column(db_exchsrv.String(1024))
    trans_date = db_exchsrv.Column(db_exchsrv.DateTime, default=func.now())
    token = db_exchsrv.Column(db_exchsrv.String(256))
    token_date = db_exchsrv.Column(db_exchsrv.DateTime)
    in_data = db_exchsrv.Column(db_exchsrv.UnicodeText)
    out_data = db_exchsrv.Column(db_exchsrv.UnicodeText)
    protocol_id = db_exchsrv.Column(db_exchsrv.String(16))
    note = db_exchsrv.Column(db_exchsrv.String(2048))
    trans_protocol = db_exchsrv.Column(db_exchsrv.String(256))
    user_name = db_exchsrv.Column(db_exchsrv.String(256))
    trans_addr = db_exchsrv.Column(db_exchsrv.String(16))
    trans_parent = db_exchsrv.Column(db_exchsrv.String(32))

    def __init__(self, trans_id=None, trans_status=None, in_data=None,
                 note=None, user=None, addr=None, trans_parent=None):
        self.trans_id = trans_id
        self.trans_status = trans_status
        self.in_data = in_data
        self.note = note
        self.user_name = user
        self.trans_addr = addr
        self.trans_parent = trans_parent


class TransActionsLog(db_exchsrv.Model):
    __tablename__ = 'transactions_logs'
    __bind_key__ = 'exchsrv'
    id = db_exchsrv.Column(db_exchsrv.Integer, primary_key=True)
    trans_id = db_exchsrv.Column(db_exchsrv.String(32))
    trans_date = db_exchsrv.Column(db_exchsrv.DateTime, default=func.now())
    log = db_exchsrv.Column(db_exchsrv.UnicodeText)

    def __init__(self, trans_id=None, log=None):
        self.trans_id = trans_id
        self.log = log
