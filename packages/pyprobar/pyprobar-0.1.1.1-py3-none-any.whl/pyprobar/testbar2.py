import sys, re, abc, threading

CLEAR_TO_END = "\033[K"
UP_ONE_LINE = "\033[F"


class ProgressBar(object, metaclass=abc.ABCMeta):
    def __init__(self, width=25, title=''):
        self.width = width
        self.title = ProgressBar.filter_str(title)
        self._lock = threading.Lock()

    @property
    def lock(self):
        return self._lock

    @abc.abstractmethod
    def update(self, progress=0):
        pass

    @staticmethod
    def filter_str(pending_str):
        """去掉字符串中的\r、\t、\n"""
        return re.sub(pattern=r'\r|\t|\n', repl='', string=pending_str)


class CircleProgress(ProgressBar):
    def __init__(self, width=10, title=''):
        """
         @param width : 进度条展示的长度
         @param title : 进度条前面展示的文字
        """
        super(CircleProgress, self).__init__(width=width, title=title)
        self._current_char = ''

    def update(self, progress=0):
        """
        @param progress : 当前进度值,非0则更新符号
        """
        with self.lock:
            if progress > 0:
                self._current_char = self._get_next_circle_char(self._current_char)
            sys.stdout.write('\r' + CLEAR_TO_END)
            sys.stdout.write("\r%s:[%s]" % (self.title, self._current_char))
            # sys.stdout.flush()

    def _get_next_circle_char(self, current_char):
        if current_char == '':
            current_char = '-'
        elif current_char == '-':
            current_char = '\\'
        elif current_char == '\\':
            current_char = '|'
        elif current_char == '|':
            current_char = '/'
        elif current_char == '/':
            current_char = '-'
        return current_char


class LineProgress(ProgressBar):
    def __init__(self, total=100, symbol='#', width=25, title=''):
        """
         @param total : 进度总数
         @param symbol : 进度条符号
         @param width : 进度条展示的长度
         @param title : 进度条前面展示的文字
        """
        super(LineProgress, self).__init__(width=width, title=title)
        self.total = total
        self.symbol = symbol
        self._current_progress = 0

    def update(self, progress=0):
        """
        @param progress : 当前进度值
        """
        with self.lock:
            if progress > 0:
                self._current_progress = progress
            sys.stdout.write('\r' + CLEAR_TO_END)
            hashes = '#' * int(self._current_progress / self.total * self.width)
            spaces = ' ' * (self.width - len(hashes))
            sys.stdout.write("\r%s:[%s] %d%%" % (self.title, hashes + spaces, self._current_progress))
            # sys.stdout.flush()


class MultiProgressManager(object):
    def __new__(cls, *args, **kwargs):
        """单例"""
        if not hasattr(cls, '_instance'):
            cls._instance = super(MultiProgressManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._progress_dict = {}
        self._lock = threading.Lock()

    def put(self, key, progress_bar):
        with self._lock:
            if key and progress_bar:
                self._progress_dict[key] = progress_bar
                progress_bar.index = len(self._progress_dict) - 1

    def clear(self):
        with self._lock:
            self._progress_dict.clear()

    def update(self, key, progress):
        """
        @param key : 待更新的进度条标识
        @param progress : 当前进度值
        """
        with self._lock:
            if not key:
                return
            delta_line = len(self._progress_dict)
            sys.stdout.write(UP_ONE_LINE * delta_line if delta_line > 0 else '')
            for tmp_key in self._progress_dict.keys():
                progress_bar = self._progress_dict.get(tmp_key)
                tmp_progress = 0
                if key == tmp_key:
                    tmp_progress = progress
                progress_bar.update(tmp_progress)
                sys.stdout.write('\n')

import time 
def mock_multi_progress(progress_manager, sleep_time):
    for i in range(1, 101):
        progress_manager.update(threading.current_thread().name, i)
        time.sleep(sleep_time)


def mock_single_progress(progress_bar, sleep_time):
    for i in range(1, 101):
        progress_bar.update(i)
        time.sleep(sleep_time)

# multi line
progress_manager = MultiProgressManager()

thread1 = threading.Thread(target=mock_multi_progress, args=(progress_manager, 0.05), name=str(1001))
thread2 = threading.Thread(target=mock_multi_progress, args=(progress_manager, 0.2), name=str(1002))
thread3 = threading.Thread(target=mock_multi_progress, args=(progress_manager, 0.1), name=str(1003))

thread_pool = []
thread_pool.append(thread1)
thread_pool.append(thread2)
thread_pool.append(thread3)

progress_manager.put(str(1001), LineProgress(total=100, title='1 thread'))
progress_manager.put(str(1002), LineProgress(total=100, title='2 thread'))
progress_manager.put(str(1003), LineProgress(total=100, title='3 thread'))

thread1.start()
thread2.start()
thread3.start()