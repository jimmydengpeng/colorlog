#######################################################################
# Copyright (C) 2023 Jimmy Deng (jimmydengpeng@gmail.com)             #
# Permission given to modify the code as long as you keep this        #
# declaration at the top                                              #
#######################################################################

from enum import IntEnum
from time import time
from typing import Optional, Union, List
from .utils import colorize, pretty_dict

'''TODO
- [x] 自动根据说所打印的字符长度判断是否换行
- [x] 设置全局的开关，根据level控制是否打印
- [ ] 允许打印单个参数，不带提示字符串
- [ ] add time,
- [ ] module name automatically
- [ ] line number
- [ ] more args, args in tuple 
'''

"""@DOCUMENT:

A log contains:
[PROMPT] <Optional>[TIME] [User input massage] [args]

The printing process is devided into 2 parts:
1. print a colored PROMPT
2. print the args
"""

class COLOR(IntEnum):
    # names    =    values
    BLACK      =    30
    RED        =    31
    GREEN      =    32
    YELLOW     =    33
    BLUE       =    34
    MAGENTA    =    35     #品红
    CYAN       =    36     #蓝绿/青
    WHITE      =    37
    CRIMSON    =    38
    GRAY       =    90

    @classmethod
    def is_valid(cls, name: str) -> bool:
        for color in cls:
            if name.upper() == color.name:
                return True
        return False
    
    @classmethod
    def get_by_name(cls, name: str):
        assert COLOR.is_valid(name)
        for color in cls:
            if name.upper() == color.name:
                return color


'''
All Log Levels:
-----------------------
| DEBUG    | debug    |
| INFO     | info     |
| WARNING  | warning  |
| SUCCESS  | success  |
| ERROR    | error    |
-----------------------
'''
class LOG_LEVEL(IntEnum):
    DEBUG   = 0
    INFO    = 1
    WARNING = 2
    SUCCESS = 3
    ERROR   = 4

    @classmethod
    def is_valid(cls, name: str) -> bool:
        for member in cls:
            if name.upper() == member.name:
                return True
        return False


LEVEL_COLOR = {
    LOG_LEVEL.SUCCESS: COLOR.GREEN,
    LOG_LEVEL.DEBUG:   COLOR.MAGENTA,
    LOG_LEVEL.INFO:    COLOR.BLUE,
    LOG_LEVEL.WARNING: COLOR.YELLOW,
    LOG_LEVEL.ERROR:   COLOR.RED
}

PROMPT_SYMBOL = {
    # Enum members are hashable & can be used as dictionary keys
    LOG_LEVEL.SUCCESS:  "✔", 
    LOG_LEVEL.DEBUG:    "",
    LOG_LEVEL.INFO:     "",
    LOG_LEVEL.WARNING:  "⚠",
    LOG_LEVEL.ERROR:    "✖"
}
'''alternatives:  ➤  ☞ ⚑  ◎ ⊙  ⇨ ▶'''


class ColorLogger:
    def __init__(
            self,
            level: str = "DEBUG",
            type_hinting: bool = True,
            max_line_len: int = 70
        ):
        if LOG_LEVEL.is_valid(level):
            self._level_threshold = LOG_LEVEL[level]
        else:
            self.warning(f"Invalid log level {str}, set to default 'DEBUG'!")
            self._level_threshold = LOG_LEVEL.DEBUG
        self._type_hinting = type_hinting
        self.MAX_LINE_LEN = max_line_len

    def _log(
            self,
            msg: str,
            args=None,
            level: LOG_LEVEL = None,
            color: Optional[COLOR] = None,
            inline: bool = None
        ):

        # TODO: update level specific logging policy
        if level < self._level_threshold:
            return

        if inline == None:
            inline = self._if_inline(args)
        self._log_prompt_msg(msg, level, color=color, inline=inline)
        self._log_args(args)
        if self._type_hinting:
            self._log_type(args)


    # TODO: update policy
    def _if_inline(self, args) -> bool:
        if isinstance(args, dict):
            return False
        else:
            try:
                return len(str(args)) < self.MAX_LINE_LEN
            except:
                return False

    def _log_prompt_msg(
            self,
            msg: str,
            level: LOG_LEVEL,
            inline: bool,
            bold: bool = False,
            color: Optional[COLOR] = None
        ):
        """
        @return: symbol + msg (same color)
        e.g.:
        ✔ [SUCCESS] SUCCESS_msg
         [DEBUG] DEBUG_msg
         [INFO] INFO_msg
        ⚠ [WARNING] WARNING_msg
        ✖ [ERROR] ERROR_msg
        """

        '''Allow customed color or using LOG_LEVEL Color'''
        color_code = color.value if color else LEVEL_COLOR[level].value

        '''prompt'''
        text = PROMPT_SYMBOL[level] + ' [' + level.name + ']'
        prompt = colorize(text, color=color_code, bold=True)

        msg += ': ' if inline else ''

        '''inline'''
        if inline != None:
            end = '' if inline else '\n'

        print(prompt, colorize(msg, color=color_code, bold=bold), end=end)

    def _log_type(self, args):
        # print(colorize(type(args), Color.GRAY.value, highlight=True))
        # print(colorize(type(args), Color.GRAY.value, highlight=False))
        print(colorize(type(args), COLOR.BLACK.value, highlight=True))
        # print(colorize(type(args), Color.BLACK.value, highlight=False))

    def _log_args(
            self,
            args
        ):
        ''' pretty print dict '''
        if isinstance(args, dict):
            args = pretty_dict(args)

        if args is not None:
            print(args)


    """APIs"""
    # TODO
    def set_level(self, level=Union[str, List[str], LOG_LEVEL]):
        if isinstance(level, str):
            self._level_threshold = LOG_LEVEL[level]
        elif isinstance(level, LOG_LEVEL):
            self._level_threshold = level
        elif isinstance(level, list):
            # for lev in level:
            raise NotImplementedError()
        else:
            raise NotImplementedError()

    def set_type_hinting(self, type_hinting: bool):
        self._type_hinting = type_hinting

    def debug(self, msg, args=None, inline=None):
        self._log(msg, args, level=LOG_LEVEL.DEBUG, inline=inline)
    
    def info(self, msg, args=None, inline=None):
        self._log(msg, args, level=LOG_LEVEL.INFO, inline=inline)

    def warning(self, msg, args=None, inline=None):
        self._log(msg, args, level=LOG_LEVEL.WARNING, inline=inline)

    def error(self, msg, args=None, inline=None):
        self._log(msg, args, level=LOG_LEVEL.ERROR, inline=inline)

    def success(self, msg, args=None, inline=None):
        self._log(msg, args, level=LOG_LEVEL.SUCCESS, inline=inline)


    # TODO
    def log(self, msg, args=None, color: Optional[str] = None, inline=True):
        ''' Assignable color '''
        _color = COLOR.CYAN
        if color and COLOR.is_valid(color):
            _color = COLOR.get_by_name(color)

        self._log(msg, args, color=_color, inline=inline)

    def print(self, args=None, inline=False):
        ''' print args without msg & with defaul prompt >>> '''
        self._log("", args, color=COLOR.CYAN, inline=inline)

    def time(self, msg, args=None, inline=False):
        ''' log time & msg '''
        pass

