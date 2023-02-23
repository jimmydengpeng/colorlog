#######################################################################
# Copyright (C) 2023 Jimmy Deng (jimmydengpeng@gmail.com)             #
# Permission given to modify the code as long as you keep this        #
# declaration at the top                                              #
#######################################################################

from enum import Enum
from time import time
from typing import Any, Optional, Union
import json, yaml, numbers
import numpy as np
from humanfriendly.tables import format_pretty_table

# TODO:
# - [ ] 自动根据说所打印的字符长度判断是否换行
# - [ ] 设置全局的开关，根据level控制是否打印
# - [ ] 方法重载，允许打印单个参数，不带提示字符串


class Color(Enum):
    # names    =    values
    GRAY       =    30
    RED        =    31
    GREEN      =    32
    YELLOW     =    33
    BLUE       =    34
    MAGENTA    =    35
    CYAN       =    36
    WHITE      =    37
    CRIMSON    =    38

    @classmethod
    def is_valid_color(cls, name: str) -> bool:
        for color in cls:
            if name.upper() == color.name:
                return True
        return False
    
    @classmethod
    def get_color_by_name(cls, name: str):
        assert Color.is_valid_color(name)
        for color in cls:
            if name.upper() == color.name:
                return color



def colorize(string: str, color=Color.WHITE, bold=True, highlight=False) -> str:
    """
    @return: a str wrapped with ANSI ESC & Color code:
                \x1b[31;1m {str} \x1b[0m
                ----====== ----- =======
                ESC  CSI    str   reset
    """
    attr = []
    num = color.value
    if highlight: num += 10
    attr.append(str(num))
    if bold: attr.append('1')
    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)


'''
-----------------------
| DEBUG    | debug    |
| INFO     | info     |
| WARNING  | warning  |
| SUCCESS  | success  |
| ERROR    | error    |
-----------------------
'''

class LogLevel(Enum):
    # enumerated constants 
    SUCCESS = Color.GREEN
    DEBUG = Color.MAGENTA
    INFO = Color.BLUE
    WARNING = Color.YELLOW
    ERROR = Color.RED

LogSymbol = dict({
    # Enum members are hashable & can be used as dictionary keys
    LogLevel.SUCCESS:  "✔", 
    LogLevel.DEBUG:    "",
    LogLevel.INFO:     "",
    LogLevel.WARNING:  "⚠",
    LogLevel.ERROR:    "✖"
})
'''alternatives:  ➤  ☞ ⚑  ◎ ⊙  ⇨ ▶'''

def debug_msg(
        msg: str,
        level=LogLevel.DEBUG,
        color : Optional[Color] = None,
        bold=False,
        inline=False
    ):
    """
    return: symbol msg (same color), e.g.
    ✔ [SUCCESS] SUCCESS
     [DEBUG] DEBUG
     [INFO] INFO
    ⚠ [WARNING] WARNING
    ✖ [ERROR] ERROR
    """
    def colored_prompt(prompt: str) -> str:
        symbol = LogSymbol[level]
        text = symbol + ' [' + prompt + ']'
        return colorize(text, color=level.value, bold=True)

    '''prompt'''
    assert isinstance(level, LogLevel)
    level_name = str(level)[len(LogLevel.__name__)+1:]
    prompt = colored_prompt(level_name)

    '''inline'''
    end = " " if inline else "\n"

    '''Using LogLevel Color'''
    if color == None:
        # print(colorize(prompt, bold=True), colorize(msg, color=level.value, bold=bold))
        print(prompt, colorize(msg, color=level.value, bold=bold), end=end)
    else:
        # print(colorize(">>>", bold=True), colorize(msg, color=color, bold=bold), end=end)
        print(colorize(msg, color=color, bold=bold), end=end)

def debug_print(
        msg: str,
        args=None,
        level: LogLevel = LogLevel.DEBUG,
        color: Optional[Color] = None,
        inline=False
    ):
    debug_msg(msg, level, color=color, inline=inline)

    ''' pretty print dict '''
    if isinstance(args, dict):
        args = pretty_dict(args)

    if args is not None:
        print(args)


