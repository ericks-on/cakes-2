$(document).ready(function() {
    // Socket.io connection
    var socket = io('/admin');
    $('#chat-send-btn').click(function() {
        var message = $('#chat-input').val();
        socket.emit('send', {"msg": message});
        $('#chat-input').val('');
        let newChat = `
        <div class="chat-messages-container d-flex-column chat-outgoing">
            <div class="chat-message-header"></div>
            <div class="chat-message">
                ${message}
            </div>
        </div>
        `
        $('.chat-dialogue').append(newChat);
    });
    socket.on('from_client', function(json) {
        let newChat = `
        <div class="chat-messages-container d-flex-column chat-incoming">
            <div class="chat-message-header"></div>
            <div class="chat-message">
                ${json.msg}
            </div>
        </div>
        `
        $('.chat-dialogue').append(newChat);
    });
});