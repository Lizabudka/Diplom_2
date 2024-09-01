import allure
import pytest
import requests
from variables import (URL, AUTH_USER, test_email, test_name, test_password, EMAIL_IS_USED,
                       AUTH_REGISTER, NEED_AUTH)


class TestChangeUserData:

    @allure.testcase('Change valid user data: PATCH request')
    @pytest.mark.parametrize('param', ['email', 'name'])
    def test_change_user_data_data_is_changed(self, create_user, param):
        token = create_user['response'].json()['accessToken']
        user_data = create_user['user_data']

        if param == 'email':
            changed_param = test_email
            not_changed_param = user_data['name']
        else:
            not_changed_param = user_data['email']
            changed_param = test_name
        changed_data = [changed_param, not_changed_param]

        with allure.step(f'Change {param} for {changed_param}'):
            response_change_data = requests.patch(f'{URL}/{AUTH_USER}',
                                                  headers={'Authorization': token},
                                                  data={param: changed_param})
        success = response_change_data.json()['success']
        status_code = response_change_data.status_code
        email = response_change_data.json()['user']['email']
        name = response_change_data.json()['user']['name']

        assert success is True and status_code is 200 and email in changed_data and name in changed_data

    @allure.testcase('Change invalid user data (PATCH request): User with such email already exists')
    def test_change_user_email_to_same_error_email_is_used(self, create_user):
        response_sign_up_1 = create_user['response']

        with allure.step(f'Create new user(2) (POST request) with data: {test_email},'
                         f'{test_password}, {test_name}'):
            response_sign_up_2 = requests.post(f'{URL}/{AUTH_REGISTER}',
                                               data={'email': test_email,
                                                     'password': test_password,
                                                     'name': test_name})
        token_1 = response_sign_up_1.json()['accessToken']
        token_2 = response_sign_up_2.json()['accessToken']

        with allure.step(f'Change user email to email of user(2): {test_email}, (PATCH request)'):
            response_change_data = requests.patch(f'{URL}/{AUTH_USER}',
                                                  headers={'Authorization': token_1},
                                                  data={'email': test_email})

        success = response_change_data.json()['success']
        message = response_change_data.json()['message']
        status_code = response_change_data.status_code

        with allure.step('Delete user(2)'):
            requests.delete(f'{URL}/{AUTH_USER}', headers={'Authorization': token_2})

        assert success is False and status_code == 403 and message == EMAIL_IS_USED

    @allure.testcase('Change user data without authorization: PATCH request')
    @pytest.mark.parametrize('param', ['email', 'name'])
    def test_no_auth_change_data_error_need_auth(self, param):
        if param == 'email':
            changed_param = test_email
        else:
            changed_param = test_name

        with allure.step(f'Change {param} to {changed_param}'):
            response = requests.patch(f'{URL}/{AUTH_USER}', data={param: changed_param})
        status_code = response.status_code
        message = response.json()['message']

        assert status_code == 401 and message == NEED_AUTH
