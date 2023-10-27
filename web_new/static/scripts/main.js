$(document).ready(function(){
    const alertContainer = $('#alertPopup .alertPopupMessage');
    function customAlert(message) {
        alertContainer.text(message);
        alertContainer.parent().css('display', 'flex');
    }

    function setCookie(name, value, days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        const expires = "expires=" + date.toUTCString();
        document.cookie = name + "=" + value + "; " + expires;
    }

    function getCookie(name) {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.indexOf(name + "=") === 0) {
                return cookie.substring(name.length + 1, cookie.length);
            }
        }
        return "";
    }

    function deleteCookie(name) {
        document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    }

    // Usage:
    // setCookie("cartItems", JSON.stringify(cartData), 7);
    // const cartData = JSON.parse(getCookie("cartItems"));

    var cartCSRF = $('#cart_csrf').val();
    const headers = {
        'X-CSRFToken': cartCSRF,
        'Content-Type': 'application/json'
    };

    function addToCart(data) {
        let response = $.ajax({
            url:'/cart',
            type: 'POST',
            data: data,
            headers: headers
        });
        return response;
    }

    function updateCart(json) {
        let response = $.ajax({
            url: '/cart',
            type: 'PUT',
            data: json,
            headers: headers
        });
        return response;
    }

    function deleteFromCart(json) {
        let response = $.ajax({
            url: '/cart',
            type: 'DELETE',
            data: json,
            headers: headers
        });
        return response;
    }

    function getCart() {
        let response = $.ajax({
            type: 'GET',
            url: '/cart',
            headers: headers,
            error: function (err) {
                customAlert("There was a problem loading the cart");
            }
        });
        return response;
    }


    getCart().then(response => {
        if (response.cart) {
            setCookie('cartItems', JSON.stringify(response.cart), 30);
        }else {
            console.log(response);
            customAlert('There was a problem loading the cart');
        }
    });
    const cartData = JSON.parse(getCookie("cartItems"));
    const cartTotal = $('#cartTotal');
    var cartTotalValue = parseInt($('#cartTotal').text());

    // default cart display
    function defaultCartDisplayShow() {
        $('.cart-content-products').find('*').not('.default-cart-display, .default-cart-display *').remove();
        $('.default-cart-display').css('display', 'flex');
    }

    function defaultCartDisplayHide() {
        $('.default-cart-display').hide()
    }

    // loading cart items to cart
    if (cartData.length > 0) {
        $('.cart-content-products').empty();
        for (let i = 0; i < cartData.length; i++) {
            let item = `
                <div class='cart-content-product flex flex-cc'>
                <div class='cart-content-product-details'>
                    <div class='cart-product-image'>
                        <img src="../static/images/${cartData[i].image}" alt="cake">
                        <div class='delete-cart-product flex-cc'>
                            <span class="material-symbols-outlined">
                                close
                            </span>
                        </div>
                    </div>
                    <div class='cart-product-name'>${cartData[i].name}</div>
                </div>
                <div class='cart-content-product-quantity flex'>
                    <div class="cart-content-product-quantity-decreament flex">
                        <span class="material-symbols-outlined">
                            remove
                        </span>
                    </div>
                    <div class="cart-content-product-quantity-value flex-cc">
                        ${cartData[i].quantity}
                    </div>
                    <div class="cart-content-product-quantity-increament flex">
                        <span class="material-symbols-outlined">
                            add
                        </span>
                    </div>
                </div>
                <div class='cart-content-product-price'>${cartData[i].price * cartData[i].quantity}</div>
                <input type='hidden' name='product_id' value='${cartData[i].product_id}' class='product-id-cart'>
                <input type='hidden' name='product_price' value='${cartData[i].price}' class='product-price-cart'>
            </div>
            `;
            let itemTotal = cartData[i].quantity * cartData[i].price;
            cartTotalValue += itemTotal;
            $('.cart-content-products').append(item);
        }
        cartTotal.text(cartTotalValue);
    }else {
        defaultCartDisplayShow()
    }

    // cart items
    function cartCurrentItems() {
        return $('.cart-content-product');
    }
    function cartCurrentNames() {
        return $('.cart-content-product .cart-content-product-details .cart-product-name').map(function() {
            return $(this).text();
        }).get();
    }

    // ************Checking if cart is empty***********
    function checkEmptyCart() {
        let cartItems = $('.cart-content-product');
        if (cartItems.length > 0){
            return false;
        }else {
            return true;
        }
    }


    // adding product to cart when clicked
    $('.product-add-to-cart').click(function(){
        let productDetails = $(this).parent()
        var name = productDetails.find('.product-details .product-name').text();
        var price = parseInt(productDetails.find('.product-details .product-price').text().split(' ')[1]);
        var productId = productDetails.find('.product-details .product-id-cart').val();
        var productImage = productDetails.find('.product-details .product-image-cart').val()
        let newQuantity;
        // Check if product is already in cart
        if (cartCurrentNames().includes(name)) {
            for (let i = 0; i < cartCurrentItems().length; i++) {
                let productName = cartCurrentItems().eq(i).find('.cart-content-product-details .cart-product-name').text();
                let quantityContainer = cartCurrentItems().eq(i).find('.cart-content-product-quantity .cart-content-product-quantity-value');
                let quantity = parseInt(cartCurrentItems().eq(i).find('.cart-content-product-quantity .cart-content-product-quantity-value').text());
                let totalContainer = cartCurrentItems().eq(i).find('.cart-content-product-price');
                if (name === productName) {
                    quantityContainer.text(quantity + 1);
                    newQuantity = parseInt(quantityContainer.text());
                    totalContainer.text(newQuantity * price);
                    cartTotalValue += price;
                    cartTotal.text(cartTotalValue);
                    break;
                }
            }
        }else{
            let cart = $('.cart-content-products');
            if (checkEmptyCart() === true) {
                defaultCartDisplayHide();
            }
            let newItem = `
            <div class='cart-content-product flex flex-cc'>
                <div class='cart-content-product-details'>
                    <div class='cart-product-image'>
                        <img src="../static/images/${productImage}" alt="cake">
                        <div class='delete-cart-product flex-cc'>
                            <span class="material-symbols-outlined">
                                close
                            </span>
                        </div>
                    </div>
                    <div class='cart-product-name'>${name}</div>
                </div>
                <div class='cart-content-product-quantity flex'>
                    <div class="cart-content-product-quantity-decreament flex">
                        <span class="material-symbols-outlined">
                            remove
                        </span>
                    </div>
                    <div class="cart-content-product-quantity-value flex-cc">
                        1
                    </div>
                    <div class="cart-content-product-quantity-increament flex">
                        <span class="material-symbols-outlined">
                            add
                        </span>
                    </div>
                </div>
                <div class='cart-content-product-price'>${price}</div>
                <input type='hidden' name='product_id' value='${productId}' class='product-id-cart'>
                <input type='hidden' name='product_price' value='${price}' class='product-price-cart'>
            </div>
            `;
            cart.append(newItem);
            newQuantity = 1;
            cartTotalValue += price;
            cartTotal.text(cartTotalValue);
        }
        // Editing the cookie after adding the items
        for (let i = 0; i < cartData.length; i++) {
            if (cartData[i].name === name) {
                cartData.splice(i, 1);
            }
        }
        var cartItem = {
            'name': name,
            'product_id': productId,
            'price': price,
            'image': productImage,
            'quantity': newQuantity
        };
        // adding to cookie
        cartData.push(cartItem);
        setCookie('cartItems', JSON.stringify(cartData), 30);

        // updating in server
        if (newQuantity === 1) {
            addToCart(JSON.stringify(cartItem)).then(response => {
                if (response.error) {
                    customAlert("There was a problem adding item to cart");
                }
            });
        }else {
            updateCart(JSON.stringify(cartItem)).then(response =>  {
                if (response.error) {
                    customAlert('There was a problem updating the cart');
                }
            });
        }


    });

    // empty the cart
    $('#emptyCart').click(function() {
        confirm('Press \'OK\' to clear the shopping Cart');
        defaultCartDisplayShow();
        cartTotal.text(0);
        for (let i = 0; i < cartData.length; i++) {
            deleteFromCart(cartData[i]);
        }
        deleteCookie('cartItems');
    });

    // increase quantity in cart
    $('.cart-content-products').on('click', '.cart-content-product .cart-content-product-quantity-increament', function() {
        let buttonContainer = $(this).parent()
        let quantityContainer = buttonContainer.find('.cart-content-product-quantity-value');
        let totalContainer = buttonContainer.parent().find('.cart-content-product-price');
        let price = parseInt(buttonContainer.parent().find('.product-price-cart').val());
        let currentQuantity = parseInt(quantityContainer.text());
        quantityContainer.text(currentQuantity + 1);
        totalContainer.text((currentQuantity + 1) * price);

        // editing the cookie after increase
        let productName = buttonContainer.parent().find('.cart-content-product-details .cart-product-name').text();
        for (let i = 0; i < cartData.length; i++) {
            if (cartData[i].name === productName) {
                cartData[i].quantity = currentQuantity + 1;
                updateCart(cartData[i]);
                break;
            }
        }
        cartTotalValue += price;
        cartTotal.text(cartTotalValue);
        setCookie('cartItems', JSON.stringify(cartData), 30);
    });

    // Decrease quantity in the cart
    $('.cart-content-products').on('click', '.cart-content-product .cart-content-product-quantity-decreament', function() {
        let buttonContainer = $(this).parent()
        let quantityContainer = buttonContainer.find('.cart-content-product-quantity-value');
        let totalContainer = buttonContainer.parent().find('.cart-content-product-price');
        let price = parseInt(buttonContainer.parent().find('.product-price-cart').val());
        let currentQuantity = parseInt(quantityContainer.text());
        let productName = buttonContainer.parent().find('.cart-content-product-details .cart-product-name').text();
        if (currentQuantity === 1) {
            buttonContainer.parent().remove();
            defaultCartDisplayShow();
            // remove from cookie
            for (let i = 0; i < cartData.length; i++) {
                if (cartData[i].name === productName) {
                    cartData.splice(i, 1);
                    deleteFromCart(cartData[i]);
                }
            }
        }else {
            quantityContainer.text(currentQuantity - 1);
            totalContainer.text((currentQuantity + 1) * price);
            for (let i = 0; i < cartData.length; i++) {
                if (cartData[i].name === productName) {
                    cartData[i].quantity = currentQuantity - 1;
                    updateCart(cartData[i]);
                }
            }
        }
        cartTotalValue -= price;
        cartTotal.text(cartTotalValue);
        setCookie('cartItems', JSON.stringify(cartData), 30);
    });

    // delete cart product 
    $('.cart-content-products').on('click', '.cart-content-product .delete-cart-product', function(){
        let currentProduct = $(this).parent().parent().parent();
        let productName = currentProduct.find('.cart-content-product-details .cart-product-name').text();
        let productTotal = parseInt(currentProduct.find('.cart-content-product-price').text());
        // remove from cookie
        for (let i = 0; i < cartData.length; i++) {
            if (cartData[i].name === productName) {
                cartData.splice(i, 1);
            }
        }
        currentProduct.remove();
        cartTotalValue -= productTotal;
        cartTotal.text(cartTotalValue);
        if (checkEmptyCart() === true) {
            defaultCartDisplayShow();
        }
        setCookie('cartItems', JSON.stringify(cartData), 30);
    });

    $('#logout-btn').click(function() {
        deleteCookie('access_token');
        deleteCookie('csrf_token');
    });
});