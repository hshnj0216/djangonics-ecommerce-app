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
        console.log('clicked');
        $('#user-rating span').off('mouseenter mouseleave click');
        $('#user-rating p').hide();
        $.ajax({
            url: '/products/submit_rating/',
            type: 'POST',
            data: {
                rating,
                product_id: productId,
            },
            success: function(data) {

            },
            error: function(data) {
                alert('An error occured');
            }
        });
    });

    //Review submission validation
    //Select the input and textarea elements
    $('.error-message').hide();
    let reviewTitleInput = $('input[name="review-title"]');
    let reviewContentTextarea = $('textarea[name="review-content"]');
    let postButton = $('#post-review-btn');

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

});