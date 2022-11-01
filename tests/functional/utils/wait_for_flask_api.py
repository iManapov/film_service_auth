import requests
import os
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from settings import test_settings


if __name__ == '__main__':
    url = test_settings.service_url + '/api/v1/signup'
    body = {
        "login": "testLogin234",
        "password": "testPsw42d",
        "email": "test@mail2.ru423",
        "first_name": "Ilnar2423",
        "last_name": "Mdtsfcs2423"
    }
    while True:
        try:
            response = requests.post(url, json=body)
            status = response.status_code
            if status < 500:
                break
        except requests.exceptions.ConnectionError:
            time.sleep(5)
