export function loadImages() {
    let images = $('.product-img');
    images.each(function() {
        let image = $(this);
        let imgSrc = image.data('src-high');
        let productId = image.data('product-id');
        $.post(imgSrc, {product_id: productId}, function(data){
            if(data['status'] == 'success') {
                image.attr('src', data['img_urls'][0]);
            } else {

            }
        });
    });
}

$(function() {
    console.log('loadImages.js loaded');
    loadImages();
});
