$(document).ready(function() {
    $(".comment-btn").on("click", comment_btn);
}); 
function comment_btn() {
    var state = this.children[0].getAttribute("value");
    var post_id = $("#comment-modal-id");
    post_id.val(state);
    console.log(state);
}