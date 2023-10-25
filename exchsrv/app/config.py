APP_PORT = 80
APP_HOST = '0.0.0.0'
APP_VER = 'Сервис обмена с ТФОМС. v0.1'
TESTING = True
DEBUG = True
ENV = 'development'

LOCAL_DATABASE_URI = 'mysql+pymysql://root:ChangeMe2023@db/exchsrv'
SQLALCHEMY_BINDS = {
    'exchsrv': LOCAL_DATABASE_URI,
}

UPLOAD_FOLDER = r'app/uploads'
TRANS_OUT_FOLDER = r'app/transactions/out'
TRANS_IN_FOLDER = r'app/transactions/in'

ALLOWED_EXTENSIONS = {'xml', 'pdf', 'zip'}
SECRET_KEY = '724a91f4f0f1ccc2adcc49d724460328050cbc8af9a1155087a86fc5ec856f90'
SQLALCHEMY_TRACK_MODIFICATIONS = False

MAX_BYTES = 10000000
BACKUP_COUNT = 9
LOG_FORMAT = '%(asctime)s [%(levelname)s] %(name)s : (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'
LOG_FILE = 'logs/exchsrv.log'

DEFAULT_ADMIN_LOGIN = 'admin'
DEFAULT_ADMIN_PASSWORD = 'admin'
DEFAULT_ADMIN_EMAIL = 'admin@test.com'
DEFAULT_ADMIN_NAME = 'Администратор'

ROWS_PER_PAGE = 25
SEND_FILES = 2

TFOMS_LOGIN = '[Логин пользователя ТФОМС]'
TFOMS_PASSWORD = '[Пароль пользователя ТФОМС]'
TFOMS_UNID = '[ID организации в ТФОМС]'
