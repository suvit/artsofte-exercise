from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('artexer.app.views',
    url(r'^$',
        "home",
        name="home"),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^add$', "page_add",
        name="page_add"),
    url(r'^(?P<page1>[a-z0-9_]+)/add$', "page_add",
        name="page_add"),
    url(r'^(?P<page2>[a-z0-9_]+)/(?P<page1>[a-z0-9_]+)/add$',
        "page_add",
        name="page_add"),
    url(r'^(?P<page1>[a-z0-9_]+)/edit$',
        "page_edit",
        name="page_edit"),
    url(r'^(?P<page2>[a-z0-9_]+)/(?P<page1>[a-z0-9_]+)/edit$',
        "page_edit",
        name="page_edit"),
    url(r'^(?P<page1>[a-z0-9_]+)/delete$',
        "page_delete",
        name="page_delete"),
    url(r'^(?P<page2>[a-z0-9_]+)/(?P<page1>[a-z0-9_]+)/delete$',
        "page_delete",
        name="page_delete"),

    url(r'^(?P<page1>[a-z0-9_]+)$',
        "page_view",
        name="page_view"),
    url(r'^(?P<page2>[a-z0-9_]+)/(?P<page1>[a-z0-9_]+)$',
        "page_view",
        name="page_view"),
)

handler404 = 'artexer.app.views.page_404'
