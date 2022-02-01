import json
from telebot import apihelper

def read_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def write_json(data, filename, indent):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=indent)


def proxy(proxy_url, type = 'HTTPS'):

    if type == 'SOCKS5':
        Proxy_URL_SOCKS5 = proxy_url
        PROXY = f'login:password@{Proxy_URL_SOCKS5}' #(the Username and password from the bought proxies)
        apihelper.proxy = {'https':'socks5:// ' + PROXY}

    elif type == 'HTTPS':
        apihelper.proxy = {'http':f'http://{proxy_url}'}
