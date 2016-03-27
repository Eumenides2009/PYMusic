from django.conf.urls import url,include
from musicsharing import views

urlpatterns = [
	url(r'^$',views.home),
	url(r'^upload$',views.upload),
	url(r'^music/(?P<audio_name>.+)$',views.get_audio),
	url(r'^get_audio_index$',views.get_audio_index),
	url(r'^picture/(?P<audio_name>.+)$',views.get_picture),
	url(r'^profile/(?P<username>.+)$',views.profile),
	url(r'^edit-profile$',views.edit_profile),
	url(r'messages/',include('postman.urls',namespace='postman',app_name='postman')),
	url(r'^accounts/',include('allauth.urls')),
]