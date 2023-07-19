$(document).ready(function() {
    $('#exit-btn').click(function() {
        $('#popups-container').hide();
        $('#popups-container').find('*').not('#exit-btn, #exit-btn *').hide();
    });

});