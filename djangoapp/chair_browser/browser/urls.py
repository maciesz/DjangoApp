from django.conf.urls import patterns, url, include
from browser import views
from dajaxice.core import dajaxice_autodiscover

dajaxice_autodiscover()

urlpatterns=patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^login/$', views.user_login, name='login'),
	url(r'^logout/$', views.user_logout, name='logout'),
	url(r'^register/$', views.register, name='register'), # ADD NEW PATTERN!
	url(r'^homepage/$', views.homepage, name='homepage'),
	url(r'^terms/$', views.terms, name='terms'),
	url(r'^rooms/$', views.rooms, name='rooms'),
	url(r'^confirmation/$', views.confirmation, name='confirmation'),
	url(r'^commit/$', views.commit, name='commit'),
    url(r'^rooms/ajaxexample_json/$', views.ajax, name='ajax'),
    url(r'^rooms/rent/$', views.rent, name='rent'),
    url(r'^rooms/content_json/$', views.load_db_content, name="load_content"),
)
