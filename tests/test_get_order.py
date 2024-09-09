import allure
import requests
from variables import NO_AUTH, URL, ORDERS


class TestGetOrder:

    @allure.testcase('Get order from authorized user')
    def test_get_order_with_auth_get_order(self, create_order_with_auth, create_user):
        create_order_with_auth.post_order()
        create_order_with_auth.post_order()

        token = create_user['response'].json()['accessToken']
        with allure.step(f'Get order (GET request) for user {create_user['response'].json()['user']}'):
            response = requests.get(f'{URL}/{ORDERS}', headers={'Authorization': token})

        orders_num = len(response.json()['orders'])
        success = response.json()['success']
        status_code = response.status_code

        assert orders_num == 2 and status_code == 200 and success is True

    @allure.testcase('Get order without authorization')
    def test_get_order_no_auth_error_need_auth(self):
        with allure.step(f'Get order (GET request) without user data'):
            response = requests.get(f'{URL}/{ORDERS}')

        success = response.json()['success']
        message = response.json()['message']
        status_code = response.status_code

        assert message == NO_AUTH and status_code == 401 and success is False
