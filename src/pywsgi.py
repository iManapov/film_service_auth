from gevent import monkey
monkey.patch_all()

from gevent.pywsgi import WSGIServer
from src.app import app
from src.core.config import settings


http_server = WSGIServer((settings.service_host, settings.service_port), app)
http_server.serve_forever()
