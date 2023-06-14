$(function() {
    // Select all images with a data-src attribute
    console.log("loadImages loaded");
    let $images = $('img[data-src]');
    let index = 0;
    let imagesPerRow = 4;

    function isImageCached(url, callback) {
        let xhr = new XMLHttpRequest();
        xhr.open('HEAD', url, true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                let cacheControl = xhr.getResponseHeader('Cache-Control');
                let maxAgeMatch = cacheControl && cacheControl.match(/max-age=(\d+)/);
                let maxAge = maxAgeMatch && parseInt(maxAgeMatch[1]);
                let lastModified = xhr.getResponseHeader('Last-Modified');
                let age = lastModified && (Date.now() - new Date(lastModified).getTime()) / 1000;
                callback(maxAge && age && age < maxAge);
            }
        };
        xhr.send();
    }


    function loadImage() {
        if (index >= $images.length) {
            // All images have been loaded
            return;
        }

        for (let i = 0; i < imagesPerRow && index < $images.length; i++) {
            let $img = $($images[index]);
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

            isImageCached(highQualitySource, function(isCached) {
                if (isCached) {
                    // Use the cached version of the image
                    $img.attr('src', highQualitySource);
                } else {
                    getLQImage();
                }
            });

            index++;
        }

        loadImage();
    }


    loadImage();
});
