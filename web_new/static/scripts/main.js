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
});