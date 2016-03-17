from django.conf.urls import url,include
from musicsharing import views

urlpatterns = [
	url(r'^$',views.default),
	url(r'^upload$',views.upload),
	url(r'^music/(?P<audio_name>.+)$',views.get_audio),
]