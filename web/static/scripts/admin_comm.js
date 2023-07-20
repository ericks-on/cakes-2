$(document).ready(function() {
    // Socket.io connection
    var socket = io('/admin');
    $('#chat-send-btn').click(function() {
        var message = $('#chat-input').val();
        socket.emit('send', {"msg": message});
        $('#chat-input').val('');
    });
    socket.on('from_client', function(json) {
        $.get('/api/verify', function(data) {
            var cls;
            if (data.username === json.sender) {
                cls = 'chat-outgoing';
            } else {
                cls = 'chat-incoming';
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