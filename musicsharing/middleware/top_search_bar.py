from musicsharing.forms import *

class SearchBarMiddleware(object):

	def process_template_response(self,request,response):
		
		search_user = SearchUserForm()
		search_song = SearchSongForm()

		response.context_data['search_user_form'] = search_user
		response.context_data['search_song_form'] = search_song

		return response

