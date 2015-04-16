from django.conf.urls import patterns, include, url
from django.contrib import admin
from chat.views_chat import chat_page

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ejabberd.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^chat/$', chat_page , name='chat_page'),
    url(r'^admin/', include(admin.site.urls)),
)
