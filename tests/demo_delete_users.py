import json
from src.ammo_factory import auth, gen_request, get_users_ids

username = password = tenant_name = 'admin'
host_ip = '172.18.173.130'


def test_delete_already_created_users():
    ids = get_users_ids(username, password, tenant_name, host_ip)
    fetched_ids = [temp_id for (user, temp_id) in ids.items() if
                   'load_test_' in user]
    headers = dict()
    headers['X-Auth-Token'] = auth(username, password, tenant_name, host_ip)
    headers['Content-Type'] = 'application/json'
    with open("../tmp/delete_existed_users.txt", "w") as f:
        for i in fetched_ids:
            req = gen_request('delete', '/v3/users/%s' % i, host_ip, headers)
            f.write(req)


if __name__ == '__main__':
    test_delete_already_created_users()