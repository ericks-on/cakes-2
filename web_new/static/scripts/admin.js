import { customAlert, alertContainer } from "./main.js";

$(document).ready(function () {
    $("#incoming-orders").DataTable({
        "ordering": false,
        "pageLength": 5,
        "lengthChange": false,
        "info": false,
    });

    $('#current-notifications').DataTable({
        "ordering": false,
        "pageLength": 5,
        "lengthChange": false,
        "info": false,
        "searching": false,
    });

    $('#current-products').DataTable({
        "ordering": false,
        "pageLength": 5,
        "lengthChange": false,
        "info": false,
    });

    $('#products-inventory').DataTable({
        "ordering": false,
        "pageLength": 5,
        "lengthChange": false,
        "info": false,
    });

    $('#current-users').DataTable({
        "ordering": false,
        "pageLength": 5,
        "lengthChange": false,
        "info": false,
    });

    $('#current-inventory').DataTable({
        "ordering": false,
        "pageLength": 5,
        "lengthChange": false,
        "info": false,
    });

    var activePage = $('#dashboard');

    $('#productPageButton').click(function () {
        activePage.hide();
        activePage = $('#products-management');
        activePage.show();
    });

    $('#dashboardButton').click(function () {
        activePage.hide();
        activePage = $('#dashboard');
        activePage.show();
    });

    $('#inventoryButton').click(function () {
        activePage.hide();
        activePage = $('#inventory-management');
        activePage.show();
    });

    $('#userPageButton').click(function () {
        activePage.hide();
        activePage = $('#user-management');
        activePage.show();
    });

    $('#ordersButton').click(function () {
        activePage.hide();
        activePage = $('#orders');
        activePage.show();
    });

    $('#notificationsButton').click(function () {
        activePage.hide();
        activePage = $('#notifications-management');
        activePage.show();
    });

    $('#addProductsBtn').click(function (event) {
        event.preventDefault();
        let CSRFToken = $(this).parent().parent().find('#csrf_token').val();
        let name = $(this).parent().parent().find('#product-name').val();
        let price = $(this).parent().parent().find('#product-price').val();
        let data = {
            'name': name,
            'price': price
        }
        $.ajax({
            url: '/products',
            method: 'POST',
            headers: {
                'X-CSRFToken': CSRFToken,
            },
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function (){
                customAlert("Product added successfully");
                $(this).parent().parent().find('#product-price').val("");
                $(this).parent().parent().find('#product-name').val("");
            },
            error: function (response) {
                console.log(response);
                customAlert("There was a problem Adding the Product");
            }
        });
    });
});