# from CoPO
class SafeFallbackEncoder(json.JSONEncoder):
    def __init__(self, nan_str="null", **kwargs):
        super(SafeFallbackEncoder, self).__init__(**kwargs)
        self.nan_str = nan_str

    def default(self, value):
        try:
            if np.isnan(value):
                return self.nan_str

            if (type(value).__module__ == np.__name__ and isinstance(value, np.ndarray)):
                return value.tolist()

            if issubclass(type(value), numbers.Integral):
                return int(value)
            if issubclass(type(value), numbers.Number):
                return float(value)

            return super(SafeFallbackEncoder, self).default(value)

        except Exception:
            return str(value)  # give up, just stringify it (ok for logs)

# from CoPO
def pretty_dict(result):
    cleaned = json.dumps(result.copy(), cls=SafeFallbackEncoder)
    return yaml.safe_dump(json.loads(cleaned), default_flow_style=False)


def get_formatted_time():
    """
    return: e.g. 20220921_200435
    """
    return time.strftime("%Y%m%d_%H%M%S", time.localtime())

def pretty_time(time_in_sec) -> str:
    unit_s = colorize("s", color=Color.GREEN, bold=False)
    unit_m = colorize("m", color=Color.YELLOW, bold=False)
    unit_h = colorize("h", color=Color.RED, bold=False)

    def get_s(t) -> str:
        return colorize(str(t), color=Color.GREEN) + \
               colorize("s", color=Color.GREEN, bold=False)

    def get_m(t) -> str:
        return colorize(str(t), color=Color.YELLOW) + \
               colorize("m", color=Color.YELLOW, bold=False)

    def get_h(t) -> str:
        return colorize(str(t), color=Color.RED) + \
               colorize("h", color=Color.RED, bold=False)

    time_in_sec = int(time_in_sec)
    if time_in_sec <= 100:
        return get_s(time_in_sec)

    elif time_in_sec > 60 and time_in_sec <= (60 * 60):
        m = time_in_sec // 60
        s = time_in_sec % 60
        return get_m(m) + get_s(s)

    elif time_in_sec > (60 * 60): 
        unit = "h"
        h = time_in_sec // (60 * 60)
        remainder = time_in_sec % (60 * 60)
        m = remainder // 60 
        s = remainder % 60
        return get_h(h) + get_m(m) + get_s(s)
    
    else:
        raise NotImplementedError
    
def sec2hms(time_in_sec):
    unit_s = colorize("s", color=Color.GREEN, bold=False)
    unit_m = colorize("m", color=Color.YELLOW, bold=False)
    unit_h = colorize("h", color=Color.RED, bold=False)

    def get_s(t) -> str:
        return str(t) + "s"

    def get_m(t) -> str:
        return str(t) + "m" 

    def get_h(t) -> str:
        return str(t) + "h"

    time_in_sec = int(time_in_sec)
    if time_in_sec <= 100:
        return get_s(time_in_sec)

    elif time_in_sec > 60 and time_in_sec <= (60 * 60):
        m = time_in_sec // 60
        s = time_in_sec % 60
        return get_m(m) + get_s(s)

    elif time_in_sec > (60 * 60): 
        h = time_in_sec // (60 * 60)
        remainder = time_in_sec % (60 * 60)
        m = remainder // 60 
        s = remainder % 60
        return get_h(h) + get_m(m) + get_s(s)
    
def time_str(s, simple=False):
    """
    Convert seconds to a nicer string showing days, hours, minutes and seconds
    """
    days, remainder = divmod(s, 60 * 60 * 24)
    hours, remainder = divmod(remainder, 60 * 60)
    minutes, seconds = divmod(remainder, 60)
    string = ""
    if not simple:
        if days > 0:
            string += f"{int(days):d} days, "
        if hours > 0:
            string += f"{int(hours):d} hours, "
        if minutes > 0:
            string += f"{int(minutes):d} minutes, "
        string += f"{int(seconds):d} seconds"
        return string
    else:
        if days > 0:
            string += f"{int(days):d}d"
        if hours > 0:
            string += f"{int(hours):d}:"
        if minutes > 0:
            string += f"{int(minutes):02d}:"
        string += f"{int(seconds):02d}s"
        return string


