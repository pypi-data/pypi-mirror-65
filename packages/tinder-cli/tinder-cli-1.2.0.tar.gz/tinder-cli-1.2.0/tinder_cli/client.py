import re
import json
import os.path

import requests


class TinderClient(object):
    API_BASE_URL = "https://api.gotinder.com"
    REQ_HEADERS = {'user-agent': 'Tinder/11.4.0 (iPhone; iOS 12.4.1; Scale/2.00)', 'content-type': 'application/json'}

    @classmethod
    def get_session(cls, tinder_token: str = None) -> (requests.Session):
        session = requests.Session()
        session.headers.update({**cls.REQ_HEADERS, 'X-Auth-Token': tinder_token})
        return session

    @classmethod
    def get_profile(cls, session: requests.Session, **kwargs) -> requests.Response:
        return session.get(cls.API_BASE_URL + '/profile', **kwargs)

    @classmethod
    def get_meta(cls, session: requests.Session, **kwargs) -> requests.Response:
        return session.get(cls.API_BASE_URL + '/v2/meta', **kwargs)

    @classmethod
    def get_recommendations(cls, session: requests.Session, **kwargs) -> requests.Response:
        return session.get(cls.API_BASE_URL + '/v2/recs/core', **kwargs)

    @classmethod
    def get_user(cls, session: requests.Session, user_id: str, **kwargs) -> requests.Response:
        return session.get(cls.API_BASE_URL + '/user/{}'.format(user_id), **kwargs)

    @classmethod
    def like_user(cls, session: requests.Session, user_id: str, **kwargs) -> requests.Response:
        return session.get(cls.API_BASE_URL + '/like/{}'.format(user_id), **kwargs)

    @classmethod
    def superlike_user(cls, session: requests.Session, user_id: str, **kwargs) -> requests.Response:
        return session.post(cls.API_BASE_URL + '/like/{}/super'.format(user_id), **kwargs)

    @classmethod
    def pass_user(cls, session: requests.Session, user_id: str, **kwargs) -> requests.Response:
        return session.get(cls.API_BASE_URL + '/pass/{}'.format(user_id), **kwargs)

    @classmethod
    def get_teasers(cls, session: requests.Session, **kwargs) -> requests.Response:
        return session.get(cls.API_BASE_URL + '/v2/fast-match/teasers', **kwargs)
