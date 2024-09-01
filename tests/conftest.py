import string
import requests
import pytest
import random
import allure
from variables import AUTH_REGISTER, URL, AUTH_USER, AUTH_LOGIN, INGREDIENTS, ORDERS


@allure.step('Generate random user data')
@pytest.fixture(scope='function')
def user_payload():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    class Dummy:
        @staticmethod
        def get_new_user_data():
            email = generate_random_string(10) + '@yandex.ru'
            password = generate_random_string(10)
            name = generate_random_string(10)

            payload = {
                'email': email,
                'password': password,
                'name': name
            }
            return payload

    return Dummy()


@allure.step('Create lists with all ingredients')
@pytest.fixture(scope='function')
def get_ingredients_hash():
    response = requests.get(f'{URL}/{INGREDIENTS}')
    ingredients_list = response.json()['data']

    class Dummy:
        def __init__(self):
            self.buns = [i['_id'] for i in ingredients_list if i['type'] == 'bun']
            self.mains = [i['_id'] for i in ingredients_list if i['type'] == 'main']
            self.sauces = [i['_id'] for i in ingredients_list if i['type'] == 'sauce']

        def get_random_ingr(self):
            burger_ingredients = {'bun': random.choice(self.buns),
                                  'main': random.choice(self.mains),
                                  'sauce': random.choice(self.sauces)}
            return burger_ingredients

    return Dummy()


@pytest.fixture(scope='function')
def create_user(user_payload):
    user_data = user_payload.get_new_user_data()
    with allure.step(f'Create new user (POST request) with data: {user_data}'):
        response = requests.post(f'{URL}/{AUTH_REGISTER}', data=user_data)
    data = {'response': response,
            'user_data': user_data}
    yield data
    with allure.step(f'Delete user (DELETE request) with data: {user_data}'):
        token = response.json()['accessToken']
        requests.delete(f'{URL}/{AUTH_USER}', headers={'Authorization': token})


@allure.step('Login user: POST request')
@pytest.fixture(scope='function')
def login_user(create_user):
    user_data = create_user['user_data']
    response = requests.post(f'{URL}/{AUTH_LOGIN}', data={'email': user_data['email'],
                                                          'password': user_data['password']})
    return response


@allure.step('Create order without authorization: POST request')
@pytest.fixture(scope='function')
def create_order_no_auth(get_ingredients_hash):
    burger = get_ingredients_hash.get_random_ingr()
    response = requests.post(f'{URL}/{ORDERS}', data={'ingredients': [burger['bun'],
                                                                      burger['main'],
                                                                      burger['sauce']]})
    return response


@allure.step('Create order with authorization: POST request')
@pytest.fixture(scope='function')
def create_order_with_auth(get_ingredients_hash, create_user):
    class Dummy:
        @staticmethod
        def post_order():
            burger = get_ingredients_hash.get_random_ingr()
            token = create_user['response'].json()['accessToken']
            response = requests.post(f'{URL}/{ORDERS}', headers={'Authorization': token},
                                     data={'ingredients': [burger['bun'],
                                                           burger['main'],
                                                           burger['sauce']]})
            return response
    return Dummy()
