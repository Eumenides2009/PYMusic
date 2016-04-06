

$(document).ready(function() {

	var user_option = $(".form-search .selecter-item:first");
	var song_option = $(".form-search .selecter-item:last");
	console.log(song_option.html());
	user_option.attr('id', 'user-option');
	song_option.attr('id', 'song-option');
	document.getElementById("user-option").addEventListener("click", change_search_state);
	document.getElementById("song-option").addEventListener("click", change_search_state);
	document.getElementById("edit-playlist-btn").addEventListener("click", edit_playlist);
	// var delete_song_btns = document.getElementsByClassName("delete-song-in-playlist");
	// for (var btn in delete_song_btns) {
	// 	console.log(btn.html());
	// 	btn.addEventListener("click", delete_song_in_playlist);
	// }
	$("#song-list").on("click","button", delete_song_in_playlist);
}); 

function change_search_state() {
	var state = $(".selecter-selected").html();
	console.log(state);
	if (state == 'User') {
		$("#id_search_user").css("display","none");
		$("#id_search_song").css("display","initial");
	} else {
		$("#id_search_song").css("display","none");
		$("#id_search_user").css("display","initial");	
	}
}

function edit_playlist() {
	var state = this.children[0].getAttribute("value");
	var modal = $("#myModal");
	var hidden_html = '<input type="' + 'hidden" id="playlist-id-in-modal" value="' + state + '">';
	$.ajax({
            url: "/get-list/" + state,
            type: "get",
            async: false,
            success: function(data) {
                if (data['error'] != null) {
                    console.log("get-list error");
                } else {
                    var music = "";
                    var json = data['name'];

                    var song_list = $("#song-list");
                    var html = '<table class="table">' +
        			"<thead>" +
        			    "<tr>" +
        			        "<th></th>" +
        			        "<th>#</th>" +
        			        "<th>Title</th>" +
        			        "<th>Author</th>" +
        			        "<th>Album</th>" +
        			        "<th>Delete</th>" +
        			    "</tr>" +
        			"</thead>" +
        			"<tbody>";
        			for (var i = 1; i <= json.length; i++) {
        				html += "<tr>" +
        				"<td></td>" +
                		"<td>" + i + "</td>" +
                		"<td>"+ json[i - 1]["title"] +"</td>" +
                		"<td>"+ json[i - 1]["author"] +"</td>" +
                		"<td>"+ json[i - 1]["album"] +"</td>" +
                		"<td>" +
                		    // '<a href="#" data-toggle="modal" data-target="#myModal">' +
                		        '<button type="button" class="glyphicon glyphicon-remove-sign delete-song-in-playlist" aria-hidden="true" '+ 'id="song' + i + '"></button">' +
                		"</td>" +
            			"</tr>";
                    }
                    html += "</tbody>" +
   						'</table>';
                    song_list.html(html);
                }
            },
            error: function() {

            }
        });


	modal.append(hidden_html);
}

function delete_song_in_playlist() {
    console.log("exec")
	var edit_playlist = $("#myModal");
	var playlist_id = $("#playlist-id-in-modal").val();

	var tmp = this.parentElement.parentElement.children[2];
	var csrf = getCSRFToken();


	var removeElement = this.parentElement.parentElement;
    var parent = this.parentElement.parentElement.parentElement;
	$.ajax({
            url: "/delete-song",
            type: "post",
            data: {list_id:playlist_id ,song_name:tmp.innerHTML, csrfmiddlewaretoken:csrf},
            async: false,
            success: function(data) {
                
                parent.removeChild(removeElement);

                for (var i = 0; i < parent.children.length; i++) {
                	parent.children[i].children[1].innerHTML = i+1
                }
            },
            error: function() {

            }
        });

}

function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        if (cookies[i].startsWith("csrftoken=")) {
            return cookies[i].substring("csrftoken=".length, cookies[i].length);
        }
    }
    return "unknown";
}
