import { customAlert, alertContainer, setCookie, getCookie, deleteCookie, showPopup } from "./main.js";

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

    // ==========users password reset popup=========
    $('.user-reset').click(function () {
        let userID = $(this).parent().parent().find('td').eq(0).text();
        $.ajax({
            url: `/users/${userID}`,
            methods: "GET",
            headers: {
                "X-CSRFToken": $('#csrf_token').val()
            },
            success: function(response) {
                let item =`
                    <div class='user-reset-popup flex-column'>
                        <div class='edit-current-value'>
                            <div class='ec-label'>ID</div>
                            <div class='ec-value' id='ecUserId'>${response.id}</div>
                        </div>
                        <div class='edit-current-value'>
                            <div class='ec-label'>Name</div>
                            <div class='ec-value'>${response.first_name + " " + response.last_name}</div>
                        </div>
                        <div class='edit-current-value'>
                            <div class='ec-label'>Email</div>
                            <div class='ec-value'>${response.email}</div>
                        </div>
                        <div class='edit-current-value'>
                            <div class='ec-label'>New Password</div>
                            <input class='ec-value' type='password' id='resetPassword'  readonly onfocus="this.removeAttribute('readonly');" onblur="this.setAttribute('readonly','');">
                        </div>
                        <div class='edit-current-value'>
                            <div class='ec-label'>Confirm Password</div>
                            <input class='ec-value' type='password' id='confirmPasswordReset'  readonly onfocus="this.removeAttribute('readonly');" onblur="this.setAttribute('readonly','');">
                        </div>
                        <button id='submitReset'>Edit</button>
                    </div>
                `
                $('#popups-container').append(item);
                showPopup();
            }
        });
    });

    // ==========reset request===========
    $('#popups-container').on('click', '.user-reset-popup #submitReset', function() {
        let userID = $(this).parent().find('#ecUserId').text();
        let password = $(this).parent().find("#resetPassword").val();
        let confirm = $(this).parent().find("#confirmPasswordReset").val();
        if (!password || !confirm) {
            alert("Please fill all the entries");
            return;
        }
        if (password !== confirm) {
            alert("The two passwords must be the same");
            return;
        }else {
            $.ajax({
                url: `/users/${userID}`,
                method: "PUT",
                headers: {
                    "X-CSRFToken": $("#csrf_token").val()
                },
                data: JSON.stringify({
                    "edit_password": "True",
                    "password": password
                }),
                contentType: 'application/json',
                success: function() {
                    alert("Password reset was successful");
                    location.reload()
                },
                error: function() {
                    customAlert("Error resseting password");
                }
            });
        }
    });

    // =======edit user details=========
    $(".user-edit").click(function() {
        let userID = $(this).parent().parent().find('td').eq(0).text();
        $.ajax({
            url: `/users/${userID}`,
            methods: "GET",
            headers: {
                "X-CSRFToken": $('#csrf_token').val()
            },
            success: function(response) {
                let item =`
                    <div class='user-edit-popup flex-column'>
                        <h2>Edit User</h2>
                        <p>***Only Enter values for the fields you wish to edit and leave the others blank</p>
                        <input type='hidden' id='editUserId' value='${response.id}'>
                        <div class="user-edit-popup-header flex">
                            <div class="edit-header-column"></div>
                            <div class="edit-header-column">Current</div>
                            <div class="edit-header-column">New</div>
                        </div>
                        <div class='user-edit-container flex-column'>
                            <div class="user-edit-row">
                                <div class='user-edit-label'>First Name</div>
                                <div class='user-edit-value'>${response.first_name}</div>
                                <input class='user-edit-new-value' value="" type='text' id='userEditFirstName'  readonly onfocus="this.removeAttribute('readonly');" onblur="this.setAttribute('readonly','');">
                            </div>
                            <div class="user-edit-row">
                                <div class='user-edit-label'>Last name</div>
                                <div class='user-edit-value'>${response.last_name}</div>
                                <input class='user-edit-new-value' value="" type='text' id='userEditLastName'  readonly onfocus="this.removeAttribute('readonly');" onblur="this.setAttribute('readonly','');">
                            </div>
                            <div class="user-edit-row">
                                <div class='user-edit-label'>Email</div>
                                <div class='user-edit-value'>${response.email}</div>
                                <input class='user-edit-new-value' value="" type='text' id='userEditEmail'  readonly onfocus="this.removeAttribute('readonly');" onblur="this.setAttribute('readonly','');">
                            </div>
                            <div class="user-edit-row">
                                <div class='user-edit-label'>Username</div>
                                <div class='user-edit-value'>${response.username}</div>
                                <input class='user-edit-new-value' value="" type='text' id='userEditUsername'  readonly onfocus="this.removeAttribute('readonly');" onblur="this.setAttribute('readonly','');">
                            </div>
                            <div class="user-edit-row">
                                <div class='user-edit-label'>Phone</div>
                                <div class='user-edit-value'>${response.phone}</div>
                                <input class='user-edit-new-value' value="" type='text' id='userEditPhone'  readonly onfocus="this.removeAttribute('readonly');" onblur="this.setAttribute('readonly','');">
                            </div>
                        </div>
                        <button id='submitUserEdit'>Edit</button>
                    </div>
                `
                $('#popups-container').append(item);
                showPopup();
            }
        });
    });
    $('#popups-container').on('click', "#submitUserEdit", function() {
        let userID = $(this).parent().find('#editUserId').val();
        let firstName = $(this).parent().find('#userEditFirstName').val();
        let lastName = $(this).parent().find('#userEditLastName').val();
        let email = $(this).parent().find('#userEditEmail').val();
        let username = $(this).parent().find('#userEditUsername').val();
        let phone = $(this).parent().find('#userEditPhone').val();
        var data = [firstName, lastName, email, username, phone];
        let message = "You are about to edit the following fields:\n";
        let editCount = 0;
        for (var i = 0; i < data.length; i++) {
            if (data[i]) {
                message += `-${data[i]}\n`;
                editCount++;
            }
        }
        if (editCount === 0) {
            alert("Please fill at least one field");
            return;
        }
        if (confirm(message)) {
            $.ajax({
                url: `/users/${userID}`,
                method: "PUT",
                headers: {
                    "X-CSRFToken": $("#csrf_token").val()
                },
                data: JSON.stringify({
                    "first_name": firstName,
                    "last_name": lastName,
                    "email": email,
                    "username": username,
                    "phone": phone
                }),
                contentType: 'application/json',
                success: function() {
                    alert("User details edited successfully");
                    location.reload()
                },
                error: function() {
                    customAlert("Error editing user details");
                }
            });
        }else {
            return;
        }
    });

    // =============Inventory================
    // ------adding inventory item-----------
    $("#add-new-inventory").click(function() {
        let item = `
            <div class='inventory-add-popup flex-column'>
                <h2>Add New Inventory Item</h2>
                <div class='inventory-add-row'>
                    <div class='inventory-add-label'>Name</div>
                    <input class='inventory-add-value' type='text' id='inventoryAddName'>
                </div>
                <div class='inventory-add-row'>
                    <div class='inventory-add-label'>Quantity</div>
                    <input class='inventory-add-value' type='number' id='inventoryAddQuantity'>
                </div>
                <div class='inventory-add-row'>
                    <div class='inventory-add-label'>Cost(Per unit)</div>
                    <input class='inventory-add-value' type='number' id='inventoryAddCost'>
                </div>
                <button id='submitInventoryAdd'>Add</button>
            </div>
        `
        $('#popups-container').append(item);
        showPopup();
    });
    $('#popups-container').on('click', '#submitInventoryAdd', function() {
        let name = $(this).parent().find('#inventoryAddName').val();
        let quantity = $(this).parent().find('#inventoryAddQuantity').val();
        let cost = $(this).parent().find('#inventoryAddCost').val();
        if (!name || !quantity || !cost) {
            alert("Please fill all the entries");
            return;
        }
        $.ajax({
            url: "/inventory",
            method: "POST",
            headers: {
                "X-CSRFToken": $("#csrf_token").val()
            },
            data: JSON.stringify({
                "name": name,
                "quantity": quantity,
                "cost": cost
            }),
            contentType: "application/json",
            success: function() {
                alert("Inventory item added successfully");
                location.reload();
            },
            error: function() {
                customAlert("Error adding inventory item");
            }
        });
    });
});