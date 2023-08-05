import json
import urllib.parse as parse

from prutils.pr_utils import print_json, json_dump


def get_url_param_dict(url):
    """
    获取url上的参数，保存到dict中
    :example
        get_url_param_dict("http://p.com/query?a=1&b=2")["a"] == "1"
    :param url:
    :return:
    """
    p = parse.urlsplit(url)
    params = parse.parse_qsl(p.query, 1)
    params_dict = dict(params)
    return params_dict


def get_post_data_dict(data):
    params = parse.parse_qsl(data, 1)
    params_dict = dict(params)
    return params_dict


def print_post_data(data):
    print("data = {}".format(json_dump(get_post_data_dict(data))))


def print_url_info(url):
    url, query = url.split('?', 1)
    print('url = "{}"'.format(url))
    print("params = {}".format(json_dump(get_post_data_dict(query))))
