

$(document).ready(function() {

	var user_option = $(".form-search .selecter-item:first");
	var song_option = $(".form-search .selecter-item:last");
	
	user_option.attr('id', 'user-option');
	song_option.attr('id', 'song-option');
	document.getElementById("user-option").addEventListener("click", change_search_state);
	document.getElementById("song-option").addEventListener("click", change_search_state);
	// document.getElementById("edit-playlist-btn").addEventListener("click", edit_playlist);
	$("#submit-edit-list").on("click", edit_playlist);
    $(".edit-playlist-btn").on("click", edit_playlist_btn);
	$(".table").on("click","span", delete_song_in_playlist);
    $(".add-song-to-list-btn").on("click", add_song_to_list_btn);
    $("#submit-add-song").on("click", add_song_to_playlist);


    // update songs in each playlist
    var tables = $(".table");
   
    $(".table").each(function(index,element){
        var id = element.getAttribute("id");
        var get = "#" + id;
        var table_now = $(get);

        $.ajax({
            url: "/get-list/" + id,
            type: "get",
            async: false,
            success: function(data) {
                if (data['error'] != null) {
                    console.log("get-list error");
                } else {
                    var music = "";
                    var json = data['name'];

                    var song_list = $("#song-list");
                    var html = '<table class="table" id="' +id+ '">' +
                    "<thead>" +
                        "<tr>" +
                            "<th></th>" +
                            "<th>#</th>" +
                            "<th>Title</th>" +
                            "<th>Author</th>" +
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
                        "<td>" +
                            // '<a href="#" data-toggle="modal" data-target="#myModal">' +
                                '<span type="button" class="glyphicon glyphicon-remove-sign delete-song-in-playlist" aria-hidden="true" '+ 'id="song' + i + '"></span">' +
                        "</td>" +
                        "</tr>";
                    }
                    html += "</tbody>" +
                        '</table>';
                  //      console.log(table_now.html());
                    //    console.log(html);
                    table_now.html(html);
                }
            },
            error: function() {

            }
        });
    });

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
function edit_playlist_btn() {
    var state = this.children[0].getAttribute("value");
    var modal = $("#myModal input");
    var input = $($("#myModal input")[1]);
    input.val(state);
}
function add_song_to_list_btn() {
    var state = this.children[0].getAttribute("value");
    var modal = $("#addSongModal");
    var input = $($("#addSongModal input")[1]);
    input.val(state);
}
function add_song_to_playlist() {
    var id = $("#addSongModal").children('input').val();
    var modal = $("#addSongModal");
    var csrf = getCSRFToken();
    var song_name = $($("#addSongModal input").get(0)).val();
    var modal_body = $("#addSongModal-body");
    console.log(id);
    console.log(song_name);

    var modal = $("#addSongModal");
    var alerts = $("#addSongModal").find(".alert");
    if (alerts.length > 0) {
        for (var i = 0; i < alerts.length; i++) {
            $(alerts[i]).remove();
        }
    }
    $.ajax({
            url: "/add-song",
            type: "post",
            data: {list_id:id ,song_name:song_name, csrfmiddlewaretoken:csrf},
            async: false,
            success: function(data) {
                window.location.href='/playlist'; 
                console.log("add song success");
            },
            error: function(data) {
                console.log("ERROR");
                var message = jQuery.parseJSON(data.responseText)["message"];
                console.log(message);
                var html = "";
                for (var i = 0; i < message.length; i++) {
                    html += '<div class="alert alert-warning alert-dismissable" id="add-playlist-alert"> \
                        <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button> \
                        <span>' + message[i] + '</span> \
                    </div> ';
                }
                modal_body.prepend(html);
            }
        });
}
function edit_playlist() {
	var id = $("#myModal").children('input').val();
    
    var list_name = $('#edit-list-name').val();
    var list_intro = $('#edit-list-intro').val();
    var csrf = getCSRFToken();
    
    console.log(csrf);
    var modal = $("#myModal");
    var alerts = $("#myModal").find(".alert");
    if (alerts.length > 0) {
        for (var i = 0; i < alerts.length; i++) {
            $(alerts[i]).remove();
        }
    }
    
    var modal_body = $("#myModal-body");
    $.ajax({
            url: "/edit-playlist",
            type: "post",
            data: {list_id:id ,name:list_name, intro:list_intro, csrfmiddlewaretoken:csrf},
            async: false,
            success: function(data) {
                window.location.href='/playlist'; 
            },
            error: function(data) {
                console.log("aaaa")
            var message = jQuery.parseJSON(data.responseText)["message"];
            
            var html = "";
            for (var i = 0; i < message.length; i++) {
                html += '<div class="alert alert-warning alert-dismissable" id="add-playlist-alert"> \
                    <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button> \
                    <span>' + message[i] + '</span> \
                </div> ';
            }
            modal_body.prepend(html);
            }
        });
    
}


function delete_song_in_playlist() {
	
	var playlist_id = this.parentElement.parentElement.parentElement.parentElement.getAttribute("id");

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
    console.log(cookies.length);
    for (var i = 0; i < cookies.length; i++) {
    
        if (cookies[i].trim().startsWith("csrftoken=")) {
       
            return cookies[i].trim().substring("csrftoken=".length, cookies[i].length);
        }
    }
    console.log("why");
    return "unknown";
}
