import requests
import json


def post_request(url, headers, data, params=None):
    """

    :param url:
    :param headers:(optional) Dictionary of HTTP Headers to send with the
        :class:`Request`.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like object
        to send in the body of the :class:`Request`.
    :param params: (optional) Dictionary or bytes to be sent in the query
        string for the :class:`Request`. 即键值对。如：http://ip:port?name=zhangsan&pwd=123456
    :return:
    """
    r = requests.post(url=url, headers=headers, data=data, params=params)
    #report = r.json()
    return r


def get_request(url, headers, data, params=None):
    """

    :param url:
    :param headers:(optional) Dictionary of HTTP Headers to send with the
        :class:`Request`.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like object
        to send in the body of the :class:`Request`.
    :param params: (optional) Dictionary or bytes to be sent in the query
        string for the :class:`Request`. 即键值对。如：http://ip:port?name=zhangsan&pwd=123456
    :return:
    """
    r = requests.get(url=url, headers=headers, data=data, params=params)
    #report = r.json()
    return r


def run(method, url=None, headers=None, data=None, params=None):
    print('【method】', method)
    r = None
    if method == 'post':
        r = post_request(url, headers, data, params)
    elif method == 'get':
        r = get_request(url, headers, data, params)
    else:
        print('method错误！！！')
    return r


if __name__ == '__main__':
    r1 = run('get', 'http://localhost:8080/noah_web/apidevice/ptl/devices', '')     # 本例为查询ptl设备
    r1 = run('get', 'http://192.168.1.57:8081/noah_web/apidevice/ptl/devices', '')     # 本例为查询ptl设备
    print(r1.json())
