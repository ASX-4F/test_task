from main import app
from fastapi.testclient import TestClient
import json
import pytest

class TestAnogramm():

    client = TestClient(app)
    test_data = [
        ['foobar','barfoo','test','estt','вижу','живу','Кабан','Банка'],
        ['foobar','barfoo','','estt','вижу','','Кабан',0],
        ['foobar','bafoo',['test'],'estt','вижу','живу','Кабан','Банка'],
        ['fOobar','barfOO',['test','estt'],'ви жу',-10,'Кабан','Банка'],
        ['fOobar',None,'ви жу',-10,'Кабан','Банка'],
        ['']

    ]


    def test_root(self):
        response = self.client.get('/')
        assert response.status_code == 200
        assert response.json() == "This is Anogramm API. See /docs for more details"

    @pytest.mark.parametrize('data', test_data)
    def test_load(self, data):
        response = self.client.post(
            '/load',
            headers={'Content-Type': 'application/json'},
            data=json.dumps(data)
        )
        if all(isinstance(element, str) for element in data):
            assert response.status_code == 200
        else:
            assert response.status_code != 200