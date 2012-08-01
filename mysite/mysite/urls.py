from django.conf.urls import patterns, include, url
from mylog.views import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
	url(r'^$',main_page),
	url(r'^view/(\w+)/$',view_page),
	url(r'^edit/([\w]*)[/]?$',edit_page),
	url(r'^list$',list_page),
	url(r'^delete$',delete_page),
#url(r'^$',main_page),
#url(r'^$',main_page),
)
