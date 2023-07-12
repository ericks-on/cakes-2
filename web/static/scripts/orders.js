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

    var statusColumn = $('.order-status-col');
    for (var i = 0; i < statusColumn.length; i++) {
        var status = statusColumn[i].innerHTML;
        if (status == 'pending') {
            statusColumn[i].addClass('pending');
        } else if (status == 'confirmed') {
            statusColumn[i].addClass('confirmed');
        } else if (status == 'delivered') {
            statusColumn[i].addClass('delivered');
        } else if (status == 'settled') {
            statusColumn[i].addClass('settled');
        };
    };

});