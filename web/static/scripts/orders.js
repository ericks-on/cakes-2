$(document).ready(function() {
    $('#more-orders-btn').click(function() {
        $('#popups-container').css('display', 'flex');
        $('.orders-popup').css('display', 'block');
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
        $('.pa-popup').show();
        $('pa-graph').show();
    });

    $('#exit-btn').click(function() {
        $('#popups-container').hide();
        $('.pa-popup').hide();
        $('pa-graph').hide();
        $('.orders-popup').hide();
    });

});