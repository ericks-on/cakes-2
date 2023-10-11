$(document).ready(function(){
    var exitPopup = $("#exit-popup");

    // Closing the popups container
    exitPopup.click(function(){
        $("#popups-container").hide();
        $("#popups-container").find("*").not('#exit-popup, #exit-popup *').hide();
    });

    // Displaying the cart
    $('#cart-ab').click(function(){
        $("#popups-container").css("display", "flex");
        $('#cart-container').css("display", "flex");
        $("#cart-container *").show();
    });
}
);