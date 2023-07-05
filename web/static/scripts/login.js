$(document).ready(function() {
    $("#loginForm").submit(function(event) {
        event.preventDefault();
        var formData = {
            username: $("#username").val(),
            password: $("#password").val()
        };
        $.post("/login", formData, function(data) {
            if (data.redirect) {
                window.location.href = data.redirect;
            }
            else {
                $("#error-notification").show();
            }
        });
    });
});