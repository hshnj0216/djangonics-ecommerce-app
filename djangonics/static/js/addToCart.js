$(function() {
    console.log("productAction.js loaded");
    $('.add-to-cart-button').on('click', function(event) {
        event.preventDefault();
        let qty = $('.qty').val();
        let form = $(this).parent('form');
        let url = form.data('add-to-cart-url');
        let productId = form.data('product-id');
        let csrfToken = $("input[name='csrfmiddlewaretoken']").val();
        alert(`productId: ${productId}, url: ${url}`);
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                qty,
                product_id: productId,
                csrfmiddlewaretoken: csrfToken,
            },
            headers: {
                'X-CSRFToken': csrfToken,
            },
            success: function(data) {
                $('#item-counter').text(data['cart_item_count']);
            }
        });
    });
});
