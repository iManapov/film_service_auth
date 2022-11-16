import json
from hashlib import md5

from rauth import OAuth1Service, OAuth2Service
from flask import current_app, url_for, request, redirect, session


class OAuthSignIn(object):
    """
    Класс для хранения всех поставщиков данных
    """
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        """Функция, отвечающая за перенаправление пользователя на сайт авторизации поставщика"""
        pass

    def callback(self):
        """
        Функция, принимает запрос со стороны сервиса поставщика и обрабатывает полученный код авторизации, обменяв
        его на токен авторизации и с помощью токена происходит обращение к api поставщику за нужными нашему сервису
        данными.
        """
        pass

    def get_callback_url(self):
        """Генерация url ссылки на наш сервис после успешной авторизации пользователя на сервисе поставщика"""
        return url_for('api_v1.callback', provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class YandexSignIn(OAuthSignIn):
    def __init__(self):
        super(YandexSignIn, self).__init__('yandex')
        self.service = OAuth2Service(
            name='yandex',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://oauth.yandex.ru/authorize',
            access_token_url='https://oauth.yandex.ru/token',
            base_url='https://oauth.yandex.ru/'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        def decode_json(payload):
            return json.loads(payload.decode('utf-8'))

        if 'code' not in request.args:
            return None, None, None, None, None, None
        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()},
            decoder=decode_json
        )
        me = oauth_session.get('https://login.yandex.ru/info?format=json').json()
        return (
            me['client_id'],
            'yandex',
            me['login'],
            me['default_email'],
            me['first_name'],
            me['last_name'],
            str(request.user_agent)
        )


class GoogleSignIn(OAuthSignIn):
    def __init__(self):
        super(GoogleSignIn, self).__init__('google')
        self.service = OAuth2Service(
            name='google',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
            access_token_url='https://oauth2.googleapis.com/token',
            base_url='https://accounts.google.com/'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            response_type='code',
            scope='openid email profile',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        def decode_json(payload):
            return json.loads(payload.decode('utf-8'))

        if 'code' not in request.args:
            return None, None, None, None, None, None
        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()},
            decoder=decode_json
        )
        me = oauth_session.get('https://openidconnect.googleapis.com/v1/userinfo').json()
        return (
            me['sub'],
            'google',
            me['email'].split('@')[0],
            me['email'],
            me['given_name'],
            me['family_name'],
            str(request.user_agent)
        )


class VkSignIn(OAuthSignIn):
    def __init__(self):
        super(VkSignIn, self).__init__('vk')
        self.service = OAuth2Service(
            name='vk',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://oauth.vk.com/authorize',
            access_token_url='https://oauth.vk.com/access_token',
            base_url='https://oauth.vk.com/'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            response_type='code',
            scope='4194304',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        def decode_json(payload):
            return json.loads(payload.decode('utf-8'))

        if 'code' not in request.args:
            return None, None, None, None, None, None
        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url(),
                  'v': '5.131'},
            decoder=decode_json
        )
        me = oauth_session.get('https://api.vk.com/method/users.get?v=5.131').json()
        email = json.loads(oauth_session.access_token_response.content.decode("utf-8"))['email']
        return (
            me['response'][0]['id'],
            'vk',
            email.split('@')[0],
            email,
            me['response'][0]['first_name'],
            me['response'][0]['last_name'],
            str(request.user_agent)
         )


class MailSignIn(OAuthSignIn):
    def __init__(self):
        super(MailSignIn, self).__init__('mail')
        self.service = OAuth2Service(
            name='mail',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://connect.mail.ru/oauth/authorize',
            access_token_url='https://connect.mail.ru/oauth/token',
            base_url='https://connect.mail.ru'
        )
        self.private_key = 'e3628e4a124e0e4f9b2ff939a8760219'

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        def decode_json(payload):
            return json.loads(payload.decode('utf-8'))

        if 'code' not in request.args:
            return None, None, None, None, None, None
        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()},

            decoder=decode_json
        )
        access_token = oauth_session.access_token
        x_mailru_vid = json.loads(oauth_session.access_token_response.content.decode("utf-8"))['x_mailru_vid']
        sig_text = x_mailru_vid.encode() + f'app_id={oauth_session.client_id}'.encode() + 'method=users.getInfo'.encode() + \
                   f'session_key={access_token}'.encode() + self.private_key.encode()
        sig = md5(sig_text).hexdigest()
        me = oauth_session.get(f'''http://www.appsmail.ru/platform/api?method=users.getInfo&\
app_id={oauth_session.client_id}&session_key={access_token}&sig={sig}''').json()

        return (
            me[0]['uid'],
            'mail',
            me[0]['nick'],
            me[0]['email'],
            me[0]['first_name'],
            me[0]['last_name'],
            str(request.user_agent)
        )
