import json
import requests
import unittest2
from src.ammo_factory import gen_request, auth


class AmmoFactoryTest(unittest2.TestCase):
    @staticmethod
    def create_user_and_get_id(login, password, tenant_name, host_ip,
                               user_json):
        auth_url = 'http://{ip}/v2.0'.format(ip=host_ip)
        v3_users = 'http://{ip}/v3/users'.format(ip=host_ip)
        headers = {
        'X-Auth-Token': auth(login, password, tenant_name, auth_url),
        'Content-Type': 'application/json'}
        r = requests.post(v3_users, data=user_json, headers=headers)
        return r.json()['user']['id']

    @staticmethod
    def get_users_ids(login, password, tenant_name, host_ip):
        auth_url = 'http://{ip}/v2.0'.format(ip=host_ip)
        v3_users = 'http://{ip}/v3/users'.format(ip=host_ip)
        headers = {
            'X-Auth-Token': auth(login, password, tenant_name,
                                              auth_url),
            'Content-Type': 'application/json'}
        r = requests.get(v3_users, headers=headers)
        return {user['name']: user['id'] for user in r.json()['users']}

    def setUp(self):
        self.username = 'admin'
        self.password = 'admin'
        self.tenant_name = 'admin'
        self.host = '172.18.173.130:5000'

    def test_auth(self):
        token = auth(self.username, self.password, self.tenant_name,
                     self.host)
        print token
        self.assertIsInstance(token, unicode)
        self.assertEqual(len(token), 32)

    def test_get_user_list(self):
        headers = dict()
        headers['X-Auth-Token'] = auth(self.username, self.password,
                                       self.tenant_name, self.host)
        headers['Content-Type'] = 'application/json'

        req = gen_request('get', '/v3/users',
                          self.host, headers, body=None)
        with open("../tmp/get_user_list_ammo.txt", "w") as f:
            for x in xrange(60):
                f.write(req)
        self.assertIsInstance(req, str)

    def test_create_60_users(self):
        headers = dict()
        headers['X-Auth-Token'] = auth(self.username, self.password,
                                       self.tenant_name, self.host)
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
                headers['Content-Length'] = len(body)
                req = gen_request('post', '/v3/users',
                                  self.host, headers, body)
                f.write(req)

    def test_delete_already_created_users(self):
        ids = self.get_users_ids(self.username, self.password,
                            self.tenant_name, self.host)
        fetched_ids = [temp_id for (user, temp_id) in ids.items() if
                       'load_test_' in user]
        headers = dict()
        headers['X-Auth-Token'] = auth(self.username, self.password,
                                       self.tenant_name, self.host)
        headers['Content-Type'] = 'application/json'
        with open("../tmp/delete_existing_users.txt", "w") as f:
            for i in fetched_ids:
                req = gen_request('delete', '/v3/users/%s' % i,
                                  self.host, headers)
                f.write(req)

    # def test_create_and_delete_60_users(self):
    #     ids = []
    #     for x in xrange(60):
    #         body = json.dumps({
    #             "user": {
    #                 "email": "qwe@qwe.com",
    #                 "enabled": True,
    #                 "name": "load_test_delete_%d" % x,
    #                 "password": "swordfish"
    #             }
    #         })
    #         ids.append(create_user_and_get_id(self.username, self.password,
    #                                           self.tenant_name,
    #                                           self.host, body))
    #     with open("../tmp/delete_user_ammo.txt", "w") as f:
    #         headers = {'X-Auth-Token': auth(self.username, self.password,
    #                                         self.tenant_name, self.host),
    #                    'Content-Type': 'application/json'}
    #
    #         for i in ids:
    #             req = gen_request('delete', '/v3/users/' + i,
    #                               self.host, headers)
    #             f.write(req)
    #
    # def test_auth_request(self):
    #     """
    #     POST /v2.0/tokens HTTP/1.1
    #     Host: identity.api.openstack.org
    #     Content-Type: application/json
    #     Accept: application/xml
    #     """
    #     body = json.dumps({"auth": {"passwordCredentials":
    #                                     {"username": "admin",
    #                                      "password": "admin"
    #                                     }, "tenantName": "admin"}})
    #     headers = dict()
    #     req1 = gen_request('post', '/v2.0/tokens',
    #                        self.host, headers, body)
    #     with open("../tmp/base_ammo.txt", "w") as f:
    #         f.write(req1)
