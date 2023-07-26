$(document).ready(function () {
    const inputField = $('#chat-emoji-btn');
    new emojiMart.EmojiPicker({
        autoHide: true, // The picker will automatically hide after selecting an emoji
        showPreview: false, // Don't show the preview of the emoji when hovering
        showSearch: false, // Disable the search bar
        categories: ['smileys', 'people', 'nature', 'food', 'activity', 'places', 'objects', 'symbols'], // Customize the visible categories
    }).bindToInput(inputField);
});
