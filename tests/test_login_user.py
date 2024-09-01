import allure
import pytest
import requests
from variables import (URL, AUTH_LOGIN, test_email, test_password, test_name,
                       EMAIL_PASS_INCORRECT, AUTH_USER)


class TestLoginUser:

    @allure.testcase('Login user with valid data')
    def test_login_user_valid_data_logged_in(self, login_user):
        response = login_user
        success = response.json()['success']
        status_code = response.status_code
        assert success is True and status_code == 200

    @allure.testcase('Login user with invalid data')
    @pytest.mark.parametrize('email, password', [['', test_password], [test_email, '']])
    def test_login_user_invalid_data_login_error(self, email, password):
        requests.post(f'{URL}/{AUTH_USER}', data={'email': test_password,
                                                  'password': test_password,
                                                  'name': test_name})

        if email == '':
            with allure.step(f'Login with wrong email: {email}'):
                response = requests.post(f'{URL}/{AUTH_LOGIN}', data={'email': f'{password}@mail.ru',
                                                                      'password': password})
        else:
            with allure.step(f'Login with wrong password: {password}'):
                response = requests.post(f'{URL}/{AUTH_LOGIN}', data={'email': email,
                                                                      'password': email})

        status_code = response.status_code
        success = response.json()['success']
        message = response.json()['message']

        assert status_code == 401 and message == EMAIL_PASS_INCORRECT and success is False
