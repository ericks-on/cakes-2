import { customAlert, alertContainer } from "./main.js";

const popupContainer = $('#popups-container');

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

    $('.edit-cproduct').click(function () {
        let fields = $(this).parent().find('td');
        console.log(fields.text())
        let id = fields.eq(0).text();
        let name = fields.eq(1).text();
        let price = parseInt(fields.eq(2).text());
        let item =`
            <div class='product-edit-popup'>
                <div class='edit-current-value'>
                    <div>ID</div>
                    <div>${id}</div>
                </div>
                <div class='edit-current-value'>
                    <div>Name</div>
                    <div>${name}</div>
                </div>
                <div class='edit-current-value'>
                    <div>Price</div>
                    <div>${price}</div>
                </div>
                <div class='edit-current-value'>
                    <div>New Name</div>
                    <input type='text' value='${name}' id='editProductName'>
                </div>
                <div class='edit-current-value'>
                    <div>New Price</div>
                    <input type='number' value='${price}' id='editProductPrice'>
                </div>
                <button>Edit</button>
            </div>
        `
        popupContainer.find('*').not('#exit-popup').remove();
        popupContainer.append(item);
        popupContainer.css('display', 'flex');
    });
});