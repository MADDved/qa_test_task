"""Автотесты в рамках тестового задания."""
import unittest

import requests

import service


TEST_DB_CREDENTIALS = {
        'host': '192.168.0.203',
        'port': 5431,
        'user': 'postgres',
        'password': 'pass',
        'database': 'db'
        }
TEST_URL = 'http://192.168.0.203:8078/get_config'


class TestGetConfigPositiveCases(unittest.TestCase,
                                 service.TestCaseDbManageMixin):
    """Проверка позитивных сценариев для метода get_config."""

    db_credentials = TEST_DB_CREDENTIALS
    url = TEST_URL
    ref_responses = service.ref_responses
    db_values = service.db_values

    @classmethod
    def setUpClass(cls):
        """Подготовка."""
        cls._add_entries_to_db(cls.db_values)

    @classmethod
    def tearDownClass(cls):
        """Очистка после завершения."""
        cls._delete_entries_from_db(cls.db_values)

    def test_correct_request_calls_sucsess_response(self):
        """Запрос с корректными параметрами: успешный ответ."""
        for entry in self.db_values:
            request_data = entry['request']
            ref_data = entry['ref_data']
            with self.subTest(request_data=request_data, ref_data=ref_data):
                response = requests.post(self.url, json=request_data)

                self.assertEqual(response.status_code,
                                 service.ref_responses['sucsess']['status'])
                self.assertEqual(response.json(), ref_data)

    def test_incorrect_type_calls_config_not_present(self):
        """Запрос с некорректным значением Type: ответ об отсутсвии конфига."""
        request_data = self.db_values[0]['request'].copy()
        request_data['Type'] = request_data['Type']*2  # Точно не правильный

        response = requests.post(self.url, json=request_data)

        self.assertEqual(response.status_code,
                         service.ref_responses['config_not_present']['status'])
        self.assertEqual(response.json(),
                         service.ref_responses['config_not_present']['data'])

    def test_incorrect_data_calls_record_not_found(self):
        """Запрос с некорректным значением Data: ответ об отсутсвии записи."""
        request_data = self.db_values[0]['request'].copy()
        request_data['Data'] = request_data['Data']*2  # Точно не правильный

        response = requests.post(self.url, json=request_data)

        self.assertEqual(response.status_code,
                         service.ref_responses['record_not_found']['status'])
        self.assertEqual(response.json(),
                         service.ref_responses['record_not_found']['data'])

    def test_empty_type_calls_config_not_present(self):
        """Запрос с пустым значением Type: ответ об отсутсвии конфига."""
        request_data = self.db_values[0]['request'].copy()
        request_data['Type'] = request_data['Type']*2  # Точно не правильный

        response = requests.post(self.url, json=request_data)

        self.assertEqual(response.status_code,
                         service.ref_responses['config_not_present']['status'])
        self.assertEqual(response.json(),
                         service.ref_responses['config_not_present']['data'])

    def test_empty_data_calls_record_not_found(self):
        """Запрос с пустым значением Data: ответ об отсутсвии записи."""
        request_data = self.db_values[0]['request'].copy()
        request_data['Data'] = request_data['Data']*2  # Точно не правильный

        response = requests.post(self.url, json=request_data)

        self.assertEqual(response.status_code,
                         service.ref_responses['record_not_found']['status'])
        self.assertEqual(response.json(),
                         service.ref_responses['record_not_found']['data'])

    def test_missed_type_calls_bad_input(self):
        """Запрос с пропущенным полем Type: ответ bad input."""
        request_data = self.db_values[0]['request'].copy()
        request_data.pop('Type')

        response = requests.post(self.url, json=request_data)

        self.assertEqual(response.status_code,
                         service.ref_responses['bad_input']['status'])
        self.assertEqual(response.json(),
                         service.ref_responses['bad_input']['data'])

    def test_missed_data_calls_bad_input(self):
        """Запрос с пропущенным полем Type: ответ bad input."""
        request_data = self.db_values[0]['request'].copy()
        request_data.pop('Data')

        response = requests.post(self.url, json=request_data)

        self.assertEqual(response.status_code,
                         service.ref_responses['bad_input']['status'])
        self.assertEqual(response.json(),
                         service.ref_responses['bad_input']['data'])


class TestEmptyValuesInDbSupport(unittest.TestCase,
                                 service.TestCaseDbManageMixin):
    """Проверка поддержки возможност хранения пыстых значений в БД.

    Выделены в отдельный тест-кейс, т.к. требуют свои данные в БД.
    """

    db_credentials = TEST_DB_CREDENTIALS
    url = TEST_URL
    ref_responses = service.ref_responses
    db_values = service.emtpy_fields_db_values

    @classmethod
    def setUpClass(cls):
        """Подготовка."""
        cls._add_entries_to_db(cls.db_values)

    @classmethod
    def tearDownClass(cls):
        """Очистка после завершения."""
        cls._delete_entries_from_db(cls.db_values)

    def test_empty_values_supported_in_db(self):
        """Если одно из полей БД имеет пустое значение: успешный ответ ."""
        for entry in self.db_values:
            with self.subTest(db_table=entry['table_name'],
                              field=entry['empty_field']):
                response = requests.post(self.url, json=entry['request'])

                self.assertEqual(response.status_code,
                                 service.ref_responses['sucsess']['status'])
                self.assertEqual(response.json(), entry['ref_data'])


class TestGetConfigNegativeCases(unittest.TestCase):
    """Проверка негативны сценариев для метода get_config."""

    url = TEST_URL
    ref_responses = service.ref_responses
    db_values = service.db_values  # Для удобства ссылки на рабочий запрос

    def test_invalid_path_calls_404(self):
        """Запрос на некорректный маршрут: 404 страница."""
        url = self.url + '_test'

        response = requests.post(url, json=self.db_values[0]['request'])

        self.assertEqual(response.status_code,
                         service.ref_responses['page_not_found']['status'])
        self.assertEqual(response.text,
                         service.ref_responses['page_not_found']['data'])

    def test_empty_request_calls_bad_input(self):
        """Пустой запрос: ответ bad input."""
        response = requests.post(self.url)

        self.assertEqual(response.status_code,
                         service.ref_responses['bad_input']['status'])
        self.assertEqual(response.json(),
                         service.ref_responses['bad_input']['data'])

    def test_unparsable_json_calls_bad_input(self):
        """Запрос с недекодируемой JSON строкой: ответ bad input."""
        response = requests.post(self.url, data='{')

        self.assertEqual(response.status_code,
                         service.ref_responses['bad_input']['status'])
        self.assertEqual(response.json(),
                         service.ref_responses['bad_input']['data'])


if __name__ == '__main__':
    unittest.main()
