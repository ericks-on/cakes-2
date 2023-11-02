import { customAlert, alertContainer, setCookie, getCookie, deleteCookie } from "./main.js";

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
        setCookie('activePage', '#products-management');
    });

    $('#dashboardButton').click(function () {
        activePage.hide();
        activePage = $('#dashboard');
        activePage.show();
        setCookie('activePage', '#dashboard');
    });

    $('#inventoryButton').click(function () {
        activePage.hide();
        activePage = $('#inventory-management');
        activePage.show();
        setCookie('activePage', '#inventory-management');
    });

    $('#userPageButton').click(function () {
        activePage.hide();
        activePage = $('#user-management');
        activePage.show();
        setCookie('activePage', '#user-management');
    });

    $('#ordersButton').click(function () {
        activePage.hide();
        activePage = $('#orders');
        activePage.show();
        setCookie('activePage', '#orders');
    });

    $('#notificationsButton').click(function () {
        activePage.hide();
        activePage = $('#notifications-management');
        activePage.show();
        setCookie('activePage', '#notifications-management');
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
        let fields = $(this).parent().parent().find('td');
        let id = fields.eq(0).text();
        console.log(id)
        let name = fields.eq(1).text();
        let price = parseInt(fields.eq(2).text());
        let item =`
            <div class='product-edit-popup'>
                <div class='edit-current-value'>
                    <div class='ec-label'>ID</div>
                    <div class='ec-value' id='ecProductId'>${id}</div>
                </div>
                <div class='edit-current-value'>
                    <div class='ec-label'>Name</div>
                    <div class='ec-value'>${name}</div>
                </div>
                <div class='edit-current-value'>
                    <div class='ec-label'>Price</div>
                    <div class='ec-value'>${price}</div>
                </div>
                <div class='edit-current-value'>
                    <div class='ec-label'>New Name</div>
                    <input class='ec-value' type='text' value='${name}' id='editProductName'>
                </div>
                <div class='edit-current-value'>
                    <div class='ec-label'>New Price</div>
                    <input class='ec-value' type='number' value=${price} id='editProductPrice'>
                </div>
                <button id='submitEdit'>Edit</button>
            </div>
        `
        popupContainer.find('*').not('#exit-popup, #exit-popup *').remove();
        popupContainer.append(item);
        popupContainer.css('display', 'flex');
    });

    popupContainer.on('click', '#submitEdit', function() {
        let newName = $(this).parent().find('#editProductName').val();
        let newPrice = parseInt($(this).parent().find('#editProductPrice').val());
        let id = $(this).parent().find('#ecProductId').text();
        $.ajax({
            url: '/products',
            method: 'PUT',
            headers: {
                'X-CSRFToken': $('#csrf_token').val()
            },
            data: JSON.stringify({
                'name': newName,
                'price': newPrice,
                'id': id
            }),
            contentType: 'application/json',
            success: function() {
                alert("Product added Successfully");
                location.reload();
            },
            error: function() {
                customAlert("There was a problem editing the product");
            }
        });
    });

    $(window).on('load', function () {
        let active = getCookie('activePage');
        if (active != ""){
            activePage.hide();
            activePage = $(active);
            activePage.show();
        }else {
            activePage.show();
        }
    });

    $('#logout').click(function() {
        deleteCookie('activePage');
    });
});