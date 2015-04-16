from django.shortcuts import render
# -*- coding: utf-8 -*-
__author__ = 'nuttha'


import requests
from requests.auth import HTTPBasicAuth

server = "localhost"
virtualhost = "localhost"
url = "http://%s:5280/admin/server/%s/users/" % (server, virtualhost)
print url
# auth = HTTPBasicAuth("admin@localhost", "123456")
auth = HTTPBasicAuth("admin@localhost", "123456")
data = {
    'newusername': "user_test_post_123",
    'newuserpassword': "123456",
    'addnewuser': "Add User"
}
resp = requests.post(url, data=data, auth=auth)

import sleekxmpp
from sleekxmpp import ClientXMPP

xmpp = ClientXMPP('admin@localhost', '123456')
xmpp.connect()
xmpp.process(block=False)

username = "nuttha@localhost"
domain= "localhost"
password = "123456"

xmpp = ClientXMPP('nuttha@23perspective.com', '123456')
xmpp.connect()
xmpp.process(block=False)

host = 'http://chat-en.shoppening.com:5280/http-bind'
username = '1406523281117@chat-en.shooppening.com'
password = 'qqqqqqqq'

# import logging
# from sleekxmpp import ClientXMPP
# from sleekxmpp.exceptions import IqError, IqTimeout
#
#
# # import xmpp
# # client = xmpp.Client('localhost',debug=[])
# # client.connect(server=('localhost',5222))
#
# class EchoBot(ClientXMPP):
#
#     def __init__(self, jid='admin@localhost', password='123456'):
#         ClientXMPP.__init__(self, jid, password)
#
#         self.add_event_handler("session_start", self.session_start)
#         self.add_event_handler("message", self.message)
#
#         # If you wanted more functionality, here's how to register plugins:
#         # self.register_plugin('xep_0030') # Service Discovery
#         # self.register_plugin('xep_0199') # XMPP Ping
#
#         # Here's how to access plugins once you've registered them:
#         # self['xep_0030'].add_feature('echo_demo')
#
#         # If you are working with an OpenFire server, you will
#         # need to use a different SSL version:
#         # import ssl
#         # self.ssl_version = ssl.PROTOCOL_SSLv3
#
#     def session_start(self, event):
#         self.send_presence()
#         self.get_roster()
#
#         # Most get_*/set_* methods from plugins use Iq stanzas, which
#         # can generate IqError and IqTimeout exceptions
#         #
#         # try:
#         #     self.get_roster()
#         # except IqError as err:
#         #     logging.error('There was an error getting the roster')
#         #     logging.error(err.iq['error']['condition'])
#         #     self.disconnect()
#         # except IqTimeout:
#         #     logging.error('Server is taking too long to respond')
#         #     self.disconnect()
#
#     def message(self, msg):
#         if msg['type'] in ('chat', 'normal'):
#             msg.reply("Thanks for sending\n%(body)s" % msg).send()
#
#
# if __name__ == '__main__':
#     # Ideally use optparse or argparse to get JID,
#     # password, and log level.
#
#     logging.basicConfig(level=logging.DEBUG,
#                         format='%(levelname)-8s %(message)s')
#
#     xmpp = EchoBot('somejid@example.com', 'use_getpass')
#     xmpp.connect()
#     xmpp.process(block=True)
assert resp.status_code == 200