$(document).ready(function () {
    var queryString = window.location.search;
    var urlParams = new URLSearchParams(queryString);
    var user = urlParams.get('user');

    function add_new_friend(datas) {
        $(".list").empty();
        datas.forEach(item => {
            $(".list").append("<div class=\'friend\'><p class=\"name\">" + item.id + "</p></div>");
        });
    }
    function get_friend() {
        $.getJSON("/getfriend", add_new_friend);
    }
    get_friend();

    $(".nav_friend_add").click(function (event) {
        var new_friend = prompt("새로운 친구 이름을 입력하세요");
        if (new_friend != null) {
            data = { "id": new_friend };
            $.ajax({
                url: "/postfriend",
                type: "post",
                contentType: "application/json",
                dataType: "json",
                data: JSON.stringify(data),
                success: get_friend
            });
        }
    });
    $(".nav_talk").click(function (event) {
        window.location = "/talk_list?user="+user;
    });
    
    $(document).on("click", "div.friend", function () {
        var name = $(this).find(".name").text();
        window.location = "/talk?user="+user+"&name="+name;
    });
});