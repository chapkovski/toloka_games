# some consntants (like host urls) go here.
REAL_HOST = 'https://toloka.yandex.ru'
SANDBOX_HOST = 'https://sandbox.toloka.yandex.ru'
DEFAULT_ACCEPT_MSG = 'Thank you!'
from renderer import bonus_template

# we obtain api from settings, there they are obtained from env
import json
import requests
from enum import Enum
from pprint import pprint
import os


class CodeStatus(Enum):
    ACCESS_DENIED = 'ACCESS_DENIED'


class objdict(dict):
    """updated dict object to access and set dict properties as obj propperties. Taken from
    here: https://goodcode.io/articles/python-dict-object/"""

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)


# TODO: replacie hardcoded with .env
settings = objdict(SANDBOX_TOLOKA_API=os.getenv('SANDBOX_TOLOKA_API'),
                   TOLOKA_API=os.getenv('TOLOKA_API'), )


class TolokaClient:
    def __init__(self, sandbox):
        self.sandbox = sandbox
        if sandbox:
            self.host = SANDBOX_HOST
            self.api_key = settings.SANDBOX_TOLOKA_API
        else:
            self.host = REAL_HOST
            self.api_key = settings.TOLOKA_API
        print(self.get_balance())

    def assign_skill(self, worker_id, skill_id, value, reason):
        payload = dict(
            skill_id=skill_id,
            user_id=worker_id,
            value=value,
            reason=reason
        )

        url = self.get_user_skills_url()
        method = 'PUT'

        r = self.request_to_toloka(url, method, payload)
        return TolokaResponse(**r)

    def get_skills_url(self):
        return f"{self.host}/api/v1/skills/"

    def get_skills_list(self):
        url = self.get_skills_url()
        method = 'GET'
        r = self.request_to_toloka(url, method)
        return r

    def get_user_skills_url(self):
        return f"{self.host}/api/v1/user-skills/"

    def get_authorization_header(self):
        """Yes, that's the weird way toloka sets authorization header."""
        return dict(Authorization=f'OAuth {self.api_key}')

    def get_headers(self):
        """getting authorization header, and open the possibility to inject other headers later."""
        headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }
        headers.update(self.get_authorization_header())
        return headers

    def get_assignment_url(self, assignment_id):
        """Im not sure we need separate url methods, but if later on toloka changes the urls, it will be easier to
        replace just these methods.
        """
        return f"{self.host}/api/v1/assignments/{assignment_id}"

    def get_bonus_url(self):
        """Im not sure we need separate url methods, but if later on toloka changes the urls, it will be easier to
        replace just these methods.
        """
        return f"{self.host}/api/v1/user-bonuses"

    def get_error_msg(self, resp):
        return dict(error=True,
                    error_status=resp.status_code,
                    error_raw=resp.json())

    def request_to_toloka(self, url, method, payload={}, ):
        headers = self.get_headers()

        if isinstance(payload, dict):
            payload = json.dumps(payload)

        if isinstance(payload, str):
            payload = payload.encode('utf-8')

        response = requests.request(method, url, headers=headers, data=payload)
        # print('HEADERs', headers)
        # print('URL', url)
        # print("STATUS CODE", response.status_code)
        # print("RAW RESP", response.json())
        if 200 <= response.status_code <= 300:
            return response.json()
        else:
            return self.get_error_msg(response)

    def get_assignment_info(self, assignment_id):
        """Using assginment id returns a toloka response object"""
        url = self.get_assignment_url(assignment_id)
        method = 'GET'
        payload = None
        r = self.request_to_toloka(url, method, payload)
        return TolokaResponse(**r)

    def full_url(self, stub):
        return f"{self.host}/api/v1/{stub}"

    def get_balance(self):
        url = self.full_url('requester')
        method = 'GET'
        payload = None
        r = self.request_to_toloka(url, method, payload)
        return TolokaResponse(**r)

    def accept_assignment(self, assignment_id):
        """given assignment id, accept assignment. The method DOES NOT CHECK whether the assignment is in acceptable status.
        for instance it is not in ACTIVE mode. It just stupidly sends accept post. All checking should be done by
        a calling function/instance. Returns toloka response object"""
        url = self.get_assignment_url(assignment_id)
        method = 'PATCH'
        # we can think about customizing acceptance message later, it's not important
        payload = dict(status='ACCEPTED',
                       public_comment=DEFAULT_ACCEPT_MSG)
        # todo: error handnling
        r = self.request_to_toloka(url, method, payload)
        return TolokaResponse(**r)

    def pay_bonus(self, user_id, bonus, title, message):
        """pay bonus in usd. Does not check for anything (nor for existance of user, nor size of bonus, nor amount of
        money available on balance, -just existence of the three params, Returns toloka response object"""
        payload = {
            "user_id": user_id,
            "amount": str(bonus),
            "public_title": {
                "EN": title,
                "RU": title
            },
            "public_message": {
                "EN": message,
                "RU": message
            }
        }

        url = self.get_bonus_url()
        method = 'POST'
        # todo: error handnling
        r = self.request_to_toloka(url, method, payload)
        return TolokaResponse(**r)


class TolokaResponse(objdict):
    """just an objdict. open for some customization"""
    pass
