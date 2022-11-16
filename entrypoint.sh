#!/bin/sh
cd /opt/app/src
flask db upgrade
gunicorn wsgi_app:app --workers 4 --worker-class gevent --bind 0.0.0.0:5001