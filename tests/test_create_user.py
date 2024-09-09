import allure
import requests
import pytest
from variables import (URL, AUTH_REGISTER, EMAIL_PASS_NAME_EMPTY, USER_EXISTS, test_email, test_password,
                       test_name)


class TestCreateUser:

    @allure.testcase('Create user with valid data')
    def test_create_user_valid_data_user_is_created(self, create_user):
        response = create_user['response']
        assert response.status_code == 200 and response.json()['success'] is True

    @allure.testcase('Create the same user with valid data twice')
    def test_create_same_user_twice_user_already_exists(self, create_user):
        response = create_user['response']
        name = response.json()['user']['name']
        email = response.json()['user']['email']

        with allure.step(f'Creating the same user again with data: {email} (email), {name} (name)'):
            response_2 = requests.post(f'{URL}/{AUTH_REGISTER}', data={'email': email,
                                                                       'name': name,
                                                                       'password': test_password})
        message = response_2.json()['message']
        success = response_2.json()['success']
        status_code = response_2.status_code
        assert success is False and message == USER_EXISTS and status_code == 403

    @allure.testcase('Create user with empty data')
    @pytest.mark.parametrize('email, password, name', [[test_email, '', test_name],
                                                       ['', test_password, test_name],
                                                       [test_email, test_password, '']])
    def test_create_user_empty_data_error_need_required_fields(self, email, password, name):
        with allure.step(f'Create user with data: email "{test_email}", '
                         f'password "{test_password}", name "{test_name}"'):
            response = requests.post(f'{URL}/{AUTH_REGISTER}', data={'email': email,
                                                                     'password': password,
                                                                     'name': name})
        message = response.json()['message']
        status_code = response.status_code
        success = response.json()['success']
        assert message == EMAIL_PASS_NAME_EMPTY and status_code == 403 and success is False
