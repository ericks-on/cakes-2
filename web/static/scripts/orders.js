$(document).ready(function() {
    $('#more-orders-btn').click(function() {
        $('#popups-container').css('display', 'flex');
        $('.orders-popup, .orders-popup *').show();
    });

    $('.product').click(function() {
        $('#popups-container').css('display', 'flex');
        var ctx = $('#pa-graph')
        product = $(this).find('.pdt-name').text().toLowerCase();
        $.get( '/sales', function( data ) {
            var sales = data.monthly_sales[product];
            var lineChart = new Chart(ctx, {
                type: 'line',
                data: {
                  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                  datasets: [{
                    label: 'Sales',
                    data: Object.values(sales),
                    borderColor: 'blue',
                    fill: false
                  }]
                },
                options: {
                  responsive: true,
                  scales: {
                    y: {
                      beginAtZero: true
                    }
                  }
                }
              });
        });
          $('.pa-popup, .pa-popup *').show();
          $('pa-graph, .pa-graph *').show();
    });


});