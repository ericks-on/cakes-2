$(document).ready(function() {

  var ordersTable = $('#all-orders-table');
  ordersTable.DataTable({
    "paging": true,
    "ordering": true,
    "info": true,
    "searching": true,
    "lengthChange": false,
  });

  // ===========================================show more orders=================================
    $('#more-orders-btn').click(function() {
        $('#popups-container').css('display', 'flex');
        $('.orders-popup, .orders-popup *').show();

    });

    // ====================================popups for product analysis======================================
    $('.product').click(function() {
        var ctx = $('#pa-graph')
        product = $(this).find('.pdt-name').text().toLowerCase();
        $.get( '/api/sales', function( data ) {
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
    $('#order-hist-table, #all-orders-table').on("click", ".orders-row", function() {
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
    $.get( '/api/monthly_aov', function( data ) {
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

  // ===============================most popular popup ======================================
  $('.mp-insight').click(function() {
    $('#popups-container').css('display', 'flex');
    $('.most-popular-popup').css('display', 'flex');
    $('.most-popular-popup *').show();
  });

  // ===============================Orders Graph ======================================

  $.get( '/api/monthly_aov', function( data ) {
    $('.orders-graph-container h2').text('Orders, ' + data.year)
    var ctx = $('#orders-graph')
    var monthly_orders = data.monthly_orders;
    var ordesLineChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        datasets: [{
          label: 'Orders',
          data: monthly_orders,
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

  // =============================Sorting with order status=================================
  $('.order-history .order-status').click(function() {
    var status = $(this).text();
    $.get( '/api/orders', function( data ) {
      var orders = data.orders;
      var ordersTable = $('.order-history #order-hist-table');
      ordersBody = ordersTable.find('tbody');
      ordersBody.empty();
      for (var i = 0; i < orders.length; i++) {
        if (ordersBody.find('tr').length == 10) {
          break;
        }
        if (orders[i].status == status) {
          var row = `
          <tr class="orders-row">
            <td>${orders[i].id}</td>
            <td>${orders[i].created_at}</td>
            <td class=${status}>${orders[i].status}</td>
            <td>${orders[i].quantity}</td>
            <td>${orders[i].order_value}</td>
          </tr>
          `
          ordersBody.append(row);
        }
      }
    });
  });

});