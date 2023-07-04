export function loadImages(quality, callback) {
    let images = $('.product-img');
    let loadedImages = 0;
    images.each(function() {
        let image = $(this);
        let imgSrc = image.data('src-url');
        let productId = image.data('product-id');
        $.post(imgSrc, {quality: quality, product_id: productId}, function(data){
            if(data['status'] == 'success') {
                image.attr('src', data['img_urls'][0]);
            }
            loadedImages++;
            if (loadedImages == images.length && callback) {
                callback();
            }
        });
    });
}

$(function() {
    console.log('loadImages.js loaded');
    loadImages('low', function() {
        loadImages('high');
    });
});
