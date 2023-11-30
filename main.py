from typing import List

from fastapi import FastAPI, Response, status

from database.connector import DatabaseConnector
from utils.anogramm import collect_anograms
import uvicorn

app = FastAPI(
    title='Anogramm'
)

db = DatabaseConnector()


@app.get('/')
def hello():
    return 'This is Anogramm API. See /docs for more details'


@app.get('/get')
def get_anogramm(word: str = ''):
    '''
    Возвращает все слова из базы, являющиеся анаграммой к ключевому
    :param word: Ключевое слово для подбора анаграмм
    :return: Json с анаграммами
    '''
    result = collect_anograms(word, db.extract_words())
    if result:
        return result
    else:
        return None


@app.get('/get_all')
def get_all():
    '''
    Получить все слова. Аналог select * from words
    :return: Json со словами
    '''
    return db.extract_words()


@app.post('/load')
def load(data: List[str], response: Response):
    '''
    Загружает слова в базу. В базу попадают только те, которых там еще нет.
    :param data: Json со списком слов для загрузки
    :return: Json со списком успешно загруженных слов
    '''
    result = db.load_words(data)
    if len(result) > 0:
        return f'data loaded: {result}'
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return 'data is not unique'

@app.post('/delete')
def delete_words(data: List[str], response: Response):
    '''
    Удаляет слова из БД
    :param data: Список слов для удаления
    :return: Список удаленных слов
    '''
    result = db.delete_words(data)
    if len(result) > 0:
        return f'data deleted: {result}'
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return 'data is not exist'

if __name__ == '__main__':
    uvicorn.run('main:app')