import os.path
from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

from mylog.views import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

site_media = os.path.join(
	os.path.dirname(__file__),'../site_media'		
)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
	url(r'^$',main_page),
	url(r'^user/(\w+)/$',main_page),
	url(r'^view/(\d+)/$',view_page),
	url(r'^edit/(\d+)/$',edit_page),
	url(r'^list/$',list_page),
	url(r'^delete/(\d+)/$',delete_page),

	url(r'^login/$','django.contrib.auth.views.login'),
	url(r'^logout/$',logout_page),
	url(r'^register/$',register_page),
	url(r'^register/success/$', direct_to_template, {'template': 'registration/register_success.html'}),

	url(r'^site_media/(?P<path>.*)/$','django.views.static.serve',
		{ 'document_root': site_media }),
)
