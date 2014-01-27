import sys

sys.path.append('.')
import src.ammo_factory

username = password = tenant_name = 'admin'
host_ip = '172.18.173.130:5000'


def test_delete_already_created_users():
    ids = src.ammo_factory.get_users_ids(username, password, tenant_name,
                                         host_ip)
    fetched_ids = [temp_id for (user, temp_id) in ids.items() if
                   'load_test_' in user]
    headers = dict()
    headers['X-Auth-Token'] = src.ammo_factory.auth(username, password,
                                                    tenant_name, host_ip)
    headers['Content-Type'] = 'application/json'
    with open("../tmp/delete_existed_users.txt", "w") as f:
        for i in fetched_ids:
            req = src.ammo_factory.gen_request('delete', '/v3/users/%s' % i,
                                               host_ip, headers)
            f.write(req)

    with open('load.ini', 'w') as f:
        f.write('[phantom]\n')
        f.write('address=%s\n' % host_ip)
        f.write('rps_schedule=const(1, 1m)')


if __name__ == '__main__':
    test_delete_already_created_users()