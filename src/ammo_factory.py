from keystoneclient.v2_0 import client

AMMO_TMPL = '''\
{method} {url} HTTP/1.1\r
Host: {host}\r
User-Agent: yandex-tank/1.1.1\r
{headers}\r
\r
{body}'''

NL = '\r\n'


def auth(username, password, tenant_name, auth_url):
    keystone = client.Client(username=username,
                             password=password,
                             tenant_name=tenant_name,
                             auth_url=auth_url)
    return keystone.auth_token


def gen_request(method, url, host, headers, body=None):
    ammo = AMMO_TMPL.format(
        method=method.upper(),
        host=host,
        url=url,
        headers='\r\n'.join("%s: %s" % (n, v) for (n, v) in headers.items()),
        body=(str(body) + '\r\n') if body else '' )
    return '%s\n%s' % (len(ammo), ammo)


if __name__ == '__main__':
    print auth('admin','admin','admin','http://172.18.173.130:5000/v2.0/')

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
# {
#   "user": {
#     "username": "jqsmith",
#     "email": "john.smith@example.org",
#     "enabled": true,
#     "OS-KSADM:password": "secrete"
#   }
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


