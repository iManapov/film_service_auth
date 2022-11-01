from gevent import monkey
monkey.patch_all()

from src.app import app
