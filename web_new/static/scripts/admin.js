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
});