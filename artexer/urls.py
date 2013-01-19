from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',
        "artexer.app.views.home",
        name="home"),
    url(r'^(?P<page1>[a-z0-9_]+)/$',
        "artexer.app.views.page_view",
        name="page_view"),
    url(r'^(?P<page1>[a-z0-9_]+)/(?P<page2>[a-z0-9_]+)/$',
        "artexer.app.views.page_view",
        name="page_view"),
    url(r'^add/$', "artexer.app.views.page_add",
        name="page_add"),
    url(r'^(?P<page1>[a-z0-9_]+)/add/$',
        "artexer.app.views.page_add",
        name="page_add"),
    url(r'^(?P<page1>[a-z0-9_]+)/edit/$',
        "artexer.app.views.page_edit",
        name="page_edit"),
    url(r'^(?P<page1>[a-z0-9_]+)/(?P<page2>[a-z0-9_]+)/edit/$',
        "artexer.app.views.page_edit",
        name="page_edit"),
    url(r'^(?P<page1>[a-z0-9_]+)/delete/$',
        "artexer.app.views.page_delete",
        name="page_delete"),
    url(r'^(?P<page1>[a-z0-9_]+)/(?P<page2>[a-z0-9_]+)/delete/$',
        "artexer.app.views.page_delete",
        name="page_delete"),

    url(r'^admin/', include(admin.site.urls)),
)
