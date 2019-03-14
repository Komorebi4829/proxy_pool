import os
import time
import random
import requests
import importlib


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', maxsplit=1)
    except ValueError as err:
        raise ImportError("{} doesn't look like a module path".format(dotted_path)) from err

    module = importlib.import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError("Module '{}' does not define a '{}' attribute/class".format(module_path, class_name)) from err


def singleton(cls, *args, **kw):
    _instances = {}

    def get_instance():
        if cls not in _instances:
            _instances[cls] = cls(*args, **kw)
        return _instances[cls]

    return get_instance


def check(proxy):
    p = {
        "http": "http://{}".format(proxy),
    }
    url = 'http://httpbin.org/ip'
    try:
        r = requests.get(url, proxies=p, timeout=10, verify=False)
        if r.status_code == 200 and r.json().get("origin"):
            return True
    except Exception as e:
        return False


def cached_url(url, cache_path, cache_filename, refresh=False):
    """
    缓存 url, 如果已有缓存文件: 如果不强制刷新 则使用缓存,
                        否则请求网页并缓存
         如果没有缓存则请求网页并缓存

    :param url:
    :param cache_path: 缓存的目录
    :param cache_filename: 缓存的文件名
    :param refresh: 是否强制刷新(忽略缓存)
    :return:
    """
    if not os.path.exists(cache_path):
        os.makedirs(cache_path)
    if '/' in cache_filename:
        cache_filename = cache_filename.replace('/', '-')

    path = os.path.join(cache_path, cache_filename)

    if os.path.exists(path):
        if refresh is False:
            print('缓存已存在，使用缓存')
            content = _load_cache(path)
            return content
        else:
            print('缓存已存在, 强制刷新')
            r = _request_and_save(url, path)
    else:
        time.sleep(3)
        r = _request_and_save(url, path)
    return r.content


def _load_cache(path):
    with open(path, 'rb') as f:
        content = f.read()
    return content


def _request_and_save(url, path):
    req = requests.get(url)
    with open(path, 'wb') as f:
        f.write(req.content)
    return req
