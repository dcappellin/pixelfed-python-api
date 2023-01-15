import os
import requests


class Pixelfed:

    def __init__(self, pixelfed_domain_uri=None) -> None:
        self.domain = os.environ["PIXELFED_DOMAIN_URI"] if pixelfed_domain_uri is None else \
            pixelfed_domain_uri
        headers = {
            'Authorization': f"Bearer {os.environ['PIXELFED_API_TOKEN']}",
            'Accept': 'application/json',
        }
        self.client = requests.Request(url=self.domain, headers=headers).prepare()

    @staticmethod
    def _get(func):
        def inner(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.client.method = 'GET'
            resp = requests.Session().send(self.client)
            resp.raise_for_status()
            return resp.json()
        return inner

    @staticmethod
    def _post(func):
        def inner(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.client.method = 'POST'
            resp = requests.Session().send(self.client)
            resp.raise_for_status()
            return resp.json()
        return inner

    @_post
    def _status_post(self, status, media_ids=None, visibility='unlisted'):
        data = {
            'media_ids': media_ids,
            'status': status,
            'visibility': visibility
        }
        self.client.prepare_body(data=None, files=None, json=data)

    @_get
    def _status(self, status_id):
        self.client.url += f'/{status_id}'

    @_get
    def instance(self):
        self.client.url += 'api/v1/instance'

    @_post
    def media(self, image_filename):
        self.client.url += 'api/v1/media'
        files = [('file', (image_filename, open(image_filename, 'rb'), 'image/jpg'))]
        self.client.prepare_body(data=None, files=files)

    def statuses(self, status_id=None, status=None, media_ids=None, visibility='unlisted'):
        self.client.url += 'api/v1/statuses'
        if status_id is not None:
            return self._status(status_id)
        else:
            return self._status_post(status, media_ids, visibility)
