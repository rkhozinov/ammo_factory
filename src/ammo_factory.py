import json
from keystoneclient.v2_0 import client
import requests

AMMO_TMPL = '''\
{method} {url} HTTP/1.1\r
Host: {host}\r
User-Agent: yandex-tank/1.1.1\r
{headers}\r
\r
{body}'''

NL = '\r\n'


def auth(login, password, tenant_name, auth_url):
    if not 'http' in auth_url:
        auth_url = 'http://{ip}/v2.0'.format(ip=auth_url)
    keystone = client.Client(username=login,
                             password=password,
                             tenant_name=tenant_name,
                             auth_url=auth_url)
    return keystone.auth_token


def create_user_and_get_id(login, password, tenant_name, host_ip, user_json):
    """
    172.18.173.130:5000
    """
    auth_url = 'http://{ip}/v2.0'.format(ip=host_ip)
    v3_users = 'http://{ip}/v3/users'.format(ip=host_ip)
    headers = {}
    headers['X-Auth-Token'] = auth(login, password, tenant_name, auth_url)
    headers['Content-Type'] = 'application/json'
    r = requests.post(v3_users, data=user_json, headers=headers)
    print r.json()['user']['id']
    return r.json()['user']['id']


def gen_request(method, url, host, headers, body=None):
    assert isinstance(headers, dict)
    assert method.upper() in ['GET', 'POST', 'DELETE', 'PUT']
    assert not body or isinstance(body, str)
    body = body if body else ''

    headers['Content-Type'] = 'application/json'
    headers['Content-length'] = str(len(body))
    headers['Accept'] = 'application/xml'

    ammo = AMMO_TMPL.format(
        method=method.upper(), host=host, url=url,
        headers='\r\n'.join("%s: %s" % (n, v) for (n, v) in headers.items()),
        body=(body.replace("'", '"') + '\r\n') if body else '')
    return '%s\n%s' % (len(ammo), ammo)


if __name__ == '__main__':
    print auth('admin', 'admin', 'admin', 'http://172.18.173.130:5000/v2.0/')

# def create(url, headers, body):
#     """
#     # Method: POST
#     # URL: http://host_address/v2.0/users
#     {
#       "user": {
#         "username": "jqsmith",
#         "email": "john.smith@example.org",
#         "enabled": true,
#         "OS-KSADM:password": "secrete"
#       }
#     }
#     """
#
#
# def get(url, headers, body):
#     """
# # Method: GET
# # URL: http://host_address/v2.0/users
# }
# """
#
#
# def gen_create(url, headers, body):
#     """
#     # Method: POST
#     # URL: http://host_address/v2.0/users
#     {
#       "user": {
#         "username": "jqsmith",
#         "email": "john.smith@example.org",
#         "enabled": true,
#         "OS-KSADM:password": "secrete"
#       }
#     }
#     """
#
#
# def gen_delete(url, headers, body):
#     """
#     # Method: DELETE
#     # URL: http://host_address/v2.0/users{/userId}
#     """
#
#
# def gen_update(url, headers, body):
#     """
#     # Method: POST
#     # URL: http://host_address/v2.0/users{/userId}
#     {
#       "user": {
#         "username": "jqsmith",
#         "email": "john.smith@example.org",
#         "enabled": true,
#         "OS-KSADM:password": "secrete"
#       }
#     }
#     """


