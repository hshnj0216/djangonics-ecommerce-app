$(function() {

    //Handle add to cart functionality
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

    //Handle buy now


    //Fill the stars when hovering
    $('#user-rating span').hover(function() {
        if(!$('#user-rating').hasClass('rated')) {
            if($(this).hasClass('fa')) {
                $(this).prevAll().addBack().removeClass('fa');
                $(this).prevAll().addBack().addClass('far');
            } else {
                 $(this).prevAll().addBack().removeClass('far');
                 $(this).prevAll().addBack().addClass('fa');
            }
        }
    });

    //Call the create rating view when a star is clicked
    $('#user-rating span').click(function() {
        let rating = $(this).data('rating');
        let productId = $(this).data('product-id');
        $('#user-rating p').hide();
        if(!('#user-rating').hasClass('rated')) {
             $.ajax({
                url: '/products/submit_rating/',
                type: 'POST',
                data: {
                    rating,
                    product_id: productId,
                },
                success: function(data) {
                    $('#customer-ratings-container').replaceWith(data);
                },
                error: function(data) {
                    alert('An error occured');
                }
            });
        }
    });

    //Review submission validation
    //Select the input and textarea elements
    $('.error-message').hide();
    let reviewTitleInput = $('input[name="review-title"]');
    let reviewContentTextarea = $('textarea[name="review-content"]');
    let postButton = $('#post-review-btn');

    //set the textarea selection at the start
    reviewContentTextarea.on('focus', function() {
        this.setSelectionRange(0, 0);
    });


    //Add event listeners for the input and textarea elements
    reviewTitleInput.on('input', function() {
        if($(this).val().length < 5) {
            //Show the error and add invalid class
            $(this).addClass('invalid');
            $(this).next('.error-message').show();
        }  else {
            // hide the error message if the value is valid and remove invalid class
            $(this).next('.error-message').hide();
            $(this).removeClass('invalid');
        }
        // check if both input and textarea are invalid
        if(reviewTitleInput.hasClass('invalid') || reviewContentTextarea.hasClass('invalid')) {
            // disable the post review button
            console.log('disabled class added');
            postButton.addClass('disabled');
        } else {
            // enable the post review button
            postButton.removeClass('disabled');
        }
    });
    reviewContentTextarea.on('input', function() {
        if($(this).val().length < 50) {
            //Show the error and add invalid class
            $(this).addClass('invalid');
            $(this).next('.error-message').show();
        }  else {
            // hide the error message if the value is valid and remove invalid class
            $(this).next('.error-message').hide();
            $(this).removeClass('invalid');
        }
        // check if both input and textarea are invalid
        if(reviewTitleInput.hasClass('invalid') || reviewContentTextarea.hasClass('invalid')) {
            // disable the post review button
            console.log('disabled class added');
            postButton.addClass('disabled');
        } else {
            // enable the post review button
            postButton.removeClass('disabled');
        }
    });

    //Handle review submission
    postButton.click(function(event) {
        event.preventDefault();
        let reviewTitle = reviewTitleInput.val();
        let reviewContent = reviewContentTextarea.val();
        let productId = $(this).data('product-id');
        let csrfToken = $(this).siblings('input[name="csrfmiddlewaretoken"]').val();
        console.log(csrfToken);
        console.log(productId);
        $.ajax({
            url: '/products/post_review/',
            type: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            data: {
                product_id: productId,
                review_title: reviewTitle,
                review_content: reviewContent,
            },
            success: function(data) {
                $('#customer-reviews-container').replaceWith(data);
            },
        })
    });
});