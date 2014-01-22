def create(url, headers, body):
    """
    # Method: POST
    # URL: http://host_address/v2.0/users
    {
      "user": {
        "username": "jqsmith",
        "email": "john.smith@example.org",
        "enabled": true,
        "OS-KSADM:password": "secrete"
      }
    }
    """


def get(url, headers, body):
    """
# Method: GET
# URL: http://host_address/v2.0/users
{
  "user": {
    "username": "jqsmith",
    "email": "john.smith@example.org",
    "enabled": true,
    "OS-KSADM:password": "secrete"
  }
}
"""


def gen_create(url, headers, body):
    """
    # Method: POST
    # URL: http://host_address/v2.0/users
    {
      "user": {
        "username": "jqsmith",
        "email": "john.smith@example.org",
        "enabled": true,
        "OS-KSADM:password": "secrete"
      }
    }
    """


def gen_delete(url, headers, body):
    """
    # Method: DELETE
    # URL: http://host_address/v2.0/users{/userId}
    """


def gen_update(url, headers, body):
    """
    # Method: POST
    # URL: http://host_address/v2.0/users{/userId}
    {
      "user": {
        "username": "jqsmith",
        "email": "john.smith@example.org",
        "enabled": true,
        "OS-KSADM:password": "secrete"
      }
    }
    """


def auth(username, password, auth_url):
    token = None

    return token


class Request(object):
    def __init__(self, url, headers, body):
        self.url = url
        self.headers = headers
        self.body = body

    def __str__(self):
        return self.headers + self.body

    def __unicode__(self):
        return self.__str__()