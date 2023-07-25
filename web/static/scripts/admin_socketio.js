$(document).ready(function() {
    // scroll to last message
    function scrollToLastMessage() {
        const messageContainer = $(".chat-dialogue");
        messageContainer.scrollTop(messageContainer.prop("scrollHeight"));
    }

    // Socket.io connection
    var socket = io('/admin');
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