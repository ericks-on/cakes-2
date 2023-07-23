$(document).ready(function() {
    // Socket.io connection
    var socket = io('/admin');
    $('#chat-send-btn').click(function() {
        var message = $('#chat-input').val();
        if (message == '') {
            alert('Please enter a message');
            return;
        }
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
                    $('.chat-dialogue').empty();
                    $("#chat-id").val(chat_id);
                    for (var i = 0; i < data.messages.length; i++) {
                        if (data.messages[i].sender == 'client') {
                            let newChat = `
                            <div class="chat-messages-container d-flex-column chat-outgoing">
                                <div class="chat-message-header"></div>
                                <div class="chat-message">
                                    ${data.messages[i].message}
                                </div>
                            </div>
                            `
                            $('.chat-dialogue').append(newChat);
                        } else {
                            let newChat = `
                            <div class="chat-messages-container d-flex-column chat-incoming">
                                <div class="chat-message-header"></div>
                                <div class="chat-message">
                                    ${data.messages[i].message}
                                </div>
                            </div>
                            `
                        $('.chat-dialogue').append(newChat);
                    }
                }
            }
            $('.default-chat-window').hide();
            $('.chat-window').show();
            });
    });
});