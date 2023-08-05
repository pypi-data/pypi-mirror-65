import re
import uuid


def get_re_first(pattern, string, flags=0):
    """
    print(get_re_first("\\d", "abc1") == "1")
    :param pattern:
    :param string:
    :param flags:
    :return:
    """
    r = re.search(pattern, string, flags)
    return r.group()


def get_re_first_subs(pattern, string, flags=0):
    r = re.search(pattern, string, flags)
    return r.groups()


def get_re_all(pattern, string, flags=0):
    r = re.findall(pattern, string, flags)
    return r


def get_re_last(pattern, string, flags=0):
    return get_re_all(pattern, string, flags)[-1]


def rand_hex32():
    return uuid.uuid4().hex

def replace(pattern, repl, string):
    return re.sub(pattern, repl, string, flags=re.I)

def replace_chinese(repl, string):
    return replace(u'([\u4e00-\u9fa5])', repl, string)
