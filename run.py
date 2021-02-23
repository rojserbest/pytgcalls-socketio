from server import web, app
from config import HOST, PORT

web.run_app(app, host=HOST, port=PORT)
