$(function () {
    $("#demo").val("muyou")
});

$(function () {
    $(window).keyup(function (event) {
        if (event.keyCode == 13) {
            ss();
        }
    });

    $("#pp").click(function () {
        window.location.href = "/demo2";
    });

    $("#ss").click(ss);
});

function ss() {
    var news = $("#news").val();
    console.log(news);
    window.location.href = "/news?word=" + news;
}
