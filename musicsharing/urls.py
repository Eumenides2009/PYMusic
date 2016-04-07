from django.conf.urls import url,include,patterns
from musicsharing import views
from postman.views import WriteView

urlpatterns =  patterns('postman.views',
    url(r'^messages/write/(?:(?P<recipients>[^/#]+)/)?$',
        WriteView.as_view(autocomplete_channels=('user')),
        name='write')
	) + [

	# player
	url(r'^$',views.home,name='home'),
	url(r'^upload$',views.upload),
	url(r'^get_lyric/(?P<lyric_name>.+)$',views.get_lyric),
	url(r'^music/(?P<audio_name>.+)$',views.get_audio),
	url(r'^get_audio_index$',views.get_audio_index,name='all_music'),
	url(r'^picture/(?P<audio_name>.+)$',views.get_picture),

	# single song

	url(r'^remove-song-repo$',views.remove_song_repo),

	# profile
	url(r'^profile/(?P<username>.*)$',views.profile,name='profile'),
	url(r'^edit-profile$',views.edit_profile),

	# list
	url(r'^create-list$',views.create_list),
	url(r'^get-list/(?P<list_id>\d+)$',views.get_list),
	url(r'^delete-list$',views.delete_list),
	url(r'^get-list-picture/(?P<list_id>.+)$',views.get_list_picture),
	url(r'^get-list-name$',views.get_list_name),

	# song in list
	url(r'^delete-song$',views.delete_song),
	url(r'^add-song$',views.add_song),


	# third party package
	url(r'messages/',include('postman.urls',namespace='postman',app_name='postman')),
	url(r'notifications/',include('pinax.notifications.urls')),
	url(r'^ajax_select/', include('ajax_select.urls')),
	url(r'^accounts/',include('allauth.urls')),
	url(r'^playlist$',views.playlist,name='playlist'),
	url(r'^edit-playlist$',views.edit_playlist),
	url(r'^manage-songs$',views.manage_songs),

	url(r'^friend-stream$',views.friend_stream),	
] 


