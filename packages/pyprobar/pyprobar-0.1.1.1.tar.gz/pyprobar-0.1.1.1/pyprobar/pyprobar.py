import sys
import time
import datetime
from datetime import timedelta
import numpy as np
from colorama import Fore

def get_bar(percent, symbol_1="█", symbol_2='>'):
    """Get the appearance of bar"""
    unit_percent = 0.034
    total_space = 30
    n_sign1, mod_sign1 = divmod(percent, unit_percent)
    N1 = int(n_sign1)
    sign1 = symbol_1 * N1
    N0 = int((mod_sign1/unit_percent) * (total_space - N1))

    sign0 = symbol_2 * N0
    SIGN = '|' + sign1 + sign0 + (total_space- N1 - N0-1) * ' ' + '|'
    return SIGN, N1

def get_color(N_color, update=True, COLOR=[0]):
    """random choice n colors"""
    if update == True or COLOR[0] == 0:
        color_list = ['CYAN', 'GREEN', 'RED', 'YELLOW', 'RESET', \
                      'LIGHTGREEN_EX',  'LIGHTRED_EX', \
                      'LIGHTYELLOW_EX',  'LIGHTBLACK_EX', 'LIGHTBLUE_EX', 'LIGHTCYAN_EX']
        # 'LIGHTMAGENTA_EX', 'MAGENTA', 'BLUE',

        color = [Fore.LIGHTCYAN_EX]  # Manually specify the first color
        for i in range(N_color - 2):
            color.append(eval("Fore." + np.random.choice(color_list)))
        color.append(Fore.LIGHTBLUE_EX)  # and the last color
        COLOR[0] = color

        return COLOR[0]
    else:
        return COLOR[0]



def bar(index, total_size, color='constant_random', symbol_1="█", symbol_2='>'):
    """Simple progress bar display, to instead of tqdm.
    :arg color: options  'constant_random', 'update_random', 'reset'
    """
    
    global first_time, flag_update_color, COLOR
    _index = index + 1
    if index == 0:
        first_time = time.time()
        flag_update_color = None
        index = 1

    _percent = index/(total_size) # for time
    percent = (_index)/total_size # for bar
    cost_time = time.time() - first_time

    total_time = cost_time/_percent
    # remain_time = int(total_time - cost_time)
    remain_time = int(total_time * (1-percent))
    remain_time = timedelta(seconds=remain_time)
    total_time = timedelta(seconds=int(total_time))
    ETC_1 = f"{remain_time}|{total_time} "
    ETC_2 = f"ETC: {(datetime.datetime.now() + remain_time).strftime('%m-%d %H:%M:%S')}"

    SIGN, N1 = get_bar(percent, symbol_1, symbol_2)

    if color == "update_random":
        if flag_update_color != N1:
            flag_update_color = N1
            COLOR = get_color(N_color=4, update=True)
            [color1, color2, color3, color4] = COLOR
        else:
            [color1, color2, color3, color4] = COLOR

        print(color1 + f"\r{percent * 100: >6.2f}% ", color2 + SIGN, color3 + f"{ETC_1}", color4 + f"{ETC_2}",
              Fore.RESET, end='',flush=True)
    elif color == 'constant_random':
        [color1, color2, color3, color4] = get_color(N_color=4, update=False)
        print(f"\r{color1}{percent * 100: >6.2f}% {color2}{SIGN}{color3}{ETC_1}{color4}{ETC_2} {Fore.RESET} ",
              end='', flush=True)
    elif color == 'reset':

        print(f"\r{percent * 100: >6.2f}% "+ SIGN + f"{ETC_1} {ETC_2}", end='', flush=True)
    else:
        raise ValueError("Invalid input!")

    if _index == total_size:
        print('\n')


class probar:
    """
    Simple progress bar display, to instead of tqdm.
    """

    def __init__(self, iterable, total_steps=None, symbol_1="█", symbol_2='>'):
        self.iterable = iterable
        self.t0 = time.time()
        self.symbol_1 = symbol_1
        self.symbol_2 = symbol_2

        if hasattr(iterable, '__len__'):
            self.total_steps = len(iterable)
        else:
            self.total_steps = total_steps
            if self.total_steps == None:
                raise ValueError(f'{iterable} has no __len__ attr, use total_steps param')

    def __iter__(self):
        for idx, i in enumerate(self.iterable):
            c = idx + 1

            if idx == 0:
                print(f"\r{0:.2f}% \t  {0:.1f}|{np.inf:.1f}s ", end='', flush=True)
                # sys.stdout.write(f"\r{0:.2f}% \t  {0:.1f}|{np.inf:.1f}s ")
                d_percent = 0.01
            else:
                # percent = self.c / self.total_steps
                percent = c / self.total_steps
                PERCENT = percent * 100

                if PERCENT >= d_percent:
                    d_percent += 0.01
                    cost_time = time.time() - self.t0
                    total_time = cost_time / percent

                    remain_time = int(total_time - cost_time)
                    remain_time = datetime.timedelta(seconds=remain_time)
                    total_time = timedelta(seconds=int(total_time))
                    cost_time = datetime.timedelta(seconds=int(cost_time))

                    _PERCENT=f"{PERCENT: >6.2f}%"
                    SIGN, N1 = get_bar(percent, self.symbol_1, self.symbol_2)
                    _COST = f" {cost_time}|{total_time} "
                    _REMAIN = f" {remain_time}|{total_time} "
                    _ETC = f" ETC: {(datetime.datetime.now() + remain_time).strftime('%m-%d %H:%M:%S')}"

                    print('\r'+ Fore.CYAN +f"{_PERCENT}"+Fore.LIGHTBLACK_EX+SIGN+  \
                          Fore.LIGHTGREEN_EX +_REMAIN+ Fore.LIGHTBLUE_EX +_ETC+ Fore.RESET, end='', flush=True)

            if c == self.total_steps:
                print('\n')

            yield idx, i

