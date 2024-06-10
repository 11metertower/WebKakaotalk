$(document).ready(function () {
    var ws = new WebSocket("ws://localhost:8000/ws");
    var queryString = window.location.search;
    var urlParams = new URLSearchParams(queryString);
    var userr = urlParams.get('user');
    var name = urlParams.get('name');
    $.getJSON("/gettalklist", submit_id);
    ws.onmessage = function (event) {
        var data = JSON.parse(event.data);
        var id = userr;
        var idd = data.id;
        var user = data.user;
        var talk = data.talk;
        var time = data.time;
        if (id == user) {
            data.oppo = idd;
            $.ajax({
                url: "/posttalk",
                type: "post",
                contentType: "application/json",
                dataType: "json",
                data: JSON.stringify(data),
                success: function (talklist) {
                    $.getJSON("/gettalklist", submit_id);
                }
            });
        }
    };

    $("#send1").click(function () {
        click_button1();
    });

    $("#text1").keyup(function (event) {
        if (event.keyCode == 13 && !event.shiftKey) {
            event.preventDefault();
            $("#text1").submit();
        }
    });

    $("#text1").on("submit", function () {
        click_button1();
    });

    function click_button1() {
        var talk = $("#text1").val();
        talk = talk.replaceAll("\n", "<br>").replaceAll(" ", "&nbsp;");
        if (talk == "<br>") {
            talk = "";
            $("#text1").val(talk);
        }
        if (talk.slice(-4) == "<br>") {
            talk = talk.slice(0, -4);
        }
        if (talk != "") {
            var user = userr;
            var time = new Date().toLocaleTimeString("ko-KR").slice(0, -3);
            var data = { id: user, user: name, talk: talk, time: time, oppo: name };
            ws.send(JSON.stringify(data));
            $.ajax({
                url: "/posttalk",
                type: "post",
                contentType: "application/json",
                dataType: "json",
                data: JSON.stringify(data),
                success: function (talklist) {
                    $.getJSON("/gettalklist", submit_id);
                }
            });
        }
    }

    function submit_id(datas) {
        var id = userr;
        $(".user1 .wrap").empty();
        datas.forEach(item => {
            var idd = item.id;
            var user = item.user;
            var talk = item.talk;
            var time = item.time;
            if (id == user && idd == name) {
                $(".user1 .wrap").append("<div class=\"username\"><p>" + idd + "</p></div><div class=\"chat ch1\"><div class=\"textbox\">" + talk + "</div><div class=\"time\"><p>" + time + "</p></div></div>");
            }
            else if (id == idd && user == name) {
                $(".user1 .wrap").append("<div class=\"chat ch2\"><div class=\"textbox\">" + talk + "</div><div class=\"time\"><p>" + time + "</p></div></div>");
            }
        });
        $("#text1").val("");
        $('.wrap').scrollTop($('.wrap')[0].scrollHeight);
    }

    $('#input_image').change(function () {
        if (this.files.length > 0) {
            var image_name = this.files[0].name;
        }
        var time = new Date().toLocaleTimeString("ko-KR").slice(0, -3);
        var talk = "<a href=\"#\" onclick=\"window.open('/static/" + image_name + "')\"><img src=\"/static/" + image_name + "\"></a>";
        var data = { id: userr, user: name, talk: talk, time: time, oppo: name };
        ws.send(JSON.stringify(data));
        $.ajax({
            url: "/posttalk",
            type: "post",
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify(data),
            success: function (talklist) {
                $.getJSON("/gettalklist", submit_id);
            }
        });
    });

    $('#input_video').change(function () {
        if (this.files.length > 0) {
            var video_name = this.files[0].name;
        }
        var time = new Date().toLocaleTimeString("ko-KR").slice(0, -3);
        var talk = "<video src=\"/static/" + video_name + "\" controls></a>";
        var data = { id: userr, user: name, talk: talk, time: time, oppo: name };
        ws.send(JSON.stringify(data));
        $.ajax({
            url: "/posttalk",
            type: "post",
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify(data),
            success: function (talklist) {
                $.getJSON("/gettalklist", submit_id);
            }
        });
    });
});