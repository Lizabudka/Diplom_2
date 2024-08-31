import string
import requests
import pytest
import random
from variables import AUTH_REGISTER, URL, AUTH_USER, AUTH_LOGIN, INGREDIENTS, ORDERS


# generate random user data
@pytest.fixture(scope='function')
def user_payload():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    email = generate_random_string(10) + '@yandex.ru'
    password = generate_random_string(10)
    name = generate_random_string(10)

    payload = {
        'email': email,
        'password': password,
        'name': name
    }
    return payload


# get random ingredients' hash
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
    response = requests.post(f'{URL}/{AUTH_REGISTER}', data=user_payload)
    yield response
    token = response.json()['accessToken']
    requests.delete(f'{URL}/{AUTH_USER}', headers={'Authorization': token})


@pytest.fixture(scope='function')
def login_user(user_payload, create_user):
    response = requests.post(f'{URL}/{AUTH_LOGIN}', data={'email': user_payload['email'],
                                                          'password': user_payload['password']})
    return response


@pytest.fixture(scope='function')
def create_order_no_auth(get_ingredients_hash):
    burger = get_ingredients_hash.get_random_ingr()
    response = requests.post(f'{URL}/{ORDERS}', data={'ingredients': [burger['bun'],
                                                                      burger['main'],
                                                                      burger['sauce']]})
    return response


@pytest.fixture(scope='function')
def create_order_with_auth(get_ingredients_hash, create_user):

    class Dummy:
        @staticmethod
        def post_order():
            burger = get_ingredients_hash.get_random_ingr()
            token = create_user.json()['accessToken']
            response = requests.post(f'{URL}/{ORDERS}', headers={'Authorization': token},
                                     data={'ingredients': [burger['bun'],
                                                           burger['main'],
                                                           burger['sauce']]})
            return response

    return Dummy()
