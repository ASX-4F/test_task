from typing import List

from fastapi import FastAPI, Response, status

from database.connector import DatabaseConnector
from utils.anogramm import collect_anograms

app = FastAPI(
    title='Anogramm'
)

db = DatabaseConnector()

@app.get('/')
def hello():
    return 'This is Anogramm API. See /docs for more details'


@app.get('/get')
def get_anogramm(word: str = ''):
    result = collect_anograms(word, db.extract_words())
    if result:
        return result
    else:
        return None


@app.get('/get_all')
def get_all():
    return db.extract_words()


@app.post('/load')
def load(data: List[str], response: Response):
    result = db.load_words(data)
    if len(result) > 0:
        return f'data loaded: {result}'
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return 'data is not unique'

