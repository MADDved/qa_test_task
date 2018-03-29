"""Служебные сущности для автотестов."""
import psycopg2
from psycopg2 import sql


class TestCaseDbManageMixin():
    """Примесный класс для добавления поддержки управления БД.

    Содержит реализацию служебных методов:
     * _add_entries_to_db - добавление записей в БД
     * _delete_entries_from_db - удаление записей из БД

    Свойство db_credentials должно быть переопределено для корректной работы.
    """

    db_credentials = {
        'host': 'hostmane',
        'port': 5432,
        'user': 'postgres',
        'password': 'password',
        'database': 'database'
        }

    @classmethod
    def _add_entries_to_db(cls, entries):
        """Служебная функция. Добавить записи в БД.

        на вход:
         * entries - список, в котором каждый эдлемент - словарь в котором
          должны быть как минимум следующие ключи:
           * table_name - содержит строку с именем таблицы
           * values - содержит список или кортеж со значениями, которые надо
            добавить.
        """
        connection = psycopg2.connect(**cls.db_credentials)
        cursor = connection.cursor()
        query = sql.SQL('INSERT INTO {} VALUES %s')
        for entry in entries:
            cursor.execute(query.format(sql.Identifier(entry['table_name'])),
                           (entry['values'], ))
        connection.commit()
        connection.close()

    @classmethod
    def _delete_entries_from_db(cls, entries):
        """Служебная функция. Удалить записи из БД.

        на вход:
         * entries - список, в котором каждый эдлемент - словарь в котором
          должны быть как минимум следующие ключи:
           * table_name - содержит строку с именем таблицы
           * values - содержит список или кортеж со значениями, которые надо
            добавить.
        """
        connection = psycopg2.connect(**cls.db_credentials)
        cursor = connection.cursor()
        query = sql.SQL('DELETE FROM {} WHERE "data"=%s')
        for entry in entries:
            cursor.execute(query.format(sql.Identifier(entry['table_name'])),
                           (entry['values'][0], ))
        connection.commit()
        connection.close()


ref_responses = {
    'sucsess': {
        'status': 200,
    },
    'page_not_found': {
        'data': '404 page not found',
        'status': 404,
    },
    'config_not_present': {
        'data': {'error': 'config model not present'},
        'status': 400,
    },
    'record_not_found': {
        'data': {'error': 'record not found'},
        'status': 400,
    },
    'bad_input': {
        'data': {'error': 'Bad input'},
        'status': 400,
    },
}

db_values = [{
    'table_name': 'develop_mr_robot_configs',
    'values': ('test_data_1', 'test_1.host.test', 9991, 'test_database_1',
               'test_user_1', 'test_password_1', 'test_schema_1'),
    'request': {'Type': 'Develop.mr_robot', 'Data': 'test_data_1'},
    'ref_data': {
        'Data': 'test_data_1',
        'Host': 'test_1.host.test',
        'Port': 9991,
        'Database': 'test_database_1',
        'User': 'test_user_1',
        'Password': 'test_password_1',
        'Schema': 'test_schema_1'
        }
    },
    {
    'table_name': 'test_vpn_configs',
    'values': ('test_data_1', 'test_1.host.test', 9991,
               'test_1.virtualhost.test', 'test_user_1', 'test_password_1'),
    'request': {'Type': 'Test.vpn', 'Data': 'test_data_1'},
    'ref_data': {
        'Data': 'test_data_1',
        'Host': 'test_1.host.test',
        'Port': 9991,
        'Virtualhost': 'test_1.virtualhost.test',
        'User': 'test_user_1',
        'Password': 'test_password_1'
        }
    }
]

