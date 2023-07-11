$(document).ready(function() {
    $('#more-orders-btn').click(function() {
        $('#popups-container').css('display', 'flex');
        $('#orders-popup-container').css('display', 'flex');
    });

    $('#more-sales-btn').click(function() {
        $('#popups-container').css('display', 'flex');
        $('#sales-popup-container').css('display', 'flex');
    });

    $('#exit-btn').click(function() {
        $('#orders-popup-container').css('display', 'none');
        $('#sales-popup-container').css('display', 'none');
    });
});