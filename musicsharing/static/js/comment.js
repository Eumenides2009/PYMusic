$(document).ready(function() {
    $(".comment-btn").on("click", comment_btn);
}); 
function comment_btn() {
    var state = this.children[0].getAttribute("value");
    var post_id = $("#comment-modal-id");
    post_id.val(state);
    console.log(state);
}




$(document).ready(function(){
    $(".comment-modal").on("submit", "form", addComment);
});

function addComment(event) {

    event.preventDefault();
    var form = $(this);
    var post_id = $(this).find('input[name="post_id"]').val();
    
    var profile_id = $(this).find('input[name="profile_id"]').val();
    var user_name = $(this).find('input[name="user_name"]').val();
    
    var comment_content = $(this).find('textarea[name="content"]').val();
    console.log(comment_content);
    var csrf = $(this).find('input[name="csrfmiddlewaretoken"]').val();
    var modal = $("#myModal");

    var modal_body = $("#myModal-body");
    console.log(modal_body);
    $.post("/comment", {'content':comment_content, 'post_id':post_id, 'csrfmiddlewaretoken':csrf})
        .done(function(data){
        
            modal.modal('toggle');
            form.each(function(){
                this.reset();
            });
            var timestamp = data['time'];

            
            var html = '<div class="row pull-left"> \
                    <div class="col-md-1"> \
                        <img class="img-rounded" src="/get-profile-picture/' + profile_id + '" alt="..."> \
                    </div> \
                    <div class="col-md-11"> \
                        <div class="post-comments"> \
                            <p class="blog-post-meta">'+ timestamp +' &nbsp;<a href="/profile/'+ user_name +'">'+ user_name +'</a> says : </p> \
                            <p> \
                            '+ comment_content +' \
                            </p> \
                        </div> \
                        <div style="clear:both"></div> \
                    </div> \
                </div> ';
            
            $('#comment-list-'+ post_id).append(html);
        
    })
    .error(function(data){
        var message = jQuery.parseJSON(data.responseText)["message"];
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