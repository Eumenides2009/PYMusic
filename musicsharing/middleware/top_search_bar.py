from musicsharing.forms import *

class SearchBarMiddleware(object):

	def process_template_response(self,request,response):
		
		search_user = SearchUserForm()
		search_song = SearchSongForm()
		add_song = AddSongForm()

		response.context_data['search_user_form'] = search_user
		response.context_data['search_song_form'] = search_song
		response.context_data['add_song_form'] = add_song

		return response

