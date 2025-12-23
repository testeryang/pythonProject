import threading # 导入线程库

from streamlit import toast

from tests.BlockExprole.test_api import *


def YC_TUI_blocks(max_count,thread_count):
    import time  # 导入时间库
    # 创建一个字典，用于最后汇总结果使用
    result_data = {
        'success_count' : 0,
        'error_conut' : 0,
        'total_count' : 0,
        'error' : [],
        'start_time' : time.time() # 这个函数是代表的当前时间
    }

    # 创建线程锁，保护代码不被同时多个引用
    lock = threading.Lock()

    # 编写嵌套函数，保证线程去执行任务
    def worker(thread_id):
        try:
            print(f'第{thread_id}次线程开始执行')
            blocks = get_tui_blocks(max_messages=max_count)
            total_count = len(blocks)
            with lock:
                result_data['success_count'] += 1
                result_data['total_count'] += total_count
            print(f'第{thread_id}次线程执行完成，共收到{len(blocks)}条信息')

        except Exception as e:
            with lock:
                result_data['error_conut'] += 1

                result_data['error'].append(f'第{thread_id}线程报错，报错信息为:{str(e)}')

            print(f'第{thread_id}次线程失败，失败原因为{str(e)}')

    threads = []

    for i in range(thread_count):
        t = threading.Thread(target=worker,args=(i+1,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    result_data['haoshi_time'] = time.time() - result_data['start_time']
    return result_data

def YC_Latest_Transactions(max_shuliang,thread_count):
    import time
    result_data = {
        'success_count' : 0,
        'error_count' : 0,
        'error' : [],
        'start_time' : time.time(),
        'shuliang_ever' : 0
}
    lock = threading.Lock()
    def latest_transactions():
        try:
            blocks = get_Latest_Transactions(max_messages=max_shuliang)
            a = len(blocks)
            with lock:
                result_data['shuliang_ever'] += a
                result_data['success_count'] += 1

        except Exception as err:
            with lock:
                result_data['error_count'] += 1
                result_data['error'].append(str(err))

    thread = []
    for a in range(thread_count):
        t = threading.Thread(target=latest_transactions,args=(a+1,))
        t.start()
        thread.append(t)
    for t in thread:
        t.join()
    result_data['haoshi_time'] = time.time() - result_data['start_time']
    print(result_data)
    return result_data

def YC_Account_Updates(address,max_messages,thread_count):
    import time
    result_data = {
        'success_count' : 0,
        'error_count' : 0,
        'start_time' : time.time(),
        'error' : [],
        'total_count' : 0
    }
    lock = threading.Lock()
    def account_updates():
        try:
            account = get_Account_Updates(address=address,max_messages=max_messages)
            total = len(account)
            with lock:
                result_data['success_count'] += 1
                result_data['total_count'] += total

        except Exception as err:
            result_data['error_count'] += 1
            result_data['error'].append(str(err))

    threads = []

    for a in range(thread_count):
        t = threading.Thread(target=account_updates,args=(a+1,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    result_data['haoshi_time'] = time.time() - result_data['start_time']

    return result_data