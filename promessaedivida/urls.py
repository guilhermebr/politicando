#encoding: utf-8

from django.conf.urls import patterns, include, url

urlpatterns = patterns('promessaedivida.views',
    url(r'^$', 'index', name='promessaedivida'),
)