import json

import pytest
from fastapi.testclient import TestClient

from database.connector import DatabaseConnector
from main import app


class TestAnogramm():
    client = TestClient(app)
    db = DatabaseConnector()

    valid_test_data = [
        ['cat', 'дом', 'apple', 'стол', 'book', 'окно', 'dog', 'кресло', 'banana', 'рука'],
        ['table', 'ручка', 'car', 'книга', 'chair', 'яблоко', 'window', 'кот', 'глаз', 'door'],
        ['голова', 'hand', 'стул', 'гитара', 'ноутбук', 'book', 'яблоко', 'dog', 'карта', 'дерево'],
        ['дом', 'window', 'глаз', 'pen', 'стол', 'banana', 'гитара', 'книга', 'chair', 'cat'],
        ['кофе', 'apple', 'рука', 'стул', 'ноутбук', 'карта', 'стол', 'head', 'кот', 'глаз']
    ]

    invalid_test_data = [
        ['cat', ['дом', 'apple'], 'стол', 'book'],
        ['table', None, 'car', 'книга', 'chair'],
        ['голова', 'hand', 465, 'гитара', 'ноутбук'],
        ['дом', 'window', 'глаз', -6, 'стол'],
        ['кофе', ['apple'], 'рука', 'стул', 'ноутбук'],
        ['голова', {'дерево': 1}, 'dog', 'ручка', 'chair'],
        [['гитара', 'рука', 'стол', 'pen', 'глаз', 'дом']]
    ]

    not_exists_test_data = [
        ['flower', 'гитара', 'chair', 'sun', 'слон', 'lamp', 'river', 'птица', 'clock', 'moon'],
        ['computer', 'солнце', 'bookshelf', 'яблоко', 'часы', 'catfish', 'keyboard', 'стена', 'гриб', 'cloud'],
        ['mountain', 'дождь', 'ящик', 'lampshade', 'elephant', 'flowerpot', 'screen', 'камень', 'bus', 'mirror'],
        ['guitar', 'банан', 'pencil', 'замок', 'звезда', 'собака', 'pizza', 'фонарь', 'hat', 'парк'],
        ['bicycle', 'корабль', 'cloud', 'медведь', 'карандаш', 'mirror', 'стрела', 'candle', 'трава', 'гора']
    ]

    def test_root(self):
        response = self.client.get('/')
        assert response.status_code == 200
        assert response.json() == "This is Anogramm API. See /docs for more details"

    @pytest.mark.parametrize('data', invalid_test_data)
    def test_load_invalid_data(self, data):
        response = self.client.post(
            '/load',
            headers={'Conten-Type': 'application/json'},
            data=json.dumps(data)
        )
        assert response.status_code == 422

    @pytest.mark.parametrize('data', valid_test_data)
    def test_load_valid_data(self, data):
        response = self.client.post(
            '/load',
            headers={'Conten-Type': 'application/json'},
            data=json.dumps(data)
        )
        assert response.status_code == 200

    def test_get_all(self):
        response = self.client.get('/get_all')
        assert response.status_code == 200

    @pytest.mark.parametrize('data', valid_test_data)
    def test_get_anogram(self, data):
        for word in data:
            response = self.client.get(f'/get?word={word}')
            assert response.status_code == 200


    @pytest.mark.parametrize('data', invalid_test_data)
    def test_delete_invalid_data(self, data):
        response = self.client.post(
            '/delete',
            headers={'Content-Type': 'application/json'},
            data=json.dumps(data)
        )

        assert response.status_code == 422

    @pytest.mark.parametrize('data', valid_test_data)
    def test_delete_valid_data(self, data):
        response = self.client.post(
            '/delete',
            headers={'Content-Type': 'application/json'},
            data=json.dumps(data)
        )
        assert response.status_code == 200

    @pytest.mark.parametrize('data', not_exists_test_data)
    def test_delete_not_exists_data(self, data):
        response = self.client.post(
            '/delete',
            headers={'Content-Type': 'application/json'},
            data=json.dumps(data)
        )

        assert response.status_code == 400
