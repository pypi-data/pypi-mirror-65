"""Base REST performer"""

import base64
import json
from urllib.parse import urlparse

import requests

from .performer import Performer


class restAPI(Performer):
    def __init__(self, api_info):
        super().__init__()
        self.url = self._resolve_url(api_info)
        self.auth_method = self._resolve_auth_method(api_info.get('auth', None))
        self.headers = self._resolve_headers(api_info)

    def _resolve_url(self, api_info):
        """Check the URL"""
        url = api_info.get('url', None)
        if url:
            try:
                check = urlparse(url)
                if all([check.scheme, check.netloc, check.path]):
                    return url
                else:
                    raise ValueError("URL could not parse components - scheme: %s, netlock: %s, path:%s" % (check.scheme, check.netloc, check.path))
            except Exception:
                raise ValueError("URL failed url check using urlparse: %s" % url)
        else:
            raise ValueError("Must provide a value for URL when creating a restAPI class")

    def _resolve_auth_method(self, auth):
        """Resolves the authentication method by 'duck typing' the parameters provided or raise error"""
        # if isinstance(auth, type({})):
        #    raise TypeError("Auth must be dictionary. provided: %s, type: %s" % (auth, type(auth)))
        user = auth.get('user', None)
        password = auth.get('password', None)
        token = auth.get('token', None)
        bearer = auth.get('bearer', None)
        if password is not None and user is None:
            raise ValueError("Must provide user if providing password for auth")
        if user is None and token is None:
            return None
        if bearer:
            return "bearer"
        if token:
            return "token"
        if user and password:
            return "userpass"
        if user:
            return "user"

    def _resolve_headers(self, api_info):
        """Manage the headers that will be used on requests"""
        headers = api_info.get('headers', {})
        if headers.get('Content-Type') is None:
            headers["Content-Type"] = "application/json"
        if headers.get('Authorization') is None:
            if self.auth_method == "bearer":
                headers["Authorization"] = "Bearer %s" % (api_info['auth']['bearer'].strip("Bearer").strip())
            if self.auth_method == "token":
                creds = "%s:%s" % (api_info['auth']['user'], api_info['auth']['token'].strip("Basic").strip())
                encoded = base64.b64encode(creds.encode())
                headers["Authorization"] = "Basic %s" % encoded.decode()
            elif self.auth_method == "userpass":
                creds = "%s:%s" % (api_info['auth']['user'], api_info['auth']['password'])
                encoded = base64.b64encode(creds.encode())
                headers["Authorization"] = "Basic %s" % encoded.decode()
        return headers

    def perform_get(self, args):
        path = args.get('path')
        data = args.get('data', {})
        if path:
            target = "%s/%s" % (self.url, path.format(**args))
            print("GET %s %s" % (self.headers, target))
            r = requests.get(target, headers=self.headers, params=data)
            self._check_request(r)
            return r

    def perform_post(self, args):
        path = args.get('path')
        data = args.get('data', {})
        if path:
            target = "%s/%s" % (self.url, path.format(**args))
            print("POST %s with data: %s" % (target, data))
            r = self._resolve_response(requests.post(target, data=json.dumps(data), headers=self.headers))
            return r

    def _resolve_response(self, r):
        try:
            r.raise_for_status()
        except Exception:
            return r

    def _check_request(self, r):
        try:
            r.raise_for_status()
        except Exception:
            print(r.text)

    def _pprint_json(self, j, dl=4, sort_keys=False):
        print(str(json.dumps(j, separators=(',', ':'), sort_keys=sort_keys, indent=2)))
