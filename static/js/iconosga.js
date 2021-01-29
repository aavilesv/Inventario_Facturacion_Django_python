$(function () {
    $("#bookpanel").find(".btn-cerrar").click(function () {
        $("#bookpanel").modal("hide");
    });

    $(".icon").hover(function () {
        $(this).addClass("hovered");
    }, function () {
        $(this).removeClass("hovered");
    }).click(function () {
        $.blockUI({message: ''});
        var url = $(this).attr('url');
        if (url[0] == '/') {
            location.href = url;
        } else {
            location.href = "/" + url;
        }
    });
});