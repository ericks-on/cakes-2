$(document).ready(function() {
  // ===========================================show more orders=================================
    $('#more-orders-btn').click(function() {
        $('#popups-container').css('display', 'flex');
        $('.orders-popup, .orders-popup *').show();
    });

    // ====================================popups for product analysis======================================
    $('.product').click(function() {
        var ctx = $('#pa-graph')
        product = $(this).find('.pdt-name').text().toLowerCase();
        $.get( '/sales', function( data ) {
            var sales = data.monthly_sales[product];
            $('.pa-popup h2').text(product.toUpperCase() + ' ' +
            'SALES' + ' ' + data.year);
            var lineChart = new Chart(ctx, {
                type: 'line',
                data: {
                  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                  datasets: [{
                    label: 'Sales',
                    data: sales,
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
          $('#popups-container').css('display', 'flex');
          $('.pa-popup, .pa-popup *').show();
          $('pa-graph, .pa-graph *').show();
    });

    // ==================================== popus for order info=================================
    $('.orders-row').click(function() {
      $('#popups-container').css('display', 'flex');
      $('.order-detailed-popup').css('display', 'flex');
      $('.order-detailed-popup *').show();
      $(this).find('td').each(function(index) {
        if (index == 0) {
          $('#order-id').text($(this).text());
        } else if (index == 1) {
          $('#order-date').text($(this).text());
        } else if (index == 2) {
          $('#order-status').text($(this).text());
        } else if (index == 3) {
          $('#order-quantity').text($(this).text());
        } else if (index == 4) {
          $('#order-amount').text($(this).text());
        }
    });
  });

  // =====================================insights popup======================================  
  $('.aov-insight').click(function() {
    $.get( '/monthly_aov', function( data ) {
      var ctx = $('#aov-graph')
      var monthly_aov = data.monthly_aov;
      $('.aov-popup h2').text('Average Order Value, ' + data.year);
      var lineChart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            datasets: [{
              label: 'AOV',
              data: monthly_aov,
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

    $('#popups-container').css('display', 'flex');
    $('.aov-popup').css('display', 'flex');
    $('.aov-popup *').show();
  });


});