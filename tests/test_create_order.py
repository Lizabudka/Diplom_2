import allure
import random
import requests
from variables import URL, ORDERS, EMPTY_INGR_HASH


class TestCreateOrder:

    @allure.testcase('Create new order without authorization and with valid data')
    def test_create_order_valid_data_no_auth_order_created(self, create_order_no_auth):
        success = create_order_no_auth.json()['success']
        status_code = create_order_no_auth.status_code
        assert success is True and status_code == 200 and create_order_no_auth.json()['order']['number']

    @allure.testcase('Create new order with authorization and valid data')
    def test_create_order_valid_data_with_auth_order_created(self, create_order_with_auth):
        response = create_order_with_auth.post_order()
        success = response.json()['success']
        status_code = response.status_code
        assert (success is True and status_code == 200
                and response.json()['order']['number']
                and response.json()['order']['owner'])

    @allure.testcase('Create new order with empty data')
    def test_create_order_empty_data_error_no_order_created(self):
        with allure.step('Create new order with invalid data: POST request'):
            response = requests.post(f'{URL}/{ORDERS}')
        message = response.json()['message']
        success = response.json()['success']
        status_code = response.status_code
        assert status_code == 400 and message == EMPTY_INGR_HASH and success is False

    @allure.testcase('Create new order with invalid data')
    def test_create_order_invalid_data_server_error(self):
        wrong_hash = str(random.randrange(10))
        with allure.step(f'Create new order with non-existent hash: {wrong_hash}'):
            response = requests.post(f'{URL}/{ORDERS}', data={'ingredients': [wrong_hash]})
        assert response.status_code == 500
