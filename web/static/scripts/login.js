$(document).ready(function() {
    $("#loginForm").submit(function(event) {
        event.preventDefault();
        var formData = {
            username: $("#username").val(),
            password: $("#password").val()
        };
        $.post("/login", formData, function(data) {
            if (data.redirect) {
                var queryParams = $.param(data.headers);
                window.location.href = data.url + "?" + queryParams;
            }
            else {
                $("#error-notification").addClass("show-error");
            }
        });
    });

    $("#lError-ok-button").click(function() {
        $("#error-notification").removeClass("show-error");
    });
});