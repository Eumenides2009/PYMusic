$(document).ready(function() {
	console.log($("#uploadMusic"));
    $("#uploadMusic").on("submit","form",upload_music);
    
});

function upload_music(event){
	console.log('sdadsa');
    event.preventDefault();
    var form = $(this);
    var data = new FormData((form).get(0));
    var picture = $(this).find('input[name="picture"]').val();
    
    var music = $(this).find('input[name="music"]').val();
    
    var lyric = $(this).find('input[name="lyric"]').val();
    
    var csrf = $(this).find('input[name="csrfmiddlewaretoken"]').val();
    var modal = $("#uploadMusic");
    var alerts = $("#uploadMusic").find(".alert");

    if (alerts.length > 0) {
        for (var i = 0; i < alerts.length; i++) {
            $(alerts[i]).remove();
        }
    }

    var modal_body = $("#uploadMusic-body");
    
    console.log(modal_body);

    $.ajax({
    url: $(this).attr('action'),
    type: $(this).attr('method'),
    data: data,
    cache: false,
    processData: false,
    contentType: false,
    success: function(data) {
        window.location.href="/home";
       
    },
    error: function(data) {
        
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
