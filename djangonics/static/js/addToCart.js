$(function() {
    console.log("productAction.js loaded");
    $('.add-to-cart-button').on('click', function(event) {
        event.preventDefault();
        let qty = $('.qty').val();
        let form = $(this).parent('form');
        let url = form.data('add-to-cart-url');
        let productId = form.data('product-id');
        let csrfToken = $("input[name='csrfmiddlewaretoken']").val();
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
              $('.toast').removeClass('show');
              $('.toast').addClass('show');
              $('.toast').fadeTo(5000, 0, 'swing', function() {
                $(this).removeClass('show');
                $(this).css('opacity', '');
              });
            }
        });
    });
});
