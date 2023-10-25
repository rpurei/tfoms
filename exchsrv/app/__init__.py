# !python
# cython: language_level=3, always_allow_keywords=True
from .models.db import db_exchsrv
from .models.applogging import SQLAlchemyHandler
from .models.files import FileProcessing
from .models.transactions import TransActions
from .models.nsi import NSIDistList
from .config import (APP_PORT, APP_HOST, MAX_BYTES, BACKUP_COUNT,
                     LOG_FORMAT, LOG_FILE, SQLALCHEMY_BINDS, UPLOAD_FOLDER)
from .views import views_handler
from .views.transactions import trans_handler
from .views.opt import opt_handler
from .views.users import login_manager, users_handler
from .views.protocols import protocols_handler
from .views.files import files_handler
from .auth.model import User
from .config import TRANS_IN_FOLDER, TRANS_OUT_FOLDER
from .tasks.service import crontab
from flask import Flask, current_app
import logging
from logging.handlers import RotatingFileHandler
from sqlalchemy_utils import database_exists, create_database
from pathlib import Path


log_format = logging.Formatter(LOG_FORMAT)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_format)
stream_handler.setLevel(logging.INFO)
info_handler = RotatingFileHandler(LOG_FILE, mode='a', maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
info_handler.setFormatter(log_format)
info_handler.setLevel(logging.INFO)
dblog_handler = SQLAlchemyHandler()
dblog_handler.setFormatter(log_format)
dblog_handler.setLevel(logging.INFO)

for item in SQLALCHEMY_BINDS.items():
    if not database_exists(item[1]):
        create_database(item[1])


def create_dirs():
    Path('logs').mkdir(exist_ok=True)
    cronlog = Path('logs/cron.log')
    cronlog.touch(exist_ok=True)
    Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
    Path(TRANS_IN_FOLDER).mkdir(parents=True, exist_ok=True)
    Path(TRANS_OUT_FOLDER).mkdir(parents=True, exist_ok=True)


def create_app():
    app = None
    try:
        app = Flask(__name__)
        app.logger.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
        app.logger.addHandler(info_handler)
        app.logger.addHandler(dblog_handler)
        app.app_context().push()
        app.config.from_pyfile('config.py')
        db_exchsrv.init_app(app)
        crontab.init_app(app)
        login_manager.init_app(app)
        db_exchsrv.create_all(bind='exchsrv', app=current_app)
        app.register_blueprint(views_handler)
        app.register_blueprint(trans_handler)
        app.register_blueprint(opt_handler)
        app.register_blueprint(users_handler)
        app.register_blueprint(protocols_handler)
        app.register_blueprint(files_handler)
        create_dirs()
        return app
    except Exception as err:
        app.logger.critical(str(err))
