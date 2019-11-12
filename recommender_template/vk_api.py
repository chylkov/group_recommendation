import requests
from urllib.parse import urljoin

def value_to_str(x):
    return ','.join(map(str, x)) if isinstance(x, (list, tuple)) else str(x)

class VKapi:
    API_URL = 'https://api.vk.com/method/'
    VERSION = '5.63'

    def __init__(self, access_token):
        self.token = access_token

    def __get_params_str__(self, params):
        if self.token is None:
            raise Exception('VK access_token should be set')

        params['access_token'] = self.token
        params['v'] = self.VERSION
        return '&'.join('%s=%s' % (k, value_to_str(v)) for k, v in params.items())

    def __create_url_request__(self, method, params):
        return urljoin(self.API_URL, method) + '?' + self.__get_params_str__(params)

    def __get_response__(self, url):
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            return response.json()['response']
        return None

    def get_user_subscriptions(self, user_id):
        url = self.__create_url_request__('users.getSubscriptions', {'user_id': user_id})
        return self.__get_response__(url)

    def get_groups_by_id(self, group_ids, fields=('members_count',)):
        assert len(group_ids) <= 500
        url = self.__create_url_request__('groups.getById', {'group_ids': group_ids, 'fields': fields})
        return self.__get_response__(url)

    def get_user_profile(self, user_ids, fields=('photo_50',)):
        assert len(user_ids) <= 1000
        url = self.__create_url_request__('users.get', {'user_ids': user_ids, 'fields': fields})
        return self.__get_response__(url)


