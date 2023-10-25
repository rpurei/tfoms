#!python
#cython: language_level=3, always_allow_keywords=True
from .db import db_exchsrv


class NSIDistList(db_exchsrv.Model):
    __tablename__ = 'nsi_dictionaries'
    __bind_key__ = 'exchsrv'
    id = db_exchsrv.Column(db_exchsrv.Integer, primary_key=True)
    dict_code = db_exchsrv.Column(db_exchsrv.String(32))
    dict_name = db_exchsrv.Column(db_exchsrv.String(256))
    dict_startdate = db_exchsrv.Column(db_exchsrv.DateTime)
    dict_editiondate = db_exchsrv.Column(db_exchsrv.DateTime)
    dict_versionnumber = db_exchsrv.Column(db_exchsrv.String(16))
    dict_status = db_exchsrv.Column(db_exchsrv.String(64), default='Пустой')
    dict_updatedate = db_exchsrv.Column(db_exchsrv.DateTime)

    def __init__(self, dict_code=None, dict_name=None, dict_startdate=None,
                 dict_editiondate=None, dict_versionnumber=None,
                 dict_status=None, dict_updatedate=None):
        self.dict_code = dict_code
        self.dict_name = dict_name
        self.dict_startdate = dict_startdate
        self.dict_editiondate = dict_editiondate
        self.dict_versionnumber = dict_versionnumber
        self.dict_status = dict_status
        self.dict_updatedate = dict_updatedate
