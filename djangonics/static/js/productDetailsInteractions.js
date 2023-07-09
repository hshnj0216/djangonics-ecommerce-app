$(function() {
    //Fill the stars when hovering
    $('#user-rating span').hover(function() {
        if($(this).hasClass('fa')) {
            $(this).prevAll().addBack().removeClass('fa');
            $(this).prevAll().addBack().addClass('far');
        } else {
             $(this).prevAll().addBack().removeClass('far');
             $(this).prevAll().addBack().addClass('fa');
        }
    });

    //Call the create rating view when a star is clicked
    $('#user-rating span').click(function() {
        let rating = $(this).data('rating');
        let productId = $(this).data('product-id');
        $.ajax({
            url: '/products/submit_rating/',
            type: 'POST',
            data: {
                rating,
                product_id: productId,
            },
            success: function(data) {
                //Re-render the user rating
            },
            error: function(data) {
                alert('An error occured');
            }
        });
    });
});