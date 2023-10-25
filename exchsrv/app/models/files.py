#!python
#cython: language_level=3, always_allow_keywords=True
from .db import db_exchsrv
from sqlalchemy.sql import func


class FileProcessing(db_exchsrv.Model):
    __tablename__ = 'file_processing'
    __bind_key__ = 'exchsrv'
    id = db_exchsrv.Column(db_exchsrv.Integer, primary_key=True)
    trans_id = db_exchsrv.Column(db_exchsrv.String(32))
    file_name = db_exchsrv.Column(db_exchsrv.String(256))
    file_size = db_exchsrv.Column(db_exchsrv.Integer)
    file_create = db_exchsrv.Column(db_exchsrv.DateTime)
    file_status = db_exchsrv.Column(db_exchsrv.String(64))
    log = db_exchsrv.Column(db_exchsrv.UnicodeText)
    date_processing = db_exchsrv.Column(db_exchsrv.DateTime,
                                        default=func.now())
    file_flags = db_exchsrv.Column(db_exchsrv.String(2048))

    def __init__(self, trans_id,
                 file_name, file_size, file_create, file_status=None,
                 log=None, file_flags=None):
        self.trans_id = trans_id
        self.file_name = file_name
        self.file_size = file_size
        self.file_create = file_create
        self.file_status = file_status
        self.log = log
        self.file_flags = file_flags
