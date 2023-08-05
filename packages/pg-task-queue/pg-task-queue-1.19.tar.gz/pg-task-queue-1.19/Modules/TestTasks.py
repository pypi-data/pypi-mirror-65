import sys
import time
import datetime
import traceback


def sleep(**params):
    func_name = f'{sys._getframe().f_code.co_name}()'
    period = 1.0
    try:
        counter = 2
        print(f'{func_name}; type(params) = {type(params)}; params = {params}')
        if isinstance(params, dict):
            # print(f'{func_name}; params = {params}')
            counter = int(params.get('counter', counter))
            period = float(params.get('period', period))
        for i in range(counter):
            print(f'{func_name}; now={datetime.datetime.now()}; counter={i}')
            time.sleep(period)
        return {'status': 'finished', 'result': 'ok'}
    except Exception as e:
        error = f'Error in {func_name}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}'
        print(error)
        return {'status': 'error', 'result': error}


def sleep_false(**params):
    func_name = f'{sys._getframe().f_code.co_name}()'
    period = 1.0
    try:
        counter = 2
        print(f'{func_name}; type(params) = {type(params)}; params = {params}')
        if isinstance(params, dict):
            counter = int(params.get('counter', counter))
            period = float(params.get('period', period))
        for i in range(counter):
            print(f'{func_name}; now={datetime.datetime.now()}; counter={i}')
            time.sleep(period)
        return {'status': 'error', 'result': f'{func_name}; test error'}
    except Exception as e:
        error = f'Error in {func_name}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}'
        print(error)
        return {'status': 'error', 'result': error}
