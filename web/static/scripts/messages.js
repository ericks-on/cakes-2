$(document).ready(function() {
    // Socket.io connection
    var socket = io();

    $('#chat-send-btn').click(function() {
        var message = $('#chat-input').val();
        socket.emit('client_send', message);
        $('#chat-input').val('');

        socket.on('chat', function(json) {
            console.log("json " + json);
            $.get('/api/verify', function(data) {
                console.log(data);
                if (data.user_type == json.sender) {
                    var cls = 'chat-outgoing';
                } else {
                    var cls = 'chat-incoming';
                }
                let newChat = `
                <div class="chat-messages-container d-flex-column ${cls}">
                    <div class="chat-message-header"></div>
                    <div class="chat-message">
                        ${json.message}
                    </div>
                </div>
                `
                $('.chat-dialogue').append(newChat);
            });
        });
});
});