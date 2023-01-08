import os

import pytest
import requests.exceptions
from dotenv import load_dotenv

from src.pixelfed_python_api import Pixelfed


class TestPixelfed:
    def test_instance(self):
        load_dotenv('prod.env')
        pfi = Pixelfed().instance()
        assert pfi is not None
        with pytest.raises(KeyError):
            pfi['error']

    def test_instance_with_server_uri(self):
        load_dotenv('prod.env')
        os.environ.pop('PIXELFED_DOMAIN_URI')
        pfi = Pixelfed('https://pixelfed.uno').instance()
        assert pfi is not None

    def test_instance_with_wrong_server_uri(self):
        load_dotenv('prod.env')
        os.environ.pop('PIXELFED_DOMAIN_URI')
        with pytest.raises(requests.exceptions.RequestException):
            pfi = Pixelfed('https://pixelfed.due').instance()

    def test_instance_noenv(self):
        load_dotenv('prod.env')
        os.environ.pop('PIXELFED_DOMAIN_URI')
        with pytest.raises(KeyError):
            pfi = Pixelfed().instance()

    def test_instance_notoken(self):
        load_dotenv('prod.env')
        os.environ.pop('PIXELFED_API_TOKEN')
        with pytest.raises(KeyError):
            pfi = Pixelfed().instance()

    def test_get_status(self):
        status_id = '508736992114141332'
        load_dotenv('prod.env')
        pfi = Pixelfed().statuses(status_id=status_id)
        assert pfi['id'] == status_id
        assert pfi is not None
        with pytest.raises(KeyError):
            pfi['error']