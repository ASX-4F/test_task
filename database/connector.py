import psycopg2
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS


class DatabaseConnector():
    def __init__(self):
        self._DB_HOST = DB_HOST
        self._DB_PORT = DB_PORT
        self._DB_NAME = DB_NAME
        self._DB_USER = DB_USER
        self._DB_PASS = DB_PASS

    def load_words(self, word_list_from_api: list) -> list:
        with psycopg2.connect(
                host=self._DB_HOST,
                database=self._DB_NAME,
                port=self._DB_PORT,
                user=self._DB_USER,
                password=self._DB_PASS
        ) as connection:
            with connection.cursor() as cursor:
                words_from_db = self.extract_words()
                list_to_load = list(set([word for word in word_list_from_api if word not in words_from_db]))

                if len(list_to_load) > 0:
                    placeholder = ','.join(['(%s)'] * len(list_to_load))
                    cursor.execute(f'INSERT INTO words (word) VALUES {placeholder}', list_to_load)
            connection.commit()
        return list_to_load

    def extract_words(self) -> list | None:
        with psycopg2.connect(
                host=self._DB_HOST,
                database=self._DB_NAME,
                port=self._DB_PORT,
                user=self._DB_USER,
                password=self._DB_PASS
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT word FROM words')
                word_list_tuples = cursor.fetchall()
                if len(word_list_tuples) > 0:
                    return [element for tuple in word_list_tuples for element in tuple]
                else:
                    return []
