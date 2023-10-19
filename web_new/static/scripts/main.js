$(document).ready(function(){
    // login
    $('#login-button').click(function(event){
        console.log('login button clicked')
        event.preventDefault();
        $.post('/', {
            username: $('#login-username').val(),
            password: $('#login-password').val()
        }, function(data, status){
            $('#loginForm').submit();
        }).fail(function(data, status){
            let errorMessages = JSON.parse(data.responseJSON['error'])['msg'];
            alert(errorMessages);
            return;
        });
    });

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

    // deleteCookie('cartItems');
    if (getCookie('cartItems') === "") {
        setCookie('cartItems', JSON.stringify([]), 30);
    }
    const cartData = JSON.parse(getCookie("cartItems"));

    // loading cart items to cart
    $('.cart-content-products').empty()
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
                <div class="cart-content-product-quantity-increament flex">
                    <span class="material-symbols-outlined">
                        remove
                    </span>
                </div>
                <div class="cart-content-product-quantity-value flex-cc">
                    ${cartData[i].quantity}
                </div>
                <div class="cart-content-product-quantity-decreament flex">
                    <span class="material-symbols-outlined">
                        add
                    </span>
                </div>
            </div>
            <div class='cart-content-product-price'>${cartData[i].price}</div>
            <input type='hidden' name='product_id' value='${cartData[i].product_id}' class='product-id-cart'>
        </div>
        `;
        $('.cart-content-products').append(item);
    }

    // adding product to cart when clicked
    $('.product-add-to-cart').click(function(){
        let productDetails = $(this).parent()
        var name = productDetails.find('.product-details .product-name').text();
        var price = parseInt(productDetails.find('.product-details .product-price').text().split(' ')[1]);
        var productId = productDetails.find('.product-details .product-id-cart').val();
        var productImage = productDetails.find('.product-details .product-image-cart').val()
        var cartCurrentItems = $('.cart-content-product');
        var cartCurrentNames = $('.cart-content-product .cart-content-product-details .cart-product-name').map(function(){
            return $(this).text();
        }).get();
        let newQuantity;
        if (cartCurrentNames.includes(name)) {
            for (let i = 0; i < cartCurrentItems.length; i++) {
                let productName = cartCurrentItems.eq(i).find('.cart-content-product-details .cart-product-name').text();
                let quantityContainer = cartCurrentItems.eq(i).find('.cart-content-product-quantity .cart-content-product-quantity-value');
                let quantity = parseInt(cartCurrentItems.eq(i).find('.cart-content-product-quantity .cart-content-product-quantity-value').text());
                if (name === productName) {
                    quantityContainer.text(quantity + 1);
                    newQuantity = parseInt(quantityContainer.text());
                    break;
                }
            }
        }else{
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
                    <div class="cart-content-product-quantity-increament flex">
                        <span class="material-symbols-outlined">
                            remove
                        </span>
                    </div>
                    <div class="cart-content-product-quantity-value flex-cc">
                        1
                    </div>
                    <div class="cart-content-product-quantity-decreament flex">
                        <span class="material-symbols-outlined">
                            add
                        </span>
                    </div>
                </div>
                <div class='cart-content-product-price'>${price}</div>
                <input type='hidden' name='product_id' value='${productId}' class='product-id-cart'>
            </div>
            `;
            let cart = $('.cart-content-products');
            cart.append(newItem);
            newQuantity = 1;
        }
        for (let i = 0; i < cartData.length; i++) {
            if (cartData[i].name === name) {
                cartData.splice(i, 1);
            }
        }
        var cartItem = {'name': name, 'product_id': productId, 'price': price, 'image': productImage, 'quantity': newQuantity};
        cartData.push(cartItem);
        setCookie('cartItems', JSON.stringify(cartData), 30);
    });
});