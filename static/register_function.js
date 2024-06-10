$(document).ready(function () {

    $(".register").click(function () {
        click_register();
    });

    function click_register() {
        var userid = $(".id").val();
        var password = $(".password").val();
        var data = { "username": userid, "password": password };
        $.ajax({
            url: "/register",
            type: "post",
            data: data,
            success: function () {
                window.alert("환영합니다");
                window.location = "/";
            }
        });
    }
});