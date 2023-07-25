$(document).ready(function() {
    // Socket.io connection
    var socket = io('/client');

    // scroll to last message
    function scrollToLastMessage() {
        const messageContainer = $(".chat-dialogue");
        messageContainer.scrollTop(messageContainer.prop("scrollHeight"));
    }

    // sending message
    $('#chat-send-btn').click(function() {
        var message = $('#chat-input').val();
        var chat_id = $('#chat-id').val();
        if (message == '') {
            alert('Please enter a message');
            return;
        }
        payload = {
            "message": message
        };
        $.post('/api/chat/' + chat_id + '/messages', payload, function(data) {
            if (data.status == 'success') {
                socket.emit('send', {"msg": data.message, "chat_id": chat_id});
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
                scrollToLastMessage();
            }
        }).fail(function() {
            alert('Please enter a message');
        });
    });

    //new chat popup
    $('#new-chat-btn').click(function() {
        $('#popups-container').css('display', 'flex');
        $('.new-chat-popup , .new-chat-popup *').show();

    });

    // creating new chat
    $('#create-chat-btn').click(function() {
        var subject = $('#new-chat-subject').val();
        var payload = {
            "subject": subject
        };
        $.post('/api/chat', payload, function(data) {
            if (data.status == 'success') {
                $('#popups-container').hide();
                $('#popups-container').find('*').not('#exit-btn, #exit-btn *').hide();
                $('#new-chat-subject').val('');
                let newChat = `
                <div class="chats-info d-flex-column">
                    <div class="chats-info-header d-flex">
                        <p>To:</p>
                        <div class="chats-info-recepient">Admin</div>                
                    </div>
                    <div class="chats-info-row d-flex">
                        <div class="chats-info-row-subject">Subject:</div>
                        <div class="chats-info-row-value">${data.subject}</div>
                    </div>
                    <input type="hidden" name="chat-id-side" value="${data.chat_id}">
                </div>
                `
                $('.chats-container').prepend(newChat);
            }
        });
    });

    // click chat to display messages
    $(".chats-info").click(function() {
        var chat_id = $(this).find('input[name="chat-id-side"]').val();
        var url = '/api/chat/' + chat_id + '/messages';
        $.get(url, function(data) {
            if (data.status == 'success') {
                $('.chat-dialogue').not(":last").empty();
                $("#chat-id").val(chat_id);
                for (var i = 0; i < data.messages.length; i++) {
                    if (data.messages[i].sender == 'client') {
                        let newChat = `
                        <div class="chat-messages-container d-flex-column chat-outgoing">
                            <div class="chat-message-header"></div>
                            <div class="chat-message">
                                ${data.messages[i].content}
                            </div>
                        </div>
                        `
                        $('.chat-dialogue').append(newChat);
                    } else {
                        let newChat = `
                        <div class="chat-messages-container d-flex-column chat-incoming">
                            <div class="chat-message-header"></div>
                            <div class="chat-message">
                                ${data.messages[i].content}
                            </div>
                        </div>
                        `
                    $('.chat-dialogue').append(newChat);
                }
            }
            $('.default-chat-window').hide();
            $('.chat-window').show();
            scrollToLastMessage();
        }
        });
    });

    // scroll to last message on chat
    $(".scroll-bottom-new-msg").click(function() {
        scrollToLastMessage();
        $('.new-msg-on-current-chat').hide();
        $('.new-msg-count').empty();
    });

    // scroll to message btn apperance
    $(".chat-dialogue").scroll(function() {
        let scrolled = $(".chat-dialogue").prop("scrollHeight") -
        ($(".chat-dialogue").scrollTop() + $(".chat-dialogue").height());
        if (scrolled > 10) {
            $('.new-msg-on-current-chat').css('display', 'flex');
        } else {
            $('.new-msg-on-current-chat').hide();
        }
    });
});