from pathlib import Path
Path('logs').mkdir(exist_ok=True)
from app import create_app
from app.config import APP_HOST, APP_PORT


try:
    app = create_app()
    app.run(host=APP_HOST, port=APP_PORT, debug=True)
    app.app_context().push()
except Exception as err:
    exit(-1)
