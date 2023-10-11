$(document).ready(function(){
    var exitPopup = $("#exit-popup");

    exitPopup.click(function(){
        $("#popups-container").hide();
        $("#popups-container").find("*").not('#exit-popup').hide();
    });
}
);