import requests
import logging
from gevent import sleep, spawn

client = None
logger = logging.getLogger(__name__)
logging.getLogger('requests').setLevel(logging.WARNING)


class UnexpectedCode(Exception):
    def __init__(self, code, msg):
        super(Exception, self).__init__("unexpected response code: %s, %s" % (code, msg))
        self.msg = msg
        self.code = code


class LarkAuth(requests.auth.AuthBase):
    def __init__(self):
        self.token = None
        self.token_expire = 0

    def __call__(self, request):
        request.headers['Authorization'] = 'Bearer ' + self.token
        return request


class LarkClient(requests.Session):
    def __init__(self, config):
        super(LarkClient, self).__init__()
        self.app_id = config['app_id']
        self.app_secret = config['app_secret']
        self.endpoint = config.get('endpoint', 'https://open.feishu.cn/open-apis')
        self.auth_data = {"app_id": config['app_id'], "app_secret": config['app_secret']}

        auth = LarkAuth()
        auth.token, auth.token_expire = self.get_token()
        self.auth = auth
        spawn(self._renew_token, auth)

    def redirect_uri(self, url, state=None):
        return '%s/authen/v1/index?redirect_uri=%s&app_id=%s&state=%s' % (self.endpoint, url, self.app_id, state)

    def get_token(self):
        r = self.post(self.endpoint + '/auth/v3/tenant_access_token/internal/', json=self.auth_data)
        if r.status_code != 200:
            r.raise_for_status()
        data = self._read_data(r)
        return data['tenant_access_token'], data['expire']

    def _read_data(self, r):
        if r.status_code != 200:
            r.raise_for_status()
        data = r.json()
        if data['code'] != 0:
            raise UnexpectedCode(data['code'], data['msg'])
        return data

    def _ensure_success(self, data):
        if data['code'] != 0:
            raise ValueError("response return non-zero code: %s, %s" % (data['code'], data['msg']))

    def _renew_token(self, auth):
        retry_interval = 3
        logger.info('start renew auth token')
        while True:
            if auth.token_expire and auth.token_expire > 120:
                sleep(auth.token_expire - 120)
            else:
                sleep(auth.token_expire / 3)

            try:
                auth.token, auth.token_expire = self.get_token()
            except:
                logger.error("unable to renew token,retry after %s seconds", retry_interval, exc_info=True)
                sleep(retry_interval)

    def send_text_message(self, content, root_id=None, chat_id=None, user_id=None, open_id=None, email=None):
        data = {
            "content": {
                "text": content
            },
            "msg_type": "text",
        }
        if root_id:
            data['root_id'] = root_id
        if open_id:
            data['open_id'] = open_id
        elif user_id:
            data['user_id'] = user_id
        elif chat_id:
            data['chat_id'] = chat_id
        elif email:
            data['email'] = email
        r = self.post(self.endpoint + '/message/v4/send/', json=data)
        self._read_data(r)

    def send_card_message(self, card, root_id=None, chat_id=None, user_id=None, open_id=None, email=None, update_multi=True):
        data = {
            "msg_type": "interactive",
            "card": card,
            "update_multi": update_multi
        }

        if root_id:
            data['root_id'] = root_id
        if open_id:
            data['open_id'] = open_id
        elif user_id:
            data['user_id'] = user_id
        elif chat_id:
            data['chat_id'] = chat_id
        elif email:
            data['email'] = email

        r = self.post(self.endpoint + '/message/v4/send/', json=data)
        self._read_data(r)

    def get_roles(self):
        r = self.get(self.endpoint + '/contact/v2/role/list')
        data = self._read_data(r)
        return data['data']['role_list']

    def get_chat_info(self, chat_id):
        r = self.get(self.endpoint + '/chat/v4/info', params={'chat_id': chat_id})
        return self._read_data(r)['data']

    def get_department_info(self, department_id):
        r = self.get(self.endpoint + '/contact/v1/department/info/get', params={"department_id": department_id})
        return self._read_data(r)['data']

    def get_department_user_infos(self, department_id, offset=0, fetch_child=False, page_size=50):
        params = {
            "offset": offset,
            "page_size": page_size,
            "fetch_child": fetch_child,
            "department_id": department_id
        }
        r = self.get(self.endpoint + '/contact/v1/department/user/detail/list', params=params)
        return self._read_data(r)['data']

    def get_users_by(self, emails=[], mobiles=[]):
        r = self.get(self.endpoint + '/user/v1/batch_get_id?', params={"emails": emails, "mobiles": mobiles})
        return self._read_data(r)['data']

    def get_auth_user(self, code):
        r = self.post(self.endpoint + '/authen/v1/access_token', json={
            'app_access_token': self.auth.token
            , 'grant_type': 'authorization_code'
            , 'code': code
        })
        return self._read_data(r)['data']

    def get_mina_auth_user(self, code):
        r = self.post(self.endpoint + '/mina/v2/tokenLoginValidate', json={
            'token': self.auth.token
            , 'code': code
        })
        return self._read_data(r)['data']

    def get_users_info(self, open_ids=[], employee_ids=[]):
        params = {}
        if open_ids and len(open_ids):
            params['open_ids'] = open_ids
        elif employee_ids and len(employee_ids):
            params['employee_ids'] = employee_ids
        r = self.get(self.endpoint + '/contact/v1/user/batch_get?', params=params)
        return self._read_data(r)['data']['user_infos']

    def get_contact_scope(self):
        r = self.get(self.endpoint + '/contact/v1/scope/get')
        return self._read_data(r)['data']


if __name__ == '__main__':
    import sys

    config = {
        'app_id': sys.argv[1],
        'app_secret': sys.argv[2]
    }
    client = LarkClient(config)
    client.send_text_message('hello', open_id=sys.argv[3])
