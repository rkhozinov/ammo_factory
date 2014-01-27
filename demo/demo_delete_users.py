import sys
import requests

sys.path.append('.')
import src.ammo_factory as ammo_factory

username = password = tenant_name = 'admin'
host_ip = '172.18.173.130:5000'


def get_users_ids(login, password, tenant_name, host_ip):
    auth_url = 'http://{ip}/v2.0'.format(ip=host_ip)
    v3_users = 'http://{ip}/v3/users'.format(ip=host_ip)
    headers = {
        'X-Auth-Token': ammo_factory.auth(login, password, tenant_name,
                                          auth_url),
        'Content-Type': 'application/json'}
    r = requests.get(v3_users, headers=headers)

    return {user['name']: user['id'] for user in r.json()['users']}


def test_delete_existing_users():
    all_id = get_users_ids(username, password, tenant_name, host_ip)
    needed_id = [temp_id for (user, temp_id) in all_id.items() if
                 'load_test_' in user]
    headers = {'X-Auth-Token': ammo_factory.auth(username, password,
                                                 tenant_name, host_ip),
               'Content-Type': 'application/json'}

    with open("delete_existing_users.txt", "w") as f:
        for i in needed_id:
            req = ammo_factory.gen_request('delete', '/v3/users/%s' % i,
                                           host_ip, headers)
            f.write(req)

    with open('load.ini', 'w') as f:
        f.write('[phantom]\n')
        f.write('address=%s\n' % host_ip)
        f.write('rps_schedule=const(12, 5s)\n')

    req_count = len(needed_id)
    print "Generated %d requests" % req_count
    if req_count:
        print "Request example:"
        print req


if __name__ == '__main__':
    test_delete_existing_users()