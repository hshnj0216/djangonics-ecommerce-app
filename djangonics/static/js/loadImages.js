$(function() {
    // Select all images with a data-src attribute
    console.log("loadImages loaded");
    $('img[data-src]').each(function() {
        let $img = $(this);
        let src = $img.attr('data-src');
        // Use AJAX to asynchronously call the get_images view for the product
        $.get(src, function(data) {
            // Replace the placeholder image with the actual product image
            console.log(data);
            $img.attr('src', data.img_urls[0]);
        });
    });
});
