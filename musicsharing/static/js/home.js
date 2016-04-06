$(document).ready(function() {
    var playlist = $("#playlist_choose");
    console.log(playlist);
    $.ajax({
            url: "/get-list-name",
            type: "get",
            async: false,
            success: function(data) {
                if (data['error'] != null) {
                    console.log("get-list-name error");
                } else {
                    var music = "";
                    var json = data['name'];
                    console.log(json);
                    var html = "";
                    for (var i = 1; i < json.length; i++) {
                        html += '<span class="selecter-item selected" data-value="'+i+'">'+ json[i] + '</span>'
                    }
                    playlist.append(html);
                }
            },
            error: function() {

            }
       });
});
