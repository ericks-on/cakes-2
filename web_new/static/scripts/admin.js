$(document).ready(function () {
    $("#incoming-orders").DataTable({
        "ordering": false,
        "pageLength": 5,
        "lengthChange": false,
        "info": false,
    });

    $('#current-notifications').DataTable({
        "ordering": false,
        "pageLength": 5,
        "lengthChange": false,
        "info": false,
        "searching": false,
    });

    $('#current-products').DataTable({
        "ordering": false,
        "pageLength": 5,
        "lengthChange": false,
        "info": false,
    });

    $('#products-inventory').DataTable({
        "ordering": false,
        "pageLength": 5,
        "lengthChange": false,
        "info": false,
    });

    $('#current-users').DataTable({
        "ordering": false,
        "pageLength": 5,
        "lengthChange": false,
        "info": false,
    });

    $('#current-inventory').DataTable({
        "ordering": false,
        "pageLength": 5,
        "lengthChange": false,
        "info": false,
    });

    var activePage = $('#dashboard');

    $('#productPageButton').click(function () {
        activePage.hide();
        activePage = $('#products-management');
        activePage.show();
    });

    $('#dashboardButton').click(function () {
        activePage.hide();
        activePage = $('#dashboard');
        activePage.show();
    });

    $('#inventoryButton').click(function () {
        activePage.hide();
        activePage = $('#inventory-management');
        activePage.show();
    });

    $('#userPageButton').click(function () {
        activePage.hide();
        activePage = $('#user-management');
        activePage.show();
    });

    $('#ordersButton').click(function () {
        activePage.hide();
        activePage = $('#orders');
        activePage.show();
    });

    $('#notificationsButton').click(function () {
        activePage.hide();
        activePage = $('#notifications-management');
        activePage.show();
    });
});