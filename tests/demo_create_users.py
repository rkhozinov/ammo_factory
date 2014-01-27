import json
import sys

sys.path.append('.')
from src import ammo_factory

username = password = tenant_name = 'admin'
host_ip = '172.18.173.130:5000'


def test_create_60_users():
    headers = dict()
    headers['X-Auth-Token'] = ammo_factory.auth(username, password,
                                                tenant_name, host_ip)
    headers['Content-Type'] = 'application/json'
    with open("tmp/create_user_ammo.txt", "w") as f:
        for x in xrange(60):
            body = json.dumps({
                "user": {
                    "email": "qwe@qwe.com",
                    "enabled": True,
                    "name": "load_test_%d" % x,
                    "password": "swordfish"
                }
            })
            headers['Content-Length'] = len(body)
            req = ammo_factory.gen_request('post', '/v3/users',
                                           host_ip, headers, body)
            f.write(req)

    with open('tmp/load.ini', 'w') as f:
        f.write('[phantom]\n')
        f.write('address=%s\n' % host_ip)
        f.write('rps_schedule=const(1, 1m)')


if __name__ == '__main__':
    test_create_60_users()