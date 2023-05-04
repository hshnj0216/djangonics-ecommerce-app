$(function() {
    $('.cart-item-select').on('change', function() {
        //when the item quantity is update make an AJAX call
        let url = '';
        let qty = $(this).val();
        $.ajax({
            url = url,
            data: {
                qty,
            },
            success: function(data) {
                $('#item-counter').text(data);
            }
        });
    });
});