emtpy_fields_db_values = [{
    'table_name': 'develop_mr_robot_configs',
    'values': ('test_data_2', '', 9991, 'test_database_2',
               'test_user_2', 'test_password_2', 'test_schema_2'),
    'request': {'Type': 'Develop.mr_robot', 'Data': 'test_data_2'},
    'ref_data': {
        'Data': 'test_data_2',
        'Host': '',
        'Port': 9991,
        'Database': 'test_database_2',
        'User': 'test_user_2',
        'Password': 'test_password_2',
        'Schema': 'test_schema_2'
        },
    'empty_field': 'Host'
    },
    {
    'table_name': 'develop_mr_robot_configs',
    'values': ('test_data_3', 'test_3.host.test', None, 'test_database_3',
               'test_user_3', 'test_password_3', 'test_schema_3'),
    'request': {'Type': 'Develop.mr_robot', 'Data': 'test_data_3'},
    'ref_data': {
        'Data': 'test_data_3',
        'Host': 'test_3.host.test',
        'Port': 0,
        'Database': 'test_database_3',
        'User': 'test_user_3',
        'Password': 'test_password_3',
        'Schema': 'test_schema_3'
        },
    'empty_field': 'Port'
    },
    {
    'table_name': 'develop_mr_robot_configs',
    'values': ('test_data_4', 'test_4.host.test', 9991, '',
               'test_user_4', 'test_password_4', 'test_schema_4'),
    'request': {'Type': 'Develop.mr_robot', 'Data': 'test_data_4'},
    'ref_data': {
        'Data': 'test_data_4',
        'Host': 'test_4.host.test',
        'Port': 9991,
        'Database': '',
        'User': 'test_user_4',
        'Password': 'test_password_4',
        'Schema': 'test_schema_4'
        },
    'empty_field': 'Database'
    },
    {
    'table_name': 'develop_mr_robot_configs',
    'values': ('test_data_5', 'test_5.host.test', 9991, 'test_database_5',
               '', 'test_password_5', 'test_schema_5'),
    'request': {'Type': 'Develop.mr_robot', 'Data': 'test_data_5'},
    'ref_data': {
        'Data': 'test_data_5',
        'Host': 'test_5.host.test',
        'Port': 9991,
        'Database': 'test_database_5',
        'User': '',
        'Password': 'test_password_5',
        'Schema': 'test_schema_5'
        },
    'empty_field': 'User'
    },
    {
    'table_name': 'develop_mr_robot_configs',
    'values': ('test_data_6', 'test_6.host.test', 9991, 'test_database_6',
               'test_user_6', '', 'test_schema_6'),
    'request': {'Type': 'Develop.mr_robot', 'Data': 'test_data_6'},
    'ref_data': {
        'Data': 'test_data_6',
        'Host': 'test_6.host.test',
        'Port': 9991,
        'Database': 'test_database_6',
        'User': 'test_user_6',
        'Password': '',
        'Schema': 'test_schema_6'
        },
    'empty_field': 'Password'
    },
    {
    'table_name': 'develop_mr_robot_configs',
    'values': ('test_data_7', 'test_7.host.test', 9991, 'test_database_7',
               'test_user_7', 'test_password_7', ''),
    'request': {'Type': 'Develop.mr_robot', 'Data': 'test_data_7'},
    'ref_data': {
        'Data': 'test_data_7',
        'Host': 'test_7.host.test',
        'Port': 9991,
        'Database': 'test_database_7',
        'User': 'test_user_7',
        'Password': 'test_password_7',
        'Schema': ''
        },
    'empty_field': 'Schema'
    },
    {
    'table_name': 'test_vpn_configs',
    'values': ('test_data_2', '', 9991,
               'test_2.virtualhost.test', 'test_user_2', 'test_password_2'),
    'request': {'Type': 'Test.vpn', 'Data': 'test_data_2'},
    'ref_data': {
        'Data': 'test_data_2',
        'Host': '',
        'Port': 9991,
        'Virtualhost': 'test_2.virtualhost.test',
        'User': 'test_user_2',
        'Password': 'test_password_2'
        },
    'empty_field': 'Host'
    },
    {
    'table_name': 'test_vpn_configs',
    'values': ('test_data_3', 'test_3.host.test', None,
               'test_3.virtualhost.test', 'test_user_3', 'test_password_3'),
    'request': {'Type': 'Test.vpn', 'Data': 'test_data_3'},
    'ref_data': {
        'Data': 'test_data_3',
        'Host': 'test_3.host.test',
        'Port': 0,
        'Virtualhost': 'test_3.virtualhost.test',
        'User': 'test_user_3',
        'Password': 'test_password_3'
        },
    'empty_field': 'Port'
    },
    {
    'table_name': 'test_vpn_configs',
    'values': ('test_data_4', 'test_4.host.test', 9991,
               '', 'test_user_4', 'test_password_4'),
    'request': {'Type': 'Test.vpn', 'Data': 'test_data_4'},
    'ref_data': {
        'Data': 'test_data_4',
        'Host': 'test_4.host.test',
        'Port': 9991,
        'Virtualhost': '',
        'User': 'test_user_4',
        'Password': 'test_password_4'
        },
    'empty_field': 'Virtualhost'
    },
    {
    'table_name': 'test_vpn_configs',
    'values': ('test_data_5', 'test_5.host.test', 9991,
               'test_5.virtualhost.test', '', 'test_password_5'),
    'request': {'Type': 'Test.vpn', 'Data': 'test_data_5'},
    'ref_data': {
        'Data': 'test_data_5',
        'Host': 'test_5.host.test',
        'Port': 9991,
        'Virtualhost': 'test_5.virtualhost.test',
        'User': '',
        'Password': 'test_password_5'
        },
    'empty_field': 'User'
    },
    {
    'table_name': 'test_vpn_configs',
    'values': ('test_data_6', 'test_6.host.test', 9991,
               'test_6.virtualhost.test', 'test_user_6', ''),
    'request': {'Type': 'Test.vpn', 'Data': 'test_data_6'},
    'ref_data': {
        'Data': 'test_data_6',
        'Host': 'test_6.host.test',
        'Port': 9991,
        'Virtualhost': 'test_6.virtualhost.test',
        'User': 'test_user_6',
        'Password': ''
        },
    'empty_field': 'Password'
    },
]
