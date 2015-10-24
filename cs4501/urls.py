from django.conf.urls import patterns, include, url
from django.contrib import admin
from cs4501 import main

urlpatterns = patterns('',
    url(r'^api/v1/users/create$', main.create_user),
    url(r'^api/v1/users/(\d+)$', main.lookup_user),
    url(r'^api/v1/users/(\d+)/update$', main.update_user),
    url(r'^api/v1/users/auth$', main.user_login),

    url(r'^api/v1/listing/create$', main.create_listing),
    url(r'^api/v1/listing/(\d+)$', main.lookup_listing),
    url(r'^api/v1/listing/(\d+)/update$', main.update_listing),
    url(r'^api/v1/listing/(\d+)/buy$', main.buy_listing),
    url(r'^api/v1/listing/recent$', main.most_recent),

    url(r'^api/v1/review/create$', main.create_review),
    url(r'^api/v1/review/(\d+)/update$', main.update_review),
    url(r'^api/v1/review/(\d+)$', main.lookup_review),
    url(r'^admin/', include(admin.site.urls)),
)
