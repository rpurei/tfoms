#!python
#cython: language_level=3, always_allow_keywords=True
from .db import db_exchsrv
from sqlalchemy.sql import func
from logging import Handler
from traceback import format_exc


class Log(db_exchsrv.Model):
    __tablename__ = 'logs'
    __bind_key__ = 'exchsrv'
    id = db_exchsrv.Column(db_exchsrv.Integer, primary_key=True)
    logger = db_exchsrv.Column(db_exchsrv.String(32))
    level = db_exchsrv.Column(db_exchsrv.String(16))
    trace = db_exchsrv.Column(db_exchsrv.String(2048))
    msg = db_exchsrv.Column(db_exchsrv.UnicodeText)
    created_at = db_exchsrv.Column(db_exchsrv.DateTime, default=func.now())

    def __init__(self, logger=None, level=None, trace=None, msg=None):
        self.logger = logger
        self.level = level
        self.trace = trace
        self.msg = msg

    def __unicode__(self):
        return self.__repr__()

    def __repr__(self):
        return "<Log: %s - %s>" % (self.created_at.strftime('%m/%d/%Y-%H:%M:%S'), self.msg[:50])


class SQLAlchemyHandler(Handler):
    def emit(self, record):
        trace = None
        exc = record.__dict__['exc_info']
        if exc:
            trace = format_exc()
        log = Log(
            logger=record.__dict__['name'],
            level=record.__dict__['levelname'],
            trace=trace,
            msg=record.__dict__['msg'],)
        db_exchsrv.session.add(log)
        db_exchsrv.session.commit()
