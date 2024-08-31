import requests
import pytest
from variables import (URL, AUTH_REGISTER, EMAIL_PASS_NAME_EMPTY, USER_EXISTS, test_email, test_password,
                       test_name)


class TestCreateUser:

    def test_create_user_valid_data_user_is_created(self, user_payload, create_user):
        response = create_user
        assert response.status_code == 200 and response.json()['success'] is True

    def test_create_same_user_twice_user_already_exists(self, user_payload, create_user):
        response = create_user
        assert response.status_code == 200

        response_2 = requests.post(f'{URL}/{AUTH_REGISTER}', data=user_payload)
        message = response_2.json()['message']
        success = response_2.json()['success']
        status_code = response_2.status_code
        assert success is False and message == USER_EXISTS and status_code == 403

    @pytest.mark.parametrize('email, password, name', [[test_email, '', test_name],
                                                       ['', test_password, test_name],
                                                       [test_email, test_password, '']])
    def test_create_user_empty_data_error_need_required_fields(self, email, password, name):
        response = requests.post(f'{URL}/{AUTH_REGISTER}', data={'email': email,
                                                                 'password': password,
                                                                 'name': name})
        message = response.json()['message']
        status_code = response.status_code
        success = response.json()['success']
        assert message == EMAIL_PASS_NAME_EMPTY and status_code == 403 and success is False
