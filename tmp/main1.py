# coding=utf-8
"""
316 good
POST / HTTP/1.0
Host: 172.18.169.204
User-Agent: ytank
X-Amz-Date: 20131227T115219Z
X-Amz-Target: DynamoDB_20120810.GetItem
Accept-Encoding: identity
Content-Type: application/x-amz-json-1.0

{"TableName": "load_spam_table", "Key": {"user_id": {"S": "user@mail.com"}, "date_message_id": {"S": "2013-12-31#123456"}}}
"""

#with open('/home/vkhlyuenv/work/tank_exp/ammo.txt','w') as f:
with open('ammo.txt','w') as f:
    req = "GET / HTTP/1.1\r\n"
    req += "Host: www.google.com\r\n"
    req += "User-Agent: yandex-tank/1.1.1\r\n"
    req += "Accept: text/html\r\n"
    req += "Connection: close\r\n"
    req += "\r\n"
    for x in xrange(1000):
        f.write(str(len(req)) + '\n')
        f.write(req)