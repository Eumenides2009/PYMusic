$(document).ready(function() {
    $(".comment-btn").on("click", comment_btn);
}); 
function comment_btn() {
    var state = this.children[0].getAttribute("value");
    var post_id = $("#comment-modal-id");
    post_id.val(state);
    console.log(state);
}

$(function () {
   $('.panel-google-plus > .panel-footer > .input-placeholder, .panel-google-plus > .panel-google-plus-comment > .panel-google-plus-textarea > button[type="reset"]').on('click', function(event) {
        var $panel = $(this).closest('.panel-google-plus');
            $comment = $panel.find('.panel-google-plus-comment');
            
        $comment.find('.btn:first-child').addClass('disabled');
        $comment.find('textarea').val('');
        
        $panel.toggleClass('panel-google-plus-show-comment');
        
        if ($panel.hasClass('panel-google-plus-show-comment')) {
            $comment.find('textarea').focus();
        }

        // $(".panel-footer").css("min-height", "0px");
   });
   $('.panel-google-plus-comment > .panel-google-plus-textarea > form > textarea').on('keyup', function(event) {
        var $comment = $(this).closest('.panel-google-plus-comment');
        
        $comment.find('button[type="submit"]').addClass('disabled');
        if ($(this).val().length >= 1) {
            $comment.find('button[type="submit"]').removeClass('disabled');
        }
   });
});


$(document).ready(function(){
    $(".btn-comment").on("click", addComment);
});

function addComment(event) {

    event.preventDefault();
    var form = $(this).siblings("form");
    var post_id = form.find('input[name="post_id"]').val();
    
    var profile_id = form.find('input[name="profile_id"]').val();
    var user_name = form.find('input[name="user_name"]').val();
    
    var comment_content = form.find('textarea[name="content"]').val();
    
    var csrf = form.find('input[name="csrfmiddlewaretoken"]').val();
    var comments = $($(this).parent().parent().siblings(".comments")[0]);
    console.log(comments);
    $.post("/comment", {'content':comment_content, 'post_id':post_id, 'csrfmiddlewaretoken':csrf})
        .done(function(data){
        
            
            form.each(function(){
                this.reset();
            });
            var timestamp = data['time'];

            var html = '<div id="" tabindex="-1" class="Ik Wv" jsmodel="mrYqlc"> \
    <div class="Wi lg "> \
        <a href="" class="ob Jk" oid="117543036089291964062" aria-hidden="true"><img class="go wi Wh img-28" src="/get-profile-picture/' + profile_id + '" alt="..."></a> \
        <div class="Jx"> \
            <div class="eR"> \
                <div class="fR"><a href="/profile/'+ user_name +'">'+ user_name +'</a> \
                    <div class="wO"><span class="Rg">'+ timestamp +'</span></span> \
                    </div> \
                </div> \
            </div> \
            <div class="Aq DK Bt UR gA"> \
                <div class="Ct">'+ comment_content +'</div> \
            </div> \
        </div> \
    </div> \
</div>';
            
            comments.append(html);
        
    })
    .error(function(data){
        // var message = jQuery.parseJSON(data.responseText)["message"];
        //     var html = "";
        //     for (var i = 0; i < message.length; i++) {
        //         html += '<div class="alert alert-warning alert-dismissable" id="add-playlist-alert"> \
        //             <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button> \
        //             <span>' + message[i] + '</span> \
        //         </div> ';
        //     }
        //     modal_body.prepend(html);


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