# TODO: add time,
# TODO: module name automatically
# TODO: line number
# TODO: more args, args in tuple 
class ColorLogger:
    def __init__(self, level):
        self._level = level

    # TODO
    def set_level(self, level=Union[dict, LogLevel]):
        self._level = level

    def debug(self, msg, args=None, inline=False):
        debug_print(msg, args, level=LogLevel.DEBUG, inline=inline)
    
    def info(self, msg, args=None, inline=False):
        debug_print(msg, args, level=LogLevel.INFO, inline=inline)

    def warning(self, msg, args=None, inline=False):
        debug_print(msg, args, level=LogLevel.WARNING, inline=inline)

    def error(self, msg, args=None, inline=False):
        debug_print(msg, args, level=LogLevel.ERROR, inline=inline)

    def success(self, msg, args=None, inline=False):
        debug_print(msg, args, level=LogLevel.SUCCESS, inline=inline)

    def log(self, msg, args=None, color: Optional[str] = None, inline=False):
        ''' Assignable color '''
        _color = Color.CYAN
        if color and Color.is_valid_color(color):
            _color = Color.get_color_by_name(color)

        debug_print(msg, args, color=_color, inline=inline)

    def print(self, args=None, inline=False):
        ''' print args without msg & with defaul prompt >>> '''
        debug_print("", args, color=Color.CYAN, inline=inline)

    def time(self, msg, args=None, inline=False):
        ''' log time & msg '''
        pass



''' tests '''
def test_debug_log_functions():
    print("="*10 + " every color " + "="*10)
    for c in Color:
        print(colorize(f"{c}", color=c, bold=False))
        print(colorize(f"{c}.BOLD", color=c))

    print("")
    print("="*10 + " every log level " + "="*10)
    for l in LogLevel:
        level_name = str(l)[len(LogLevel.__name__)+1:]
        debug_msg(level_name, level=l)

    print("")
    print("="*10 + " other color " + "="*10)
    debug_msg("BLUE", color=Color.BLUE)
    debug_msg("CYAN", color=Color.CYAN)
    debug_msg("GREEN", color=Color.GREEN)
    debug_msg("MAGENTA", color=Color.MAGENTA)

    print("")
    print("="*10 + " inline " + "="*10)
    debug_print("hello", args="world", inline=True)

    print("")
    print("="*10 + " newline " + "="*10)
    debug_print("hello", args="world")
    print("")

def test_pretty_print():
    args = dict(
        id=42,
        name=dict(first_name='Jimmy',
                    last_name='Deng'),
        sexual='male',
        age=30,
        info='Hello world!',
        arr=np.array([[1, 2], [3, 4]]),
        email=dict(a=['xxx', 'yyys', 'zzz'], b='bbb')
    )
    logger.debug('int:', 42, True)
    logger.debug('args:', args)


def test_format_pretty_table():
    column_names = ['Version', 'Uploaded on', 'Downloads']

    humanfriendly_releases = [
        ['1.23', '2015-05-25', '218'],
        ['1.23.1', '2015-05-26', '1354'],
        ['1.24', '2015-05-26', '223'],
        ['1.25', '2015-05-26', '4319'],
        ['1.25.1', '2015-06-02', '197'],
    ]
    print(format_pretty_table(humanfriendly_releases, column_names))

''' API Instance '''
logger = ColorLogger(level=None)


if __name__ == "__main__":
    # test_debug_log_functions()
    # test_get_space_dim()
    # test_pretty_print()
    # test_format_pretty_table()
    logger.log("dada", color="green")