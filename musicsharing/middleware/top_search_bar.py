from musicsharing.forms import *

class SearchBarMiddleware(object):

	def process_template_response(self,request,response):
		
		search_user = SearchUserForm()
		search_song = SearchSongForm()
		add_song = AddSongForm()
		post_song = PostSongForm()

		response.context_data['search_user_form'] = search_user
		response.context_data['search_song_form'] = search_song
		response.context_data['add_song_form'] = add_song
		response.context_data['post_song_form'] = post_song

		return response



