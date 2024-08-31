import pytest
import requests
from variables import (URL, AUTH_USER, test_email, test_name, test_password, EMAIL_IS_USED,
                       AUTH_REGISTER, NEED_AUTH)


class TestChangeUserData:

    @pytest.mark.parametrize('param', ['email', 'name'])
    def test_change_user_name_name_is_changed(self, create_user, user_payload, param):
        response_sign_up = create_user
        token = response_sign_up.json()['accessToken']
        if param == 'email':
            changed_param = test_email
            not_changed_param = user_payload['name']
        else:
            not_changed_param = user_payload['email']
            changed_param = test_name
        user_data = [changed_param, not_changed_param]

        response_change_data = requests.patch(f'{URL}/{AUTH_USER}',
                                              headers={'Authorization': token},
                                              data={param: changed_param})
        success = response_change_data.json()['success']
        status_code = response_change_data.status_code
        email = response_change_data.json()['user']['email']
        name = response_change_data.json()['user']['name']

        assert success is True and status_code is 200 and email in user_data and name in user_data

    def test_change_user_email_to_same_error_email_is_used(self, create_user, user_payload):
        response_sign_up_1 = create_user
        response_sign_up_2 = requests.post(f'{URL}/{AUTH_REGISTER}',
                                           data={'email': test_email,
                                                 'password': test_password,
                                                 'name': test_name})
        token_1 = response_sign_up_1.json()['accessToken']
        token_2 = response_sign_up_2.json()['accessToken']

        response_change_data = requests.patch(f'{URL}/{AUTH_USER}',
                                              headers={'Authorization': token_1},
                                              data={'email': test_email})

        success = response_change_data.json()['success']
        message = response_change_data.json()['message']
        status_code = response_change_data.status_code

        requests.delete(f'{URL}/{AUTH_USER}', headers={'Authorization': token_2})

        assert success is False and status_code == 403 and message == EMAIL_IS_USED

    @pytest.mark.parametrize('param', ['email', 'name'])
    def test_no_auth_change_data_error_need_auth(self, param):
        if param == 'email':
            changed_param = test_email
        else:
            changed_param = test_name

        response = requests.patch(f'{URL}/{AUTH_USER}', data={param: changed_param})
        status_code = response.status_code
        message = response.json()['message']

        assert status_code == 401 and message == NEED_AUTH
