__author__ = 'nuttha'
from django.shortcuts import render
# -*- coding: utf-8 -*-
import requests
from requests.auth import HTTPBasicAuth

server = "localhost"
virtualhost = "localhost"
url = "http://%s:5280/admin/server/%s/shared-roster/" % (server, virtualhost)
auth = HTTPBasicAuth("admin@localhost", "123456")
data = {
    'namenew': "user_test_post_123",
    'addnew': "123456"
}
resp = requests.post(url, data=data, auth=auth)

assert resp.status_code == 200