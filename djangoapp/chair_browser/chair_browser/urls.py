from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	
	# Examples:
	# url(r'^$', 'chair_browser.views.home', name='home'),
	# url(r'^blog/', include('blog.urls')),
	url(r'^browser/', include('browser.urls', namespace='browser')),
	url(r'^admin/', include(admin.site.urls)),
)
