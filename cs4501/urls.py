from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cs4501.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    urls(r'^api/v1/users/create$', main.create_user),
    urls(r'^api/v1/users/(\d+)$', main.lookup_user),
    urls(r'^api/v1/users/(\d+)/update$', main.update_user),

    urls(r'^api/v1/listing/create$', main.create_listing),
    urls(r'^api/v1/listing/(\d+)$', main.lookup_listing),
    urls(r'^api/v1/listing/(\d+)/update$', main.update_listing),
    urls(r'^api/v1/listing/(\d+)/buy$', main.buy_listing),

    urls(r'^api/v1/review/create$', main.create_review),
    urls(r'^api/v1/review/(\d+)/update$', main.update_review),
    url(r'^admin/', include(admin.site.urls)),
)
