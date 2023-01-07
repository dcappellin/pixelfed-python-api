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
        def inner(self):
            func(self)
            self.client.method = 'GET'
            return requests.Session().send(self.client).json()
        return inner

    @staticmethod
    def _post(func):
        def inner(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.client.method = 'POST'
            return requests.Session().send(self.client).json()
        return inner

    @_get
    def instance(self):
        self.client.url += 'api/v1/instance'
        print(self.client)

    @_post
    def media(self, image_filename):
        self.client.url.append('api/v1/media')
        files = [('file', (image_filename, open(image_filename, 'rb'), 'image/jpg'))]
        self.client.prepare_body(data=None, files=files)

    @_post
    def statuses(self, status, media_ids=None, visibility='unlisted'):
        self.client.url.append('api/v1/statuses')
        data = {
            'media_ids': media_ids,
            'status': status,
            'visibility': visibility
        }
        self.client.prepare_body(data=None, files=None, json=data)
