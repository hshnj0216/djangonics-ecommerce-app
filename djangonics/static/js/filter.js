$(function() {
    let url = $('.filter-form').data('filter-url');

    // function to update the product list via AJAX
    function updateProductList() {
        let selectedCategories = [];
        let minPrice = parseInt($('#min_price').val()) || 0;
        let maxPrice = parseInt($('#max_price').val()) || 9999;
        let currentPage = $('#content-container').data('page');
        let rating = $('.star-rating-filter.selected-rating').data('rating');

        // iterate over the checkboxes to get the selected categories
        $('.filter-form :checkbox:checked').each(function() {
            selectedCategories.push($(this).val());
        });

        // make an AJAX request with the selected categories, price range, and product IDs
        $.ajax({
            url: url,
            data: {
                categories: selectedCategories.join(','),
                min_price: minPrice,
                max_price: maxPrice,
                rating: rating,
                current_page: currentPage,
            },
            success: function(data) {
                $('#product-list-partial').html(data);
                 $('img[data-src]').each(function() {
                    let $img = $(this);
                    let highQualitySource = $img.data('src-high');
                    let hqRetries = 3;

                    function getHQImage() {
                        $.get(highQualitySource, function(data) {
                            if (data.status == 'success') {
                                $img.attr('src', data.img_urls[0]);
                            } else if (data.status == 'failed' && hqRetries > 0) {
                                console.log("hq retry");
                                hqRetries--;
                                getHQImage();
                            }
                        });
                    }

                    getHQImage();
                });
            }
        });
    }

    // attach a change event listener to the checkboxes of the filter form
    $('.filter-form :checkbox').change(function() {
        updateProductList();
    });

    // attach a submit event listener to the filter form to prevent default submit behavior
    $('.filter-form').submit(function(event) {
        event.preventDefault();
        updateProductList();
    });

    //attach event listener to the star rating div
    $('.star-rating-filter').on('click', function() {
        if($(this).hasClass('selected-rating')) {
            $(this).removeClass('selected-rating');
        } else {
            $('.star-rating-filter').each(function() {
                $(this).removeClass('selected-rating')
            });
            $(this).addClass('selected-rating');
        }
        updateProductList();
    });
});
