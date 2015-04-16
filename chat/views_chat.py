__author__ = 'nuttha'
from django.http import HttpResponse
from django.shortcuts import render_to_response
import sleekxmpp
from sleekxmpp import ClientXMPP

def chat_page(request):
    username = '1406523281117@chat-en.shooppening.com'

    return render_to_response('chat_pages.html',
                                {"foo": "bar"})

def sent_meaasge(message):
    return message