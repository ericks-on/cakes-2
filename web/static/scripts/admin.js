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
    var activePageBtn = $('#dashboardButton');

    $('#productPageButton').click(function () {
        activePage.hide();
        activePageBtn.toggleClass('active-sidebar');
        $(this).toggleClass('active-sidebar');
        activePageBtn = $(this);
        activePage = $('#products-management');
        activePage.show();
        let historyCookie = JSON.stringify({
            "page": "#products-management",
            "button": "#productPageButton"
        });
        setCookie('activePage', historyCookie);
    });

    // ===========Page Navigation============
    $('#dashboardButton').click(function () {
        activePage.hide();
        activePageBtn.toggleClass('active-sidebar');
        $(this).toggleClass('active-sidebar');
        activePageBtn = $(this);
        activePage = $('#dashboard');
        activePage.show();
        let historyCookie = JSON.stringify({
            "page": "#dashboard",
            "button": "dashboardButton"
        });
        setCookie('activePage', historyCookie);
    });

    $('#inventoryButton').click(function () {
        activePage.hide();
        activePageBtn.toggleClass('active-sidebar');
        $(this).toggleClass('active-sidebar');
        activePageBtn = $(this);
        activePage = $('#inventory-management');
        activePage.show();
        let historyCookie = JSON.stringify({
            "page": "#inventory-management",
            "button": "#inventoryButton"
        });
        setCookie('activePage', historyCookie);
    });

    $('#userPageButton').click(function () {
        activePage.hide();
        activePageBtn.toggleClass('active-sidebar');
        $(this).toggleClass('active-sidebar');
        activePageBtn = $(this);
        activePage = $('#user-management');
        activePage.show();
        let historyCookie = JSON.stringify({
            "page": "#user-management",
            "button": "#userPageButton"
        });
        setCookie('activePage', historyCookie);
    });

    $('#ordersButton').click(function () {
        activePage.hide();
        activePageBtn.toggleClass('active-sidebar');
        $(this).toggleClass('active-sidebar');
        activePageBtn = $(this);
        activePage = $('#orders');
        activePage.show();
        let historyCookie = JSON.stringify({
            "page": "#orders",
            "button": "#ordersButton"
        });
        setCookie('activePage', historyCookie);
    });

    $('#notificationsButton').click(function () {
        activePage.hide();
        activePageBtn.toggleClass('active-sidebar');
        $(this).toggleClass('active-sidebar');
        activePageBtn = $(this);
        activePage = $('#notifications-management');
        activePage.show();
        let historyCookie = JSON.stringify({
            "page": "#notifications-management",
            "button": "#notificationsButton"
        });
        setCookie('activePage', historyCookie);
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

    // ============handling Refresh============
    $(window).on('load', function () {
        let active = getCookie('activePage');
        if (active != ""){
            active = JSON.parse(active);
            activePage.hide();
            activePage = $(active.page);
            activePageBtn = $(active.button);
            activePageBtn.addClass('active-sidebar');
            activePage.show();
        }else {
            activePage.show();
            activePageBtn.addClass('active-sidebar');
        }
    });

    // ======Delete cookie after logout=========
    $('#logout').click(function() {
        deleteCookie('activePage');
    });

    // ===========adding notification============
    $('#addNotificationsBtn').click(function() {
        let message = $('#notification-message').val()
        $.ajax({
            url: "/notifications",
            method: "POST",
            data: JSON.stringify({
                "message": message
            }),
            headers: {
                "X-CSRFToken": $('#csrf_token').val()
            },
            contentType: "application/json",
            success: function(){
                alert("Notification Added successfully");
                location.reload();
            },
            fail: function() {
                customAlert("There was a problem adding the Notification");
            }
        });
    });

    // ===========adding new users==============
    $('#addUserButton').click(function() {
        let firstName = $('#addUserFirstName');
        let lastName = $('#addUserLastName');
        let email = $('#addUserEmail');
        let phone = $('#addUserPhone');
        let username = $('#addUserUserName');
        let password = $('#addUserPassword');
        let confirmPassword = $('#confirmUserPassword');
        if (password.val() !== confirmPassword.val()){
            alert("The two passwords must be the same");
            return;
        }
        $.ajax({
            url: '/users',
            method: 'POST',
            headers: {
                'X-CSRFToken': $('#csrf_token').val()
            },
            contentType: 'application/json',
            data: JSON.stringify({
                'first_name': firstName.val(),
                'last_name': lastName.val(),
                'email': email.val(),
                'phone': phone.val(),
                'username': username.val(),
                'password': password.val()
            }),
            success: function() {
                alert('User added successfully');
                location.reload();
            },
            error: function() {
                customAlert("There was a problem adding user");
            }
        })
    });

    // =============deleting users=================
    $('.user-remove').click(function () {
        if (confirm("You are about to Delete the user")) {
            let userID = $(this).parent().parent().find('td').eq(0).text();
            $.ajax({
                url: "/users",
                method: "DELETE",
                headers: {
                    'X-CSRFToken': $('#csrf_token').val()
                },
                data: JSON.stringify({
                    "userID": userID
                }),
                contentType: "application/json",
                success: function () {
                    alert("Deleted user successfully");
                    location.reload();
                },
                error: function () {
                    customAlert("Error Deleting user");
                }
            });
        }else {
            return;
        }
    });

});