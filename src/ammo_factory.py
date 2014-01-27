from keystoneclient.v2_0 import client

AMMO_TMPL = '''\
{method} {url} HTTP/1.1\r
Host: {host}\r
User-Agent: yandex-tank/1.1.1\r
{headers}\r
\r
{body}\r
'''

NL = '\r\n'


def auth(login, password, tenant_name, host_ip):
    if not 'http' in host_ip:
        host_ip = 'http://{ip}/v2.0'.format(ip=host_ip)
    keystone = client.Client(username=login,
                             password=password,
                             tenant_name=tenant_name,
                             auth_url=host_ip)
    return keystone.auth_token


def gen_request(method, url, host, headers, body=None):
    assert isinstance(headers, dict)
    assert not body or isinstance(body, str)
    body = body if body else ''

    ammo = AMMO_TMPL.format(
        method=method.upper(), host=host, url=url,
        headers=NL.join("%s: %s" % (n, v) for (n, v) in headers.items()),
        body=(body.replace("'", '"') + NL) if body else '')
    return '%s\n%s' % (len(ammo), ammo)


if __name__ == '__main__':
    pass