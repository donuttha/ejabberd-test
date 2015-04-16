
__author__ = 'nuttha'


import requests
from requests.auth import HTTPBasicAuth

server = "localhost"
virtualhost = "localhost"
url = "http://%s:5280/admin/server/%s/users/" % (server, virtualhost)
print url
auth = HTTPBasicAuth("admin@localhost", "123456")
data = {
    'newusername': "user_test_post_321",
    'newuserpassword': "123456",
    'addnewuser': "Add User"
}
resp = requests.post(url, data=data, auth=auth)

print url
print resp.content
import sleekxmpp
# import xmpp
# client = xmpp.Client('localhost',debug=[])
# client.connect(server=('localhost',5222))

assert resp.status_code == 200