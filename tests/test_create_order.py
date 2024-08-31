import pytest
import random
import requests
from variables import URL, ORDERS, EMPTY_INGR_HASH


class TestCreateOrder:

    def test_create_order_valid_data_no_auth_order_created(self, create_order_no_auth):
        success = create_order_no_auth.json()['success']
        status_code = create_order_no_auth.status_code
        assert success is True and status_code == 200 and create_order_no_auth.json()['order']['number']

    def test_create_order_valid_data_with_auth_order_created(self, create_order_with_auth):
        response = create_order_with_auth.post_order()
        success = response.json()['success']
        status_code = response.status_code
        assert (success is True and status_code == 200
                and response.json()['order']['number']
                and response.json()['order']['owner'])

    def test_create_order_empty_data_error_no_order_created(self):
        response = requests.post(f'{URL}/{ORDERS}')
        message = response.json()['message']
        success = response.json()['success']
        status_code = response.status_code
        assert status_code == 400 and message == EMPTY_INGR_HASH and success is False

    def test_create_order_invalid_data_server_error(self):
        response = requests.post(f'{URL}/{ORDERS}', data={'ingredients': [str(random.randrange(10))]})
        assert response.status_code == 500
