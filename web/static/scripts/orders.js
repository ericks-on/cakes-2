$(document).ready(function() {
    $('#more-orders-btn').click(function() {
        $('#popups-container').css('display', 'flex');
        $('.orders-popup, .orders-popup *').show();
    });

    $('.product').click(function() {
        $('#popups-container').css('display', 'flex');
        var ctx = $('#pa-graph')
        var lineChart = new Chart(ctx, {
            type: 'line',
            data: {
              labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
              datasets: [{
                label: 'Sales',
                data: [10, 20, 30, 25, 35, 45],
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
          $('.pa-popup, .pa-popup *').show();
          $('pa-graph, .pa-graph *').show();
    });


});