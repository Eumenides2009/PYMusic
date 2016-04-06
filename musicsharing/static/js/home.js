$(document).ready(function() {
    var playlist = $("#playlist_choose");
    var parent = playlist.parent();
    console.log(parent);
    $.ajax({
            url: "/get-list-name",
            type: "get",
            async: false,
            success: function(data) {
                if (data['error'] != null) {
                    console.log("get-list-name error");
                } else {
                    var json = data['name'];
                    var html = "";
                    var option_html = "";
                    for (var i = 1; i <= json.length; i++) {
                        if (i == 1) 
                            html += '<span class="selecter-item selected" data-value="'+i+'">'+ json[i - 1] + '</span>';
                        else
                            html += '<span class="selecter-item" data-value="'+i+'">'+ json[i - 1] + '</span>';
                        option_html += '<option value="'+i+'">'+ json[i - 1] + '</option>'
                    }
                    console.log(parent.children());
                    parent.children().eq(0).html(option_html);
                    parent.children().eq(1).html(json[0]);
                    parent.children().eq(2).html(html);
                }
            },
            error: function() {

            }
       });
});
