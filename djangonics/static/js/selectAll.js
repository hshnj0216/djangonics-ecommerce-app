$(function() {
    console.log("select all loaded");
    $('#select-all-check').on('change', function() {
        var isChecked = $(this).is(':checked');
        $('.cart-item-checkbox').prop('checked', isChecked);
    });
});