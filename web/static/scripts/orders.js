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

    $.get('http://192.168.0.34:3000/api/v1_0/orders', function(data) {
        var orders = data.orders;
        var ordersTableBody = $('#order-hist-table tbody');
        ordersTableBody.empty();
        for (var i = 0; i < orders.length; i++) {
            var order = orders[i];
            var orderRow = $('<tr></tr>');
            var orderID = $('<td></td>').text(order.id);
            var orderDate = $('<td></td>').text(order.created_at);
            var orderStatus = $('<td></td>').text(order.status);
            orderQuantity = $('<td></td>').text(order.quantity);
            var orderTotal = $('<td></td>').text(order.order_value);
            orderRow.append(orderID);
            orderRow.append(orderDate);
            orderRow.append(orderStatus);
            orderRow.append(orderQuantity);
            orderRow.append(orderTotal);
            ordersTableBody.append(orderRow);
        };
    });
});