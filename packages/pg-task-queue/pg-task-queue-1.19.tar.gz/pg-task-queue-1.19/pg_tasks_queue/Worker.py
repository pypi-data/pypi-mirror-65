import os
import sys
import json
import traceback
import importlib.util
import time
import threading
import queue
import datetime
import multiprocessing
import pg_tasks_queue.Kthread as kthread
from pg_tasks_queue.Database import TasksDatabase as database


class Worker(object):

    _timeout_sec = 60.
    _blocking = False
    _started = False
    _sleep_sec = 1.
    _started_timestamp = None
    _life_timeout_sec = None

    def check_module(self, module_name):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        module_spec = importlib.util.find_spec(module_name)
        if module_spec is None:
            print(f'Error in {func_name}: module: "{module_name}" not found')
            return None
        else:
            return module_spec

    def import_module(self, module_name):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        try:
            module_spec = self.check_module(module_name)
            if module_spec is None:
                return None
            module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(module)
            return module
        except Exception as e:
            print(f'Error in {func_name}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
            return None

    def import_function_from_module(self, module_name, function_name):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        try:
            module = self.import_module(module_name)
            if module is None:
                return None
            if not hasattr(module, function_name):
                print(f'Error in {func_name}: module: "{module_name}"; function: "{function_name}" not found')
                return None
            return getattr(module, function_name)
        except Exception as e:
            print(f'Error in {func_name}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
            return None

    def worker(self, task_dict):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        # print(f'{func_name}; os.getpid(): {os.getpid()}; os.getppid(): {os.getppid()}')
        try:
            task_module = task_dict.get('module')
            task_func = task_dict.get('func')
            func = self.import_function_from_module(task_module, task_func)
            if func is None:
                error = f'Error in {func_name}: import_function_from_module({task_module}, {task_func}) is None'
                print(error)
                return {'error': error}
            else:
                params = task_dict.get('params')
                if isinstance(params, str):
                    params = json.loads(params)
                if not isinstance(params, dict):
                    params = dict()
                print(f'Started task (id={task_dict.get("task_id")}) at {datetime.datetime.now()}; task_dict: {task_dict}')
                res = func(**params)
                print(f'Finished task (id={task_dict.get("task_id")}) at {datetime.datetime.now()}; result: {res}')
                return res
        except Exception as e:
            error = f'Error in {func_name}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}'
            print(error)
            return {'status': 'error', 'result': error}

    def worker_process(self, queue, task_dict):
        result = self.worker(task_dict)
        queue.put(result)

    def update_db_task(self, task_dict, result_dict):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        if not isinstance(result_dict, dict):
            error = f'Error in {func_name}: not isinstance(_result_dict, dict)...'
            print(error)
            database.update_task_error(task_dict, error)
        else:
            status = result_dict.get('status')
            result = result_dict.get('result', '')
            if not isinstance(status, str):
                error = f'Error in {func_name}: not isinstance(status, str)...'
                print(error)
                database.update_task_error(task_dict, error)
            elif status == 'error':
                database.update_task_error(task_dict, result)
            else:
                update_values = {'finished_time': datetime.datetime.now(),
                                 'status': status,
                                 'result': result}
                database.update_task(task_dict.get('task_id'), update_values)

    def stop_woker(self, func_name, task_dict):
        error = f'Error in {func_name}: worker.is_alive() => os.kill(os.getpid(), signal.SIGINT)'
        database.update_task_error(task_dict, error)
        try:
            # sys.exit(1)
            import signal
            os.kill(os.getpid(), signal.SIGINT)
        finally:
            print(error)

    def _do_task(self, process_type):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        # print(f'{func_name}; os.getpid(): {os.getpid()}; os.getppid(): {os.getppid()}')
        if not self._started:
            print(f'{func_name}; self._started = False; return')
            return
        try:
            task_dict = database.get_one_task()
            # print(f'{func_name}: now={datetime.datetime.now()}; task_dict: {task_dict}')
            if isinstance(task_dict, dict):
                task_dict = dict(task_dict)
                if process_type is None or process_type.lower() == 'none' or process_type.lower() == '<none>':
                    timer = threading.Timer(self._timeout_sec, self.stop_woker, args=(func_name, task_dict,))
                    timer.setDaemon(True)
                    timer.start()
                    result_dict = self.worker(task_dict)
                    timer.cancel()
                    self.update_db_task(task_dict, result_dict)
                elif process_type in ['fork', 'thread', 'kthread']:
                    if process_type == 'fork':
                        worker_queue = multiprocessing.Queue()
                        worker = multiprocessing.Process(target=self.worker_process, args=(worker_queue, task_dict,))
                    else:
                        worker_queue = queue.Queue()
                        if process_type == 'thread':
                            worker = threading.Thread(target=self.worker_process, args=(worker_queue, task_dict,))
                            worker.setDaemon(True)
                        else:
                            worker = kthread.KThread(target=self.worker_process, args=(worker_queue, task_dict,))
                    worker.start()
                    worker.join(timeout=self._timeout_sec)
                    if worker.is_alive():
                        if process_type in ['fork', 'kthread']:
                            worker.terminate()
                            error = f'Error in {func_name}: worker({process_type}).is_alive() => worker.terminate()'
                            print(error)
                            database.update_task_error(task_dict, error)
                        else:
                            error = f'Error in {func_name}: worker({process_type}).is_alive() => sys.exit(1)'
                            print(error)
                            database.update_task_error(task_dict, error)
                            sys.exit(1)
                    else:
                        if not worker_queue.empty():
                            self.update_db_task(task_dict, worker_queue.get_nowait())
                        else:
                            error = f'Error in {func_name}: queue is empty()...'
                            print(error)
                            database.update_task_error(task_dict, error)

            if not self._blocking:
                if self._life_timeout_sec is not None:
                    time_delta = datetime.datetime.now() - self._started_timestamp
                    if time_delta.total_seconds() > self._life_timeout_sec:
                        return
                threading.Timer(self._sleep_sec, self._do_task, args=(process_type,)).start()
        except Exception as e:
            print(f'Error in {func_name}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')

    def start(self, config_dict):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        try:
            if not isinstance(config_dict, dict):
                print(f'Error in {func_name}: not isinstance(config_dict, dict); return...')
                return

            database_dict = config_dict.get('database')
            if not isinstance(database_dict, dict):
                print(f'Error in {func_name}: not isinstance(database_dict, dict)...')
                return

            kwargs = {'settings': database_dict}
            if not database.init(**kwargs):
                print(f'Error in {func_name}: not database.init(); return...')
                return False
            if not database.test_tables(create=False):
                print(f'Error in {func_name}: not database.test_tables(); return...')
                return False

            process_type = 'none'
            worker_cfg = config_dict.get('worker')
            if isinstance(worker_cfg, dict):
                self._timeout_sec = float(worker_cfg.get('timeout_sec', self._timeout_sec))
                self._sleep_sec = float(worker_cfg.get('sleep_sec', self._sleep_sec))
                self._life_timeout_sec = float(worker_cfg.get('life_timeout_sec', self._life_timeout_sec))
                blocking = worker_cfg.get('blocking')
                if isinstance(blocking, str):
                    self._blocking = False if worker_cfg.get('blocking', 'true').lower() == 'false' else True
                elif isinstance(blocking, bool):
                    self._blocking = blocking
                process_type = worker_cfg.get('process_type', process_type)

            if process_type.lower() not in ['fork', 'thread', 'kthread', 'none', '<none>']:
                print(f'Error in {func_name}: unknown process_type "{process_type}"...')
                return

            self._started = True
            self._started_timestamp = datetime.datetime.now()
            if self._blocking:
                while self._started:
                    self._do_task(process_type)
                    time.sleep(self._sleep_sec)
                    if self._life_timeout_sec is not None:
                        time_delta = datetime.datetime.now() - self._started_timestamp
                        if time_delta.total_seconds() > self._life_timeout_sec:
                            break
            else:
                self._do_task(process_type)
        except Exception as e:
            print(f'Error in {func_name}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
            raise e

    def stop(self):
        self._started = False
