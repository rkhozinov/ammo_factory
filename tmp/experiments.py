r = """GET /v2.0/extensions HTTP/1.1\r
Host: 172.18.173.130:5000\r
Content-Type: application/json\r
Accept: application/xml\r
\r
"""

with open("1ammo.txt","w") as f:
            f.write(str(len(r)) + '\n')
            f.write(r)