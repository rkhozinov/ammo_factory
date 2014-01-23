import json
import requests
import unittest2
import src.ammo_factory as gen


class AmmoFactoryTest(unittest2.TestCase):
    def setUp(self):
        self.username = 'admin'
        self.password = 'admin'
        self.tenant_name = 'admin'
        self.host = '172.18.173.130:5000'

    def test_auth(self):
        token = gen.auth(self.username, self.password, self.tenant_name,
                         self.host)
        print (token)
        self.assertIsInstance(token, unicode)
        self.assertEqual(len(token), 32)

    def test_get_user_list(self):
        headers = dict()
        token = gen.auth(self.username, self.password,
                         self.tenant_name, self.host)
        headers['X-Auth-Token'] = token

        req = gen.gen_request('get', '/v3users' % token,
                              self.host, headers, body=None)
        print req

        with open("../tmp/get_user_list_ammo.txt", "w") as f:
            for x in xrange(1000):
                f.write(req)
        self.assertIsInstance(req, str)


    def test_create_60_users(self):
        headers = dict()
        token = gen.auth(self.username, self.password,
                         self.tenant_name, self.host)
        headers['X-Auth-Token'] = token
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
                req = gen.gen_request('post', '/v3/users',
                                      self.host, headers, body)
                f.write(req)
                self.assertIsInstance(req, str)
                #self.assertEqual(req.split('\n')[0],'275')

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
            ids.append(gen.create_user_and_get_id(self.username, self.password,
                                                  self.tenant_name,
                                                  self.host, body))
        with open("../tmp/delete_user_ammo.txt", "w") as f:
            headers = {}
            token = gen.auth(self.username, self.password,
                                 self.tenant_name, self.host)
            headers['X-Auth-Token'] = token
            for i in ids:
                req = gen.gen_request('delete', '/v3/users/' + i,
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
                                         "password": "admin"},
                                    "tenantName": "admin"
        }
        })
        headers = dict()
        req1 = gen.gen_request('post', '/v2.0/tokens',
                               self.host, headers, body)
        with open("../tmp/base_ammo.txt", "w") as f:
            f.write(req1)
