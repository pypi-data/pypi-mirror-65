import requests
from flask import Response


class HttpClient:
    client = None


class AbstractApp(HttpClient):
    headers = {'Content-type': 'application/json'}

    def post(self, url, data=dict()):
        return self.client.post(url, json=data, headers=self.headers)

    def get(self, url, data=dict()):
        return self.client.get(url, json=data, headers=self.headers)

    def register(self, username, email, password, confirm):
        return self.post('/register', data=dict(username=username, email=email, password=password, confirm=confirm))

    def login(self, username, password):
        return self.post('/login', data=dict(username=username, password=password))

    def logout(self):
        return self.post('/logout')

    def delete(self, user_id, password):
        return self.post('/user/delete', data=dict(user_id=user_id, password=password))


class LocalApp(AbstractApp):
    from app import create_app
    app = create_app('testing')
    client = app.test_client()


class RemoteApp(AbstractApp):
    client = requests
    base_url = 'http://10.9.14.101:8000'

    def post(self, url, data=dict()):
        res = super().post(self.base_url + url, data)
        return self.convert_to_flask_response(res)

    def get(self, url, data=dict()):
        res = super().get(self.base_url + url, data)
        return self.convert_to_flask_response(res)

    # TODO transfer headers
    @staticmethod
    def convert_to_flask_response(response):
        res = Response(
            response=response.text,
            status=response.status_code,
            mimetype=response.headers['content-type']
        )

        return res
