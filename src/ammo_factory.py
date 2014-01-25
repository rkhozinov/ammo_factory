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


def auth(login, password, tenant_name, host_ip):
    if not 'http' in host_ip:
        host_ip = 'http://{ip}/v2.0'.format(ip=host_ip)
    keystone = client.Client(username=login,
                             password=password,
                             tenant_name=tenant_name,
                             auth_url=host_ip)
    return keystone.auth_token


def create_user_and_get_id(login, password, tenant_name, host_ip, user_json):
    auth_url = 'http://{ip}/v2.0'.format(ip=host_ip)
    v3_users = 'http://{ip}/v3/users'.format(ip=host_ip)
    headers = {'X-Auth-Token': auth(login, password, tenant_name, auth_url),
               'Content-Type': 'application/json'}
    r = requests.post(v3_users, data=user_json, headers=headers)
    return r.json()['user']['id']


def get_users_ids(login, password, tenant_name, host_ip):
    auth_url = 'http://{ip}/v2.0'.format(ip=host_ip)
    v3_users = 'http://{ip}/v3/users'.format(ip=host_ip)
    headers = {'X-Auth-Token': auth(login, password, tenant_name, auth_url),
               'Content-Type': 'application/json'}
    r = requests.get(v3_users, headers=headers)
    return {user['name']: user['id'] for user in r.json()['users']}


def gen_request(method, url, host, headers, body=None):
    assert isinstance(headers, dict)
    assert method.upper() in ['GET', 'POST', 'DELETE', 'PUT']
    assert not body or isinstance(body, str)
    body = body if body else ''

    ammo = AMMO_TMPL.format(
        method=method.upper(), host=host, url=url,
        headers='\r\n'.join("%s: %s" % (n, v) for (n, v) in headers.items()),
        body=(body.replace("'", '"') + '\r\n') if body else '')
    return '%s\n%s' % (len(ammo), ammo)


if __name__ == '__main__':
    print get_users_ids('admin', 'admin', 'admin', '172.18.173.130:5000')

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


