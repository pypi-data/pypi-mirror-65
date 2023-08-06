import sys
import time
import threading
from functools import wraps
from multiprocessing import Process
from multiprocessing import Pool

from concurrent.futures import ThreadPoolExecutor

def progress(function=None, stream=sys.stdout, char='.', pause=0.2):
    """Shows a progress bar while a function runs."""
    if function is None:
        return lambda func: progress(func, stream, char, pause)

    @wraps(function)
    def wrap_function(*args, **kwargs):
        stop = False

        def progress_bar():
            while not stop:
                stream.write(char)
                stream.flush()
                time.sleep(pause)
            stream.write('\b\b finished.')
            stream.flush()
        
        try:
            p = threading.Thread(target=progress_bar)
            p.start()
            return function(*args, **kwargs)
        finally:
            stop = True

    return wrap_function

from time import sleep

@progress
def wait_with_me():
    sleep(5)

# lock = threading.Lock()


def func(name):
	# lock.acquire()
	print(f"{name} start")
	sleep(5)
	print(f"{name} finish")
	# lock.release()

@progress
def run():
	namelist = [1,2,3,4]
	with ThreadPoolExecutor(max_workers=4) as executor:
		res = [executor.submit(func, name) for name in namelist]


run()
# wait_with_me()
# test()