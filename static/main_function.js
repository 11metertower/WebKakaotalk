$(document).ready(function () {
    $(".idsubmit").click(function (event) {
        var userid = $(".id").val();
        var password = $(".password").val();

        var data = { "username": userid, "password": password };
        $.ajax({
            url: "/token",
            type: "post",
            data: data,
            success: function () {
                window.location = "/friends?user=" + userid;
            },
            error: function (e) {
                window.alert("ID와 비밀번호가 일치하지 않거나 존재하지 않는 ID입니다.")
            }
        });
    });

    $(".register").click(function () {
        window.location = "/register_page";
    });
});