import json, yaml



def colorize(string: str, color: int, bold=True, highlight=False) -> str:
    """
    @return: a string wrapped with ANSI ESC & COLOR CODE:
                \x1b[31;1m {str} \x1b[0m
                ----====== ----- =======
                     -- COLOR CODE
                        - TEXT DECORATION
                         - Finishing symbol
                ESC  CSI    str   reset
    """
    csi = []
    color_code = color+10 if highlight else color
    csi.append(str(color_code))
    if bold: csi.append('1')
    return f"\x1b[{';'.join(csi)}m{string}\x1b[0m"
    # return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)


class BASE_ENUM:
    @classmethod
    def is_valid(cls, name: str) -> bool:
        for color in cls:
            if name.upper() == color.name:
                return True
        return False
    
    @classmethod
    def get_by_name(cls, name: str):
        assert Color.is_valid(name)
        for color in cls:
            if name.upper() == color.name:
                return color





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

#TODO
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


