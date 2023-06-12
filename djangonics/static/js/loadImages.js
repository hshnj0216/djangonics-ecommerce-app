$(function() {
    // Select all images with a data-src attribute
    console.log("loadImages loaded");
    $('img[data-src]').each(function() {
        let $img = $(this);
        let lowQualitySource = $img.data('src');
        let highQualitySource = $img.data('src-high');
        let lqRetries = 3;
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

        function getLQImage() {
            $.get(lowQualitySource, function(data) {
                if (data.status == 'success') {
                    // Replace the placeholder image with the actual product image
                    $img.attr('src', data.img_urls[0]);
                    getHQImage();
                } else if (data.status == 'failed' && lqRetries > 0) {
                    console.log("lq retry");
                    lqRetries--;
                    getLQImage();
                }
            });
        }

        getLQImage();
    });
});

