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
    // Usage:
    // setCookie("cartItems", JSON.stringify(cartData), 7);
    // const cartData = JSON.parse(getCookie("cartItems"));

    // ading to cart
    $('.product-add-to-cart').click(function(){
        let newItem = `
        <div class='cart-content-product flex flex-cc'>
        <div class='cart-content-product-details'>
            <div class='cart-product-image'>
                <img src="../static/images/donut.jpg" alt="cake">
                <div class='delete-cart-product flex-cc'>
                    <span class="material-symbols-outlined">
                        close
                    </span>
                </div>
            </div>
            <div class='cart-product-name'>12-pack</div>
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
        <div class='cart-content-product-price'>960</div>
    </div>
    `;
    let cart = $('.cart-content-products');
    cart.append(newItem);
    });
});