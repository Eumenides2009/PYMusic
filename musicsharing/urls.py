from django.conf.urls import url,include
from musicsharing import views

urlpatterns = [
	url(r'^$',views.home),
	url(r'^upload$',views.upload),
	url(r'^music/(?P<audio_name>.+)$',views.get_audio),
	url(r'^accounts/',include('allauth.urls')),
]