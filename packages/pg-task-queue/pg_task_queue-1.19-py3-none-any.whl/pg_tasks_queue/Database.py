import os
import re
import sys
import copy
import traceback
import json
import datetime
import psycopg2
import psycopg2.extras
import psycopg2.extensions
import numpy as np
import pandas as pd
import threading
import csv
import tempfile
import socket


class Json:

    @classmethod
    def get_correct_json_value(cls, value):
        func_name = f'{cls.__name__}.{sys._getframe().f_code.co_name}()'
        try:
            if value is None:
                return None
            value = copy.deepcopy(value)
            if isinstance(value, dict):
                for k, v in value.items():
                    k = Json.get_correct_json_value(k)
                    v = Json.get_correct_json_value(v)
                    value[k] = v
            elif isinstance(value, list):
                result = []
                for v in value:
                    v = Json.get_correct_json_value(v)
                    result.append(v)
                value = result
            elif isinstance(value, pd.Timestamp) or isinstance(value, datetime.datetime):
                value = datetime.datetime.strftime(value, '%Y-%m-%d %H:%M:%S.%f')
            elif isinstance(value, np.dtype(np.int64).type):
                value = int(value)
            elif isinstance(value, np.bool_) or isinstance(value, np.bool):
                value = bool(value)
            return value
        except Exception as e:
            print(f'Error in {func_name}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
            print(f'Error in {func_name}: value: {value} : {type(value)}')
            return False

    @classmethod
    def json_dumps(cls, _json_value):
        func_name = f'{cls.__name__}.{sys._getframe().f_code.co_name}()'
        try:
            return json.dumps(Json.get_correct_json_value(_json_value))
        except Exception as e:
            print(f'Error in {func_name}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
            return None


class PgDatabase:

    _settings = dict()
    _connection = None
    _auto_disconnect = True
    _result = None

    def __init__(self, **kwargs):
        self._settings = kwargs.get('settings')
        if not isinstance(self._settings, dict):
            self._settings = dict()
        self._auto_disconnect = kwargs.get('auto_disconnect', self._auto_disconnect)
        self._connection = kwargs.get('connection')
        if self._connection is not None:
            self._auto_disconnect = False
        if kwargs.get('schema') is not None:
            self._settings['schema'] = kwargs.get('schema')

    @staticmethod
    def build_dict_from_row(cursor, row):
        x = {}
        for key, col in enumerate(cursor.description):
            x[col[0]] = row[key]
        return x

    def get_attr(self, attr_name):
        if not isinstance(self._settings, dict):
            return None
        return self._settings.get(attr_name)

    def set_attr(self, attr_name, attr_value):
        if isinstance(self._settings, dict):
            self._settings[attr_name] = attr_value

    @property
    def connection(self):
        return self._connection

    def connect(self, dbname=None, close_connection=False, reconnect=False):
        err_str = f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        if self._connection is not None and reconnect is False:
            return True
        if not isinstance(self._settings, dict):
            print(f'{err_str}: not isinstance(self._settings, dict)...')
            return False
        conn_dict = copy.deepcopy(self._settings)
        if dbname is not None:
            conn_dict['dbname'] = dbname
        conn_dict['sslmode'] = self._settings.get('sslmode', 'disable')
        conn_string = "host='{host}' port={port} dbname='{dbname}' user='{user}' password='{password}' " \
                      "sslmode='{sslmode}'".format(**conn_dict)
        try:
            self._connection = psycopg2.connect(conn_string, cursor_factory=psycopg2.extras.RealDictCursor)
            dec2_float = psycopg2.extensions.new_type(
                psycopg2.extensions.DECIMAL.values,
                'DEC2FLOAT',
                lambda value, curs: float(value) if value is not None else None)
            psycopg2.extensions.register_type(dec2_float, self._connection)
            self._connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            if close_connection:
                self.disconnect()
            return True
        except Exception as e:
            print(f'{err_str}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
            self._connection = None
            return False

    def connect_to_db(self):
        self._result = None
        if self._connection is not None:
            return True
        self.connect()
        return False if self._connection is None else True

    def disconnect(self, force=False):
        err_str = f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        if self._connection is None:
            return
        if self._auto_disconnect is True or force is True:
            try:
                self._connection.rollback()
                self._connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
                self._connection.close()
            except Exception as e:
                print(f'{err_str}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
            finally:
                self._connection = None

    def _update_dict(self, _dict):
        if isinstance(_dict, dict):
            for k, v in _dict.items():
                if isinstance(v, np.int64):
                    _dict[k] = int(v)
                elif isinstance(v, np.bool_):
                    _dict[k] = bool(v)
        return _dict

    def _execute(self, sql_string, sql_params=None, get_result=True):

        err_str = f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        if not self.connect_to_db():
            return False
        try:
            cursor = self._connection.cursor()
            if sql_params is None:
                cursor.execute(sql_string)
            else:
                cursor.execute(sql_string, self._update_dict(sql_params))
            if get_result:
                result = cursor.fetchall() or []
                if result and isinstance(result[0], tuple):
                    self._result = list(map(lambda row: self.build_dict_from_row(cursor, row), result))
                else:
                    self._result = result
            return True
        except Exception as e:
            print(f'{err_str}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
            self._connection.rollback()
            self._result = None
            raise e
            return False
        finally:
            if cursor is not None:
                cursor.close()

    def begin(self):
        if not self.connect_to_db():
            return False
        return True

    def do(self, sql_string, sql_params=None):
        if not self.connect_to_db():
            return False
        cursor = self._connection.cursor()
        cursor.execute(sql_string, sql_params)
        return True

    def commit(self):
        if self._connection is not None:
            self._connection.commit()

    def rollback(self):
        if self._connection is not None:
            self._connection.rollback()
            self._connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    def _execute_sql(self, sql_string, sql_params=None, get_result=True, returning=None):
        self._result = None
        res = self._execute(sql_string, sql_params=sql_params, get_result=get_result)
        self.disconnect()
        if returning:
            if not isinstance(self._result, list):
                return None
            elif len(self._result) == 0:
                return None
            return_value = self._result[0]
            if returning != '*':
                return_value = return_value[returning]
            return return_value
        return res

    def _make_where_conditions(self, conditions):
        def simple_sql_condition(field, op, value):
            cond = []
            vals = {}

            if value is not None:
                if isinstance(value, tuple) or isinstance(value, list):
                    if op == '@':  # sql
                        cond.append(field + " in " + value[0])
                        vals[field] = value[1]
                    elif op == '@>':
                        cond.append(field + " @> " + " %(" + field + ")s ")
                        vals[field] = value
                    else:
                        value = ["'{}'".format(v) for v in value]
                        suffix = " IN( {seq} )".format(seq=','.join(value))
                        if op == "!=" or op == "!":
                            op = "NOT"
                        else:
                            op = ""
                        cond.append(field + " " + op + suffix)
                        # vals.append(value)
                else:
                    if op == '@>$':
                        op = 'like'

                    cond.append(field + " " + op + " %(" + field + ")s ")
                    vals[field] = value
            else:
                if op == "!=" or op == "!":
                    op = " is not null "
                else:
                    op = " is null "
                cond.append(field + op)
            return cond, vals

        values = {}
        sql = ''
        cond = []
        for key, value in conditions.items():
            op = '='
            field = key
            # ~* , ~  <>!
            res = re.search(r'^([<>!@$=~*]{1,3})(.+)', field)
            if res:
                op = res.group(1)
                field = res.group(2)

            if re.search(r'|', field):  # (field1 = %s or field2 = %s or field3 = %s)
                fields = field.split("|")
                tmp_cond = []
                tmp_vals = {}
                for fld in fields:
                    c, v = simple_sql_condition(fld, op, value)
                    tmp_cond.extend(c)
                    tmp_vals.update(v)

                cond.append("( " + " or ".join(tmp_cond) + " )")
                values.update(tmp_vals)

            else:  # field = %s
                c, v = simple_sql_condition(field, op, value)
                cond.extend(c)
                values.update(v)
        if len(cond):
            sql = " AND ".join(cond)
        return values, sql

    def select(self, sql_string, where=None, order=None, limit=None, offset=None, group_by=None, lock=None):
        def sql_select_filter(sql_string, where, order=None, limit=None, offset=None, group_by=None, lock=None):
            values = {}
            if where:
                values, act_where_sql = self._make_where_conditions(where)
                if act_where_sql is not None:
                    sql_string += " WHERE " + act_where_sql

            if group_by is not None and len(group_by):
                sql_string += " GROUP BY " + ",".join(group_by)

            if order is not None and len(order):
                order_fields = []
                for field, direction in order.items():
                    order_fields.append(field + " " + direction)
                sql_string += " ORDER BY " + ",".join(order_fields)
            if limit is not None:
                sql_string += " LIMIT %(limit)s"
                values.update({"limit": limit})
            if offset is not None:
                sql_string += " OFFSET %(offset)s"
                values.update({"offset": offset})
            if lock is not None:
                sql_string += " FOR " + lock

            return sql_string, values

        result_sql, sql_params = sql_select_filter(sql_string, where, order, limit, offset, group_by, lock)
        if not self._execute_sql(sql_string=result_sql, sql_params=sql_params):
            return None
        return self._result

    def insert(self, table, values, returning='*'):
        keys = ','.join(values.keys())
        sql_params = ','.join(['%s' for key in values.keys()])
        result_sql = """INSERT INTO {} ({}) VALUES({})""".format(table, keys, sql_params)
        if returning is not None:
            result_sql += ' RETURNING ' + returning
        sql_params = []
        for v in values.values():
            if isinstance(v, dict):
                sql_params.append(psycopg2.extras.Json(v))
            else:
                sql_params.append(v)
        res = self._execute_sql(sql_string=result_sql, sql_params=sql_params, returning=returning)
        self.commit()
        return res

    def update(self, table, values, where=None, returning='*'):
        sql_params = {}
        keys = []
        for key in values:
            keys.append(key + '=%(' + key + ')s')
            v = values[key]
            if isinstance(v, dict):
                sql_params[key] = psycopg2.extras.Json(v)
            else:
                sql_params[key] = v
        result_sql = 'UPDATE {} SET {}'.format(table, ','.join(keys))
        if where:
            act_where_values, act_where_sql = self._make_where_conditions(where)
            result_sql += " WHERE " + act_where_sql
            sql_params.update(act_where_values)
        if returning:
            result_sql += ' RETURNING ' + returning
        return self._execute_sql(sql_string=result_sql, sql_params=sql_params, returning=returning)

    def delete(self, table, where):
        act_where_values, act_where_sql = self._make_where_conditions(where)
        result_sql = 'DELETE FROM {} WHERE {}'.format(table, act_where_sql)
        return self._execute_sql(sql_string=result_sql, sql_params=act_where_values, get_result=False)

    def execute_sql_without_result(self, result_sql):
        self._execute_sql(sql_string=result_sql, get_result=False)

    def copy_from(self, table, data, through_pipe=True, csv_filepath=None):
        err_str = f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}()'

        def copy_from_csv_file(csv_file):
            try:
                sql = f"""
                    COPY {table}({','.join(data[0].keys())}) FROM STDIN WITH
                    CSV
                    HEADER
                    DELIMITER AS ','
                    """
                cursor.copy_expert(sql, csv_file)
                return True
            except Exception as e:
                print(f'{err_str}.copy_from_csv_file(): {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
                self._connection.rollback()
                return False

        if not self.connect_to_db():
            return False
        cursor = self._connection.cursor()

        for index, row in enumerate(data):
            for key in row:
                if isinstance(row[key], str):
                    row[key] = row[key].replace('\t', '\\t').replace('\n', '\\n').\
                        replace('\r', '\\r').replace('`', "'").replace('\\', '')
                if row[key] == "":
                    row[key] = "\\N"
                if row[key] is None:
                    row[key] = "\\N"
                if isinstance(row[key], dict):
                    row[key] = json.dumps(row[key], ensure_ascii=False)

        if through_pipe:
            # https://stackoverflow.com/questions/6765310/piping-postgres-copy-in-python-with-psycopg2
            r_fd, w_fd = os.pipe()
            to_thread = threading.Thread(target=copy_from_csv_file, args=(os.fdopen(r_fd),))
            to_thread.start()
            write_f = os.fdopen(w_fd, 'w')
            wr = csv.DictWriter(write_f, tuple(data[0].keys()), delimiter=',', lineterminator='\n')
            wr.writeheader()
            for row in data:
                wr.writerow(row)
            write_f.close()
            to_thread.join()
        else:
            if csv_filepath is None:
                csv_filepath = os.path.join(tempfile.gettempdir(), '__temp.csv')
            if os.path.exists(csv_filepath):
                os.remove(csv_filepath)

            with open(csv_filepath, 'wt', encoding='utf-8') as csv_file:
                wr = csv.DictWriter(csv_file, tuple(data[0].keys()), delimiter=',', lineterminator='\n')
                wr.writeheader()
                for row in data:
                    wr.writerow(row)

            copy_from_csv_file(open(csv_filepath, 'rt', encoding='utf-8'))
            if os.path.exists(csv_filepath):
                os.remove(csv_filepath)

        self.commit()
        self.disconnect()

    def insert_df(self, table, df):
        df_columns = list(df.columns.values)
        columns = ",".join(df_columns)
        values = "VALUES({})".format(",".join(["%s" for _ in df_columns]))
        insert_stmt = "INSERT INTO {} ({}) {}".format(table, columns, values)
        close_connection = True if self._connection is None else False
        if not self.connect_to_db():
            return False
        cursor = self._connection.cursor()
        psycopg2.extras.execute_batch(cursor, insert_stmt, df.values)
        self.commit()
        self.disconnect()

    def create_database(self):
        sql_string = 'CREATE DATABASE {dbname};'.format(**self._settings)
        return self._execute_sql(sql_string=sql_string, get_result=False)

    def create_schema(self):
        sql_string = "CREATE SCHEMA {schema} AUTHORIZATION {user};".format(**self._settings)
        return self._execute_sql(sql_string=sql_string, get_result=False)

    def _test_table(self, table_name, table_columns, create, primary_key=None):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        err_str = f'Error in {func_name}'

        table_schema = self._settings.get('schema')
        sql_string = 'SELECT * FROM information_schema.tables'
        result_dict = self.select(sql_string=sql_string,
                                  where={'table_type': 'BASE TABLE',
                                         'table_schema': table_schema,
                                         'table_name': table_name})
        if result_dict is None:
            return False
        if len(result_dict) == 0:
            if not create:
                return False
            print(f'Try to create table "{table_name}"...')
            sql_string = f'CREATE TABLE {table_schema}.{table_name} ('
            counter = 0
            for column_name, table_column in table_columns.items():
                if counter > 0:
                    sql_string += ', '

                not_null = False
                if isinstance(table_column, dict):
                    column_dic = copy.deepcopy(table_column)
                    table_column = column_dic.get('type')
                    if table_column is None:
                        print(f'{err_str}: table_column is None: table_name: {table_name}; '
                                     f'add_column: {column_name}; table_column: {table_column}')
                        return False
                    not_null = column_dic.get('not_null')
                    not_null = False if not_null is None else not_null
                elif not isinstance(table_column, str):
                    print(f'{err_str}: table_column is not str: table_name: {table_name}; '
                                 f'add_column: {column_name}; table_column: {table_column}')
                    return False
                sql_string += f'"{column_name}" {table_column}'
                if not_null:
                    sql_string += ' NOT NULL'
                counter += 1
            if primary_key:
                if not isinstance(primary_key, list):
                    print(f'{err_str}: primary_key is not list: table_name: {table_name}')
                    return False
                sql_string += ', PRIMARY KEY('
                counter = 0
                for k in primary_key:
                    if counter > 0:
                        sql_string += ', '
                    sql_string += f'"{k}"'
                    counter += 1
                sql_string += ')'
            sql_string += ');'
            if not self._execute_sql(sql_string, get_result=False):
                return False
        elif len(self._result) == 1:
            sql_string = 'SELECT column_name, udt_name as column_type, column_default, ' \
                         'character_maximum_length, is_nullable FROM information_schema.columns'
            result_dict = self.select(sql_string=sql_string,
                                      where={'table_schema': self._settings.get('schema'),
                                             'table_name': table_name})
            if result_dict is None:
                return False
            real_table_columns = {}
            for column_dict in result_dict:
                real_table_columns[column_dict.get('column_name')] = column_dict

            add_columns = []
            update_columns = []
            for column_name, column_type in table_columns.items():
                real_table_column = real_table_columns.get(column_name)
                if real_table_column is None:
                    add_columns.append(column_name)
                else:
                    not_null = False
                    if isinstance(column_type, dict):
                        column_dic = copy.deepcopy(column_type)
                        column_type = column_dic.get('type')
                        not_null = column_dic.get('not_null')
                        not_null = False if not_null is None else not_null
                    elif not isinstance(column_type, str):
                        print(f'{err_str}: column_type is not str;'
                                     f' column_name: {column_name}; column_type: {column_type}')
                        return False
                    if column_type == 'serial':
                        if real_table_column.get('column_type') != 'int4':
                            update_columns.append(column_name)
                            continue
                        elif real_table_column.get('column_default') is None:
                            update_columns.append(column_name)
                            continue
                    else:
                        real_table_column_type = real_table_column.get('column_type')
                        if column_type.startswith('varchar('):
                            character_maximum_length = real_table_column.get('character_maximum_length')
                            real_table_column_type += f'({character_maximum_length})'
                        if column_type != real_table_column_type:
                            update_columns.append(column_name)
                            continue
                    if not_null:
                        if real_table_column.get('is_nullable') != 'NO':
                            update_columns.append(column_name)

            remove_columns = []
            for column_name, column_dict in real_table_columns.items():
                table_column = table_columns.get(column_name)
                if table_column is None:
                    remove_columns.append(column_name)
            update = False
            if len(add_columns) > 0:
                print(f'{func_name}: table_name: {table_name}; add_columns: {add_columns}')
                update = True
            if len(remove_columns) > 0:
                print(f'{func_name}: table_name: {table_name}; remove_columns: {remove_columns}')
                update = True
            if len(update_columns) > 0:
                print(f'{func_name}: table_name: {table_name}; update_columns: {update_columns}')
                update = True

            if not update:
                return True
            else:
                if not create:
                    return False
                if len(add_columns) > 0:
                    for column_name in add_columns:
                        table_column = table_columns.get(column_name)
                        if isinstance(table_column, str):
                            sql_string = f'ALTER TABLE {table_schema}.{table_name} ' \
                                         f'ADD COLUMN "{column_name}" {table_column}'
                            if not self._execute_sql(sql_string, get_result=False):
                                return False
                        else:
                            print(f'{err_str} in add_columns: table_name: {table_name}; '
                                         f'column_name: {column_name}; table_column: {table_column}')
                            return False

                if len(remove_columns) > 0:
                    for column_name in remove_columns:
                        sql_string = f'ALTER TABLE {table_schema}.{table_name} DROP COLUMN "{column_name}"'
                        if not self._execute_sql(sql_string, get_result=False):
                            return False

                if len(update_columns) > 0:
                    for column_name in update_columns:
                        table_column = table_columns.get(column_name)
                        if isinstance(table_column, str):
                            sql_string = f'ALTER TABLE {table_schema}.{table_name} ' \
                                         f'ALTER COLUMN "{column_name}" SET DATA TYPE {table_column}'
                            if not self._execute_sql(sql_string, get_result=False):
                                return False
                        else:
                            print(f'{err_str} in update_column: table_name: {table_name}; '
                                         f'column_name: {column_name}; table_column: {table_column}')
                            return False
        else:
            print(f'{err_str}: len(self.result) != 0;1. self._result: {self._result}')
        return True


class TasksDatabase:
    pg_database = None

    @classmethod
    def test_tables(cls, create=False):
        err_str = f'Error in {cls.__name__}.{sys._getframe().f_code.co_name}()'
        table_name = 'tasks'
        table_columns = {'task_id': 'serial',
                         'module': 'varchar',
                         'func': 'varchar',
                         'params': 'text',
                         'result': 'text',
                         'status': 'varchar',
                         'retry_count': 'int4',
                         'max_retry_count': 'int4',
                         'scheduled_time': 'timestamp',
                         'defer_time': 'timestamp',
                         'create_time': 'timestamp',
                         'started_time': 'timestamp',
                         'finished_time': 'timestamp',
                         'priority': 'int4',
                         'worker_host': 'varchar',
                         'failed_email': 'varchar',
                         'success_email': 'varchar',
                         'parent_task_id': 'int4',
                         }
        if not TasksDatabase.pg_database._test_table(table_name, table_columns, create, primary_key=['task_id']):
            print(f'{err_str}: Database.pg_database._test_table("{table_name}")')
            return False
        return True

    @classmethod
    def init(cls, **kwargs):
        err_str = f'Error in {cls.__name__}.{sys._getframe().f_code.co_name}()'
        pg_database = PgDatabase(**kwargs)
        if pg_database.connect(close_connection=True):
            TasksDatabase.pg_database = pg_database
            return True
        print(f'{err_str}: database not available')
        return False

    @classmethod
    def force_disconnect(cls):
        if TasksDatabase.pg_database is not None:
            TasksDatabase.pg_database.disconnect(force=True)

    @classmethod
    def add_task(cls, task_dict):
        func_name = f'{cls.__name__}.{sys._getframe().f_code.co_name}()'
        if TasksDatabase.pg_database is None:
            print(f'Error in {func_name}: Database.pg_database is None...')
            return None
        if not isinstance(task_dict, dict):
            print(f'Error in {func_name}: not isinstance(task_dict, dict)...')
            return None
        if 'params' in task_dict.keys():
            params = task_dict.get('params')
            if isinstance(params, dict) or isinstance(params, list):
                params = Json.json_dumps(params)
                if params is None:
                    print(f'Error in {func_name}: helper.Json.json_dumps() is None...')
                    return None
            task_dict['params'] = params
        schema = TasksDatabase.pg_database.get_attr('schema')
        res_dict = TasksDatabase.pg_database.insert(table=f"{schema}.tasks", values=task_dict)
        return res_dict.get('task_id')

    @classmethod
    def get_schema(cls):
        func_name = f'{cls.__name__}.{sys._getframe().f_code.co_name}()'
        if TasksDatabase.pg_database is None:
            print(f'Error in {func_name}: Database.pg_database is None...')
            return None
        schema = TasksDatabase.pg_database.get_attr('schema')
        if TasksDatabase.pg_database is None:
            print(f"Error in {func_name}: Database.pg_database.get_attr('schema') is None...")
            return None
        return schema

    @classmethod
    def get_new_task(cls, sql_string, disconnect=True):
        func_name = f'{cls.__name__}.{sys._getframe().f_code.co_name}()'
        schema = TasksDatabase.get_schema()
        if schema is None:
            return None

        if not TasksDatabase.pg_database.begin():
            print(f'Error in {func_name}: not Database.pg_database.begin()...')
            return None

        tasks = TasksDatabase.pg_database.select(sql_string=sql_string, lock='update SKIP LOCKED')
        if not isinstance(tasks, list):
            print(f'Error in {func_name}: not isinstance(tasks, list)...')
            TasksDatabase.pg_database.disconnect()
            return None
        if len(tasks) == 0:
            if disconnect:
                TasksDatabase.pg_database.disconnect()
            return {'task_dict': None}
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        task_dict = dict(tasks[0])
        update_values = {'started_time': datetime.datetime.now(),
                         'status': 'working',
                         'worker_host': f'{host_ip} : {host_name}'}
        task_dict = TasksDatabase.pg_database.update(table=f'{schema}.tasks', values=update_values,
                                                     where={'task_id': task_dict.get('task_id')})
        TasksDatabase.pg_database.commit()
        if disconnect:
            TasksDatabase.pg_database.disconnect()

        return {'task_dict': task_dict}

    @classmethod
    def get_one_task(cls):
        func_name = f'{cls.__name__}.{sys._getframe().f_code.co_name}()'
        schema = TasksDatabase.get_schema()
        if schema is None:
            print(f'Error in {func_name}: TasksDatabase.get_schema() is None...')
            return None

        def get_sql_result(_sql_string):
            result = TasksDatabase.get_new_task(_sql_string, disconnect=False)
            if not isinstance(result, dict):
                return None
            task_dict = result.get('task_dict')
            if isinstance(task_dict, dict):
                return task_dict
            return None

        if not TasksDatabase.pg_database.connect_to_db():
            print(f'Error in {func_name}: not TasksDatabase.pg_database.connect_to_db()...')
            return None

        # 1. status is null and scheduled_time <= NOW()
        sql_string = """
            select 
                *
            from 
                {schema}.tasks
            where 
                status is null
                and (scheduled_time is not null and scheduled_time <= NOW())
            order by
                scheduled_time asc, priority desc
            limit 1
        """.format(schema=schema)
        result = get_sql_result(sql_string)
        if isinstance(result, dict):
            TasksDatabase.pg_database.disconnect()
            return result

        # 2. status = 'error' is null and max_retry_count > retry_count
        sql_string = """
            select 
                * 
            from 
                {schema}.tasks 
            where 
                status='error'
                and max_retry_count > retry_count
            order by
                finished_time asc, priority desc
            limit 1
        """.format(schema=schema)
        result = get_sql_result(sql_string)
        if isinstance(result, dict):
            TasksDatabase.pg_database.disconnect()
            return result

        # 3. Simple Tasks
        sql_string = """
            select 
                * 
            from 
                {schema}.tasks 
            where 
                status is null
                and scheduled_time is null
            order by
                priority desc, task_id asc  
            limit 1
        """.format(schema=schema)
        result = get_sql_result(sql_string)
        if isinstance(result, dict):
            TasksDatabase.pg_database.disconnect()
            return result

        TasksDatabase.pg_database.disconnect()
        return None

    @classmethod
    def update_task(cls, task_id, update_values):
        func_name = f'{cls.__name__}.{sys._getframe().f_code.co_name}()'
        if task_id is None:
            print(f'Error in {func_name}: task_id is None...')
            return False
        if not isinstance(update_values, dict):
            print(f'Error in {func_name}: not isinstance(update_values, dict)...')
            return False
        schema = TasksDatabase.get_schema()
        if schema is None:
            return False
        result = TasksDatabase.pg_database.update(table=f'{schema}.tasks', values=update_values, where={'task_id': task_id})
        return True

    @classmethod
    def update_task_error(cls, task_dict, error=None):
        func_name = f'{cls.__name__}.{sys._getframe().f_code.co_name}()'
        if not isinstance(task_dict, dict):
            print(f'Error in {func_name}: not isinstance(task_dict, dict)...')
            return False
        if error is None:
            error = f'{func_name}: error not difined...'
        update_values = {'finished_time': datetime.datetime.now(),
                         'status': 'error',
                         'result': error}
        max_retry_count = task_dict.get('max_retry_count')
        max_retry_count = 0 if max_retry_count is None else max_retry_count
        if max_retry_count > 0:
            retry_count = task_dict.get('retry_count')
            retry_count = 0 if retry_count is None else retry_count
            update_values['retry_count'] = retry_count + 1
        return TasksDatabase.update_task(task_dict.get('task_id'), update_values)

