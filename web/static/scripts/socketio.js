$(document).ready(function() {
    // Socket.io connection
    var socket = io('/client');

    // events
    socket.on('recieve', function(json) {
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