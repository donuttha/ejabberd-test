

__author__ = 'nuttha'
from django.http import HttpResponse
from django.shortcuts import render_to_response
import sleekxmpp
from sleekxmpp import ClientXMPP

import sys
import logging
import getpass
from optparse import OptionParser

import sleekxmpp
from sleekxmpp.exceptions import IqError, IqTimeout

if sys.version_info < (3, 0):
    from sleekxmpp.util.misc_ops import setdefaultencoding
    setdefaultencoding('utf8')
else:
    raw_input = input


class RegisterBot(sleekxmpp.ClientXMPP):

    """
    A basic bot that will attempt to register an account
    with an XMPP server.

    NOTE: This follows the very basic registration workflow
          from XEP-0077. More advanced server registration
          workflows will need to check for data forms, etc.
    """

    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start, threaded=True)
        self.add_event_handler("register", self.register, threaded=True)

    def start(self, event):
        self.send_presence()
        self.get_roster()

        # We're only concerned about registering, so nothing more to do here.
        self.disconnect()

    def register(self, iq):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password

        try:
            resp.send(now=True)
            logging.info("Account created for %s!" % self.boundjid)
        except IqError as e:
            logging.error("Could not register account: %s" %
                    e.iq['error']['text'])
            self.disconnect()
        except IqTimeout:
            logging.error("No response from server.")
            self.disconnect()



def chat_page(request):
    username = '1406523281117@chat-en.shooppening.com'
    password='qqqqqqqq'
    server=''
    #authenticate(username,password,server)

    return render_to_response('chat_pages.html',{"text": "text"})

def sent_meaasge(message):
    return message

#http://stackoverflow.com/questions/27684172/sleekxmpp-with-django-not-working
from rest_framework.views import APIView
class SendMessageView(APIView,sleekxmpp.ClientXMPP):

    def session_start(self,jid, password, recipient, message):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.xmpp = sleekxmpp.ClientXMPP(jid, password)
        self.recipient = recipient
        self.msg = message
        self.add_event_handler("session_start", self.start)

    def start(self, event):
        self.send_presence()
        try:
            self.get_roster()
        except IqError as err:
            logging.error('There was an error getting the roster')
            logging.error(err.iq['error']['condition'])
            self.disconnect()
        except IqTimeout:
            logging.error('Server is taking too long to respond')
            self.disconnect()

        self.send_message(mto=self.recipient,mbody=self.msg,mtype='chat')
        self.disconnect(wait=True)

    def post(self,request,format=None):

        jid=request.DATA.get('sender')
        password=request.DATA.get('password')
        receiver=request.DATA.get('receiver')
        message=request.DATA.get('message')
        # xmpp=self.aaaa(jid,password,receiver,message)
        xmpp = self.get_xmpp(jid,password,receiver,message)
        xmpp.register_plugin('xep_0030')
        xmpp.register_plugin('xep_0199')
        if xmpp.connect():
            xmpp.process(block=False)
            print "Connected"
        else:
            print "Not Connected"

class ChatClient(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password, server):
        sleekxmpp.ClientXMPP.__init__(self, '1406523281117@chat-en.shooppening.com', password,True)

        self.add_event_handler("session_start", self.start)

        self.register_plugin('xep_0030')
        self.register_plugin('xep_0004')
        self.register_plugin('xep_0060')
        self.register_plugin('xep_0199')

        # self.ssl_version = ssl.PROTOCOL_SSLv3
        self.connected = self.connect()
        if self.connected:
            self.process(threaded=True)


    def start(self, event):
        self.send_presence(priority = "-9001")
        self.get_roster(blocking = True, timeout = 3)

    def message(self, targets, msg):
        for target in targets:
            self.send_message(target, msg)

def authenticate(username='1406523281117@chat-en.shooppening.com', password='qqqqqqqq', server=''):
    xmppuser = username + '@' + server
    passTester = ChatClient(xmppuser, password, server)
    try:
        result = passTester.auth_queue.get(timeout=10)
    except:
        result = 'failed'
    passTester.disconnect()
    return result == 'success'