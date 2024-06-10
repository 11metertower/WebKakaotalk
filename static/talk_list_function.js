$(document).ready(function () {
    var queryString = window.location.search;
    var urlParams = new URLSearchParams(queryString);
    var userr = urlParams.get('user');

    $(".nav_friend").click(function (event) {
        window.location = "/friends?user=" + userr;
    });

    $.getJSON("/gettalk_list", talk_list);
    function talk_list(datas) {
        $(".list").empty();
        datas.forEach(item => {
            var opp = item.oppo;
            var talk = item.talk;
            $(".list").append("<div class=\"friend\"><p class=\"name\">" + opp + "</p><p class=\"talk\">" + talk + "</p></div>")
        });
    }

    $(document).on("click", "div.friend", function () {
        var name = $(this).find(".name").text();
        window.location = "/talk?user=" + userr + "&name=" + name;
    });
});