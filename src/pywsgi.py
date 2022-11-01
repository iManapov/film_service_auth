import os
import sys

from gevent import monkey
monkey.patch_all()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from gevent.pywsgi import WSGIServer
from src.app import app
from src.core.config import settings


http_server = WSGIServer((settings.service_host, settings.service_port), app)
http_server.serve_forever()
