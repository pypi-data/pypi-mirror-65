import hashlib
import json
import logging
import os
import shutil
import sys
import time


def init_log(level=logging.DEBUG, filename=None, filemode="w"):
    """

    :param level:
    :param filename: 日志文件路径，默认为None不写文件，
    :param filemode: 可选w覆盖模式,或a添加模式
    """
    logging.basicConfig(level=level,
                        format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                        filename=filename,
                        filemode=filemode
                        )


def hello():
    print("hello args[%s]" % (sys.argv,))


def world():
    print("world args[%s]" % (sys.argv,))


def md5(data):
    m = hashlib.md5()
    m.update(data)
    return m.hexdigest()


def json_dump(data):
    return json.dumps(data, indent=4)


def print_json(data):
    print(json_dump(data))


def get_timestamp13():
    return str(int(time.time() * 1000))


def get_timestamp10():
    return str(int(time.time()))


def read_file(file_path, mode="r"):
    with open(file_path, mode) as f:
        return f.read()


def save_file(file_path, mode=""):
    with open(file_path, mode) as f:
        return f.write()


def get_appdata_dir(appname):
    import sys
    from os import path, environ
    if sys.platform == 'darwin':
        from AppKit import NSSearchPathForDirectoriesInDomains
        # http://developer.apple.com/DOCUMENTATION/Cocoa/Reference/Foundation/Miscellaneous/Foundation_Functions/Reference/reference.html#//apple_ref/c/func/NSSearchPathForDirectoriesInDomains
        # NSApplicationSupportDirectory = 14
        # NSUserDomainMask = 1
        # True for expanding the tilde into a fully qualified path
        appdata = path.join(NSSearchPathForDirectoriesInDomains(14, 1, True)[0], appname)
    elif sys.platform == 'win32':
        appdata = path.join(environ['APPDATA'], appname)
    else:
        appdata = path.expanduser(path.join("~", "." + appname))
    return appdata


def make_path_by_relfile(refile, filename):
    return os.path.abspath(os.path.join(os.path.dirname(refile), filename))


class DictToObject(object):

    def __init__(self, dictionary):
        def _traverse(key, element):
            if isinstance(element, dict):
                return key, DictToObject(element)
            else:
                return key, element

        objd = dict(_traverse(k, v) for k, v in dictionary.items())
        self.__dict__.update(objd)


def rm_dir(dirpath):
    try:
        shutil.rmtree(dirpath)
    except FileNotFoundError:
        pass


def rm_file(filepath):
    try:
        os.remove(filepath)
    except FileNotFoundError:
        pass
