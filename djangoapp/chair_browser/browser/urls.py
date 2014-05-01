from django.conf.urls import patterns, url
from browser import views

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
)