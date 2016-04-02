from django.conf.urls import url,include,patterns
from musicsharing import views
from postman.views import WriteView

urlpatterns =  patterns('postman.views',
    url(r'^messages/write/(?:(?P<recipients>[^/#]+)/)?$',
        WriteView.as_view(autocomplete_channels=('user')),
        name='write')
	) + [
	url(r'^$',views.home),
	url(r'^upload$',views.upload),
	url(r'^get_lyric/(?P<lyric_name>.+)$',views.get_lyric),
	url(r'^music/(?P<audio_name>.+)$',views.get_audio),
	url(r'^get_audio_index$',views.get_audio_index),
	url(r'^picture/(?P<audio_name>.+)$',views.get_picture),
	url(r'^profile/(?P<username>.+)$',views.profile),
	url(r'^edit-profile$',views.edit_profile),
	url(r'^create-list$',views.create_list),
	url(r'^get-list/(?P<list_id>\d+)$',views.get_list),
	url(r'^delete-list/(?P<list_name>.+)$',views.delete_list),
	url(r'^get-list-picture/(?P<list_id>.+)$',views.get_list_picture),
	url(r'messages/',include('postman.urls',namespace='postman',app_name='postman')),
	url(r'notifications/',include('pinax.notifications.urls')),
	url(r'^ajax_select/', include('ajax_select.urls')),
	url(r'^accounts/',include('allauth.urls')),
	url(r'^playlist$',views.playlist,name='playlist'),
	url(r'^edit-playlist$',views.edit_playlist),
	url(r'^manage-songs$',views.manage_songs),
] 


