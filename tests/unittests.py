import json
import unittest2
from src.ammo_factory import create_user_and_get_id, gen_request, auth


class AmmoFactoryTest(unittest2.TestCase):
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
                req = gen_request('post', '/v3/users',
                                  self.host, headers, body)
                f.write(req)

    def test_delete_60_users(self):
        ids = []
        for x in xrange(60):
            body = json.dumps({
                "user": {
                    "email": "qwe@qwe.com",
                    "enabled": True,
                    "name": "load_test_delete_%d" % x,
                    "password": "swordfish"
                }
            })
            ids.append(create_user_and_get_id(self.username, self.password,
                                              self.tenant_name,
                                              self.host, body))
        with open("../tmp/delete_user_ammo.txt", "w") as f:
            headers = {'X-Auth-Token': auth(self.username, self.password,
                                            self.tenant_name, self.host),
                       'Content-Type': 'application/json'}

            for i in ids:
                req = gen_request('delete', '/v3/users/' + i,
                                  self.host, headers)
                f.write(req)

    def test_auth_request(self):
        """
        POST /v2.0/tokens HTTP/1.1
        Host: identity.api.openstack.org
        Content-Type: application/json
        Accept: application/xml
        """
        body = json.dumps({"auth": {"passwordCredentials":
                                        {"username": "admin",
                                         "password": "admin"
                                        }, "tenantName": "admin"}})
        headers = dict()
        req1 = gen_request('post', '/v2.0/tokens',
                           self.host, headers, body)
        with open("../tmp/base_ammo.txt", "w") as f:
            f.write(req1)
