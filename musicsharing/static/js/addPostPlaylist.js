$(document).ready(function() {
    $("#addPlaylist").on("submit", "form", addPlaylist);
    $("#addPost").on("submit", "form", addPost);
}); 
function comment_btn() {
    var state = this.children[0].getAttribute("value");
    var post_id = $("#comment-modal-id");
    post_id.val(state);
    console.log(state);
}

function addPlaylist(event) {
    event.preventDefault();
    var form = $(this);
    var picture = $(this).find('input[name="picture"]').val();
    
    var playlist_name = $(this).find('input[name="name"]').val();
    
    var intro = $(this).find('textarea[name="intro"]').val();
    
    var csrf = $(this).find('input[name="csrfmiddlewaretoken"]').val();
    var modal = $("#addPlaylist");
    var alerts = $("#addPlaylist").find(".alert");
    if (alerts.length > 0) {
        for (var i = 0; i < alerts.length; i++) {
            $(alerts[i]).remove();
        }
    }
    var modal_body = $("#addPlaylist-body");
    console.log(intro);
    $.post("/create-list", {'intro':intro, 'picture':picture, 'name':playlist_name, 'csrfmiddlewaretoken':csrf})
        .done(function(data){
            window.location.href='/playlist';
        })
        .fail(function(data) {
            console.log(data);
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
        });
}
function addPost(event) {
    event.preventDefault();
    var form = $(this);
    
    var song_name = $(this).find('input[name="post_song"]').val();
    
    var content = $(this).find('textarea[name="content"]').val();
    
    var csrf = $(this).find('input[name="csrfmiddlewaretoken"]').val();

    var modal = $("#addPost");
    var alerts = $("#addPost").find(".alert");
    if (alerts.length > 0) {
        for (var i = 0; i < alerts.length; i++) {
            $(alerts[i]).remove();
        }
    }
    
    var modal_body = $("#addPost-body");
    $.post("/post", {'post_song':song_name, 'content':content,'csrfmiddlewaretoken':csrf})
        .done(function(data){
            window.location.href='/friend-stream';
        })
        .fail(function(data) {
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