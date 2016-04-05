document.getElementById("user-option").addEventListener("click", change_search_state);
document.getElementById("song-option").addEventListener("click", change_search_state);

$(document).ready(function() {
	var user_option = $(".selecter-options"):first;
	var song_option = $(".selecter-options"):last;
	user_option.attr('id', 'user-option');
	song_option.attr('id', 'song-option');
}); 

function change_search_state() {
	var state = $(".selecter-options").html();
	if (state == 'User') {
		$.("id_search_user").hide();
	} else {
		$.("id_search_song").hide();
	}
}