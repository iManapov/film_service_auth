import json
from hashlib import md5

from rauth import OAuth2Service
from flask import current_app, url_for, request, redirect

from src.core.config import yandex, vk, google, mail, Providers


class OAuthSignIn:
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


def decode_json(payload):
    return json.loads(payload.decode('utf-8'))


def get_oauth_session(provider: OAuthSignIn, service, **kwargs):
    if 'code' not in request.args:
        return None, None, None, None, None, None
    data = {
        'code': request.args['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': provider.get_callback_url(),
    }
    data.update(**kwargs)
    oauth_session = service.get_auth_session(
        data=data,
        decoder=decode_json
    )
    return oauth_session


class YandexSignIn(OAuthSignIn):
    def __init__(self):
        super(YandexSignIn, self).__init__('yandex')
        self.service = OAuth2Service(
            name=Providers.yandex.name,
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url=yandex.authorize_url,
            access_token_url=yandex.access_token_url,
            base_url=yandex.base_url
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        oauth_session = get_oauth_session(self, self.service)
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
            name=Providers.google.name,
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url=google.authorize_url,
            access_token_url=google.access_token_url,
            base_url=google.base_url
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            response_type='code',
            scope='openid email profile',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        oauth_session = get_oauth_session(self, self.service)
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
            name=Providers.vk.name,
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url=vk.authorize_url,
            access_token_url=vk.access_token_url,
            base_url=vk.base_url
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            response_type='code',
            scope='4194304',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        oauth_session = get_oauth_session(self, self.service, v='5.131')

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
            name=Providers.mail.name,
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url=mail.authorize_url,
            access_token_url=mail.access_token_url,
            base_url=mail.base_url
        )
        self.private_key = mail.private_key

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        oauth_session = get_oauth_session(self, self.service)
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
