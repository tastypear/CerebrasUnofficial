# coding:utf-8
import requests
import json
from datetime import datetime, timedelta, timezone


class CerebrasUnofficial:
    def __init__(self, authjs_session_token: str):
        self.api_url = 'https://api.cerebras.ai'
        self.authjs_session_token = authjs_session_token
        self.key = None
        self.expiry = None
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Cookie': f'authjs.session-token={self.authjs_session_token}',
        })


    def _get_key_from_graphql(self):
        json_data = {
            'operationName': 'GetMyDemoApiKey',
            'variables': {},
            'query': 'query GetMyDemoApiKey {\n  GetMyDemoApiKey\n}',
        }
        response = self.session.post(
            'https://inference.cerebras.ai/api/graphql', json=json_data
        )
        response.raise_for_status()

        data = response.json()
        try:
            if 'data' in data and 'GetMyDemoApiKey' in data['data']:
                self.key = data['data']['GetMyDemoApiKey']
        except Exception:
            raise Exception('Maybe your authjs.session-token is invalid.')


    def _get_expiry_from_session(self):
        response = self.session.get('https://cloud.cerebras.ai/api/auth/session')
        response.raise_for_status()
        data = response.json()
        if 'user' in data and 'demoApiKeyExpiry' in data['user']:
            self.expiry = datetime.fromisoformat(
                data['user']['demoApiKeyExpiry'].replace('Z', '+00:00')
            )


    def get_api_key(self) -> str:
        if self.key is None:
            self._get_key_from_graphql()
        else:
            if self.expiry is None:
                self._get_expiry_from_session()
            if datetime.now(timezone.utc) >= self.expiry:
                self._get_key_from_graphql()
                self.expiry = datetime.now(timezone.utc) + timedelta(minutes=10)

        return self.key
