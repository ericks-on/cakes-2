$(document).ready(function() {
    $("#loginForm").submit(function(event) {
        formData = $(this).serialize()
        $.post("/login", formData, function(header){
            console.log("Login successful")
        }).fail(function(){
            $("#error-notification").addClass("show-error");
        });

    });

    $("#lError-ok-button").click(function() {
        $("#error-notification").removeClass("show-error");
    });
});