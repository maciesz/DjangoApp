from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from dajaxice.core import dajaxice_autodiscover

admin.autodiscover()
dajaxice_autodiscover()

urlpatterns = patterns('',
	
	# Examples:
	# url(r'^$', 'chair_browser.views.home', name='home'),
	# url(r'^blog/', include('blog.urls')),
	url(r'^browser/', include('browser.urls', namespace='browser')),
	url(r'^admin/', include(admin.site.urls)),
    url(r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
)
