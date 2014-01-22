import requests
import unittest2
import src.ammo_factory as gen


class AmmoFactoryTest(unittest2.TestCase):
    def setUp(self):
        self.url = 'http://172.18.173.130:5000/v2.0/'
        self.username = 'admin'
        self.password = 'admin'
        self.tenant_name = 'admin'
        self.host = '172.18.173.130:5000'

    def test_auth(self):
        token = gen.auth(self.username, self.password, self.tenant_name, self.url)
        print (token)
        self.assertIsInstance(token,unicode)
        self.assertEqual(len(token), 32)

    def test_get_user_list(self):
        headers = dict()
        headers['X-Auth-Token'] = gen.auth(self.username, self.password, self.tenant_name, self.url)
        req = gen.gen_request('get', 'v2.0/users',
                              self.host, headers, body=None)

        with open("../tmp/ammo.txt","w") as f:
            f.write(req)
            f.write(req)
        print req
        self.assertIsInstance(req,str)
        #self.assertEqual(req.split('\n')[0],'154')


    def test_get_user(self):
        headers = dict()
        headers['X-Auth-Token'] = gen.auth(self.username, self.password, self.tenant_name, self.url)
        body = {
            "user": {
                "username": "jqsmith",
                "email": "john.smith@example.org",
                "enabled": 'true',
                "OS-KSADM:password": "secrete"
            }
        }

        req = gen.gen_request('get', 'v2.0/users',
                              self.host, headers, body)
        with open("../tmp/ammo.txt","w") as f:
            f.write(req)
            f.write(req)
        print req
        self.assertIsInstance(req,str)
        #self.assertEqual(req.split('\n')[0],'275')
