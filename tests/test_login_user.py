import pytest
import requests
from variables import URL, AUTH_LOGIN, test_email, test_password, EMAIL_PASS_INCORRECT


class TestLoginUser:

    def test_login_user_valid_data_logged_in(self, login_user):
        response = login_user
        success = response.json()['success']
        status_code = response.status_code
        assert success is True and status_code == 200

    @pytest.mark.parametrize('email, password', [['', test_password], [test_email, '']])
    def test_login_user_invalid_data_login_error(self, user_payload, create_user, email, password):
        response_1 = create_user
        assert response_1.status_code == 200

        if email == '':
            response = requests.post(f'{URL}/{AUTH_LOGIN}', data={'email': user_payload['email'],
                                                                  'password': test_password})
        else:
            response = requests.post(f'{URL}/{AUTH_LOGIN}', data={'email': test_email,
                                                                  'password': user_payload['password']})

        status_code = response.status_code
        success = response.json()['success']
        message = response.json()['message']
        assert status_code == 401 and message == EMAIL_PASS_INCORRECT and success is False
