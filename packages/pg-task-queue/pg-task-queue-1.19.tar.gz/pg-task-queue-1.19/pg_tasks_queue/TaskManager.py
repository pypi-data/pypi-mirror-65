import sys
import traceback
from pg_tasks_queue.Database import TasksDatabase as database


class TaskManager(object):

    def init(self, database_dict=None, connection=None, schema=None, auto_disconnect=True):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        try:
            if database_dict is None and connection is None:
                print(f'Error in {func_name}: database_dict is None and connection is None; return...')
                return False
            if connection is not None:
                if schema is None:
                    print(f'Error in {func_name}: connection is not None and schema is None; return...')
                    return False
                auto_disconnect = False
            kwargs = {'settings': database_dict,
                      'connection': connection,
                      'schema': schema,
                      'auto_disconnect': auto_disconnect}
            if not database.init(**kwargs):
                print(f'Error in {func_name}: not database.init(); return...')
                return False
            if not database.test_tables(create=True):
                print(f'Error in {func_name}: not database.test_tables(); return...')
                return False
            return True
        except Exception as e:
            print(f'Error in {func_name}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
            return False

    def add_task(self, task_dict, task_func=None):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        try:
            if not isinstance(task_dict, dict):
                print(f'Error in {func_name}: not isinstance(task_dict, dict)...')
                return None
            if task_func is not None:
                task_dict['module'] = task_func.__module__
                task_dict['func'] = task_func.__name__
            if task_dict.get('module') is None:
                print(f"Error in {func_name}: task_dict.get('module') is None")
                return None
            if task_dict.get('func') is None:
                print(f"Error in {func_name}: task_dict.get('func') is None")
                return None
            task_id = database.add_task(task_dict)
            return task_id
        except Exception as e:
            print(f'Error in {func_name}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
            return None

    def force_disconnect(self):
        database.force_disconnect()
