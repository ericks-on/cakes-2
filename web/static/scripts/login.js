$(document).ready(function() {
    // $("#loginForm").submit(function(event) {
    //     event.preventDefault();
    //     formData = $(this).serialize()
    //     $.post("/login", formData).done(function(response) {
    //         if (response.status_code == 200) {
    //             $(this).unbind('submit').submit();
    //             console.log("Login successful");
    //         } else {
    //             $("#error-notification").addClass("show-error");
    //         }
    //     }).fail(function(){
    //         $("#error-notification").addClass("show-error");
    //     });

    // });

    $("#lError-ok-button").click(function() {
        $("#error-notification").removeClass("show-error");
    });
});