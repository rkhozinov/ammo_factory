import json
import src.ammo_factory

username = password = tenant_name = 'admin'
host_ip = '172.18.173.130'


def test_create_60_users():
    headers = dict()
    headers['X-Auth-Token'] = src.ammo_factory.auth(username, password,
                                                    tenant_name, host_ip)
    headers['Content-Type'] = 'application/json'
    with open("../tmp/create_user_ammo.txt", "w") as f:
        for x in xrange(60):
            body = json.dumps({
                "user": {
                    "email": "qwe@qwe.com",
                    "enabled": True,
                    "name": "load_test_%d" % x,
                    "password": "swordfish"
                }
            })
            req = src.ammo_factory.gen_request('post', '/v3/users',
                                               host_ip, headers, body)
            f.write(req)


if __name__ == '__main__':
    test_create_60_users()