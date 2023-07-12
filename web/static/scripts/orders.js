$(document).ready(function() {
    $('#more-orders-btn').click(function() {
        $('#popups-container').css('display', 'flex');
        $('.orders-popup').css('display', 'block');
    });

    $('#more-pdts-btn').click(function() {
        $('#popups-container').css('display', 'flex');
        $('.pdt-analysis-popup').css('display', 'block');
    });

    $('#exit-btn').click(function() {
        $('.orders-popup').css('display', 'none');
        $('.pdt-analysis-popup').css('display', 'none');
    });


});