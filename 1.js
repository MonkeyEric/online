//使用了imagesLoaded插件来判断图片是否加载完毕

var $grid = $('ul#grid');

$grid.imagesLoaded().done(function(instance) {
// 加载完成
    $grid.masonry({
        // fitWidth: true,
        // initLayout: false,
        itemSelector: '.item',
        columnWidth: '.item',
        percentPosition: true,
    });

})

isImgLoad(function () {
    $grid.masonry("layout");

});

// 判断图片加载的函数

var t_img;

var isLoad = true;

function isImgLoad(callback) {
    $('.img').each(function () {
        if (this.height === 0) {
            isLoad = false;
            return false;
        }
    });
    if (isLoad) {
        clearTimeout(t_img);
        callback();
    } else {
        isLoad = true;
        t_img = setTimeout(function () {
            isImgLoad(callback);
            }, 500);
    }
}
