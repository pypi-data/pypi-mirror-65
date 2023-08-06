jQuery(document).ready(function($){

    // jQuery sticky Menu

	$(".mainmenu-area").sticky({topSpacing:0});


    $('.product-carousel').owlCarousel({
        loop:true,
        nav:true,
        margin:20,
        responsiveClass:true,
        responsive:{
            0:{
                items:1,
            },
            600:{
                items:3,
            },
            1000:{
                items:5,
            }
        }
    });

    $('.related-products-carousel').owlCarousel({
        loop:true,
        nav:true,
        margin:20,
        responsiveClass:true,
        responsive:{
            0:{
                items:1,
            },
            600:{
                items:2,
            },
            1000:{
                items:2,
            },
            1200:{
                items:3,
            }
        }
    });

    $('.brand-list').owlCarousel({
        loop:true,
        nav:true,
        margin:20,
        responsiveClass:true,
        responsive:{
            0:{
                items:1,
            },
            600:{
                items:3,
            },
            1000:{
                items:4,
            }
        }
    });


    // Bootstrap Mobile Menu fix
    $(".navbar-nav li a").click(function(){
        $(".navbar-collapse").removeClass('in');
    });

    // jQuery Scroll effect
    $('.navbar-nav li a, .scroll-to-up').bind('click', function(event) {
        var $anchor = $(this);
        var headerH = $('.header-area').outerHeight();
        $('html, body').stop().animate({
            scrollTop : $($anchor.attr('href')).offset().top - headerH + "px"
        }, 1200, 'easeInOutExpo');

        event.preventDefault();
    });

    // Bootstrap ScrollPSY
    $('body').scrollspy({
        target: '.navbar-collapse',
        offset: 95
    });

    // Refreshing page on click "add to cart"
    $('#add_to_cart, .add-to-cart-link').on('click', function(){
        var productId = $(this).parent().find('input[name="product_id"]').val();
        $.post('/cart/add', {product_id: productId}, function(data){
            var data = JSON.parse(data);
            var totalCost = data.total_cost;
            var totalQuantity = data.total_quantity;
            $('.cart-amunt').html(totalCost + '$');
            $('.product-count').html(totalQuantity);
            $('#add_to_cart').html('in cart');

            // $('.add-to-cart-link').html('in cart');
        });
        return false;
    });

});




var ww = document.body.clientWidth;

$(document).ready(function() {
    $(".nav li a").each(function() {
        if ($(this).next().length > 0) {
            $(this).addClass("parent");
        };
    })

    $(".toggleMenu").click(function(e) {
        e.preventDefault();
        $(this).toggleClass("active");
        $(".nav").toggle();
    });
    adjustMenu();
})

$(window).bind('resize orientationchange', function() {
    ww = document.body.clientWidth;
    adjustMenu();
});

var adjustMenu = function() {
    if (ww < 768) {
        $(".toggleMenu").css("display", "inline-block");
        if (!$(".toggleMenu").hasClass("active")) {
            $(".nav").hide();
        } else {
            $(".nav").show();
        }
        $(".nav li").unbind('mouseenter mouseleave');
        $(".nav li a.parent").unbind('click').bind('click', function(e) {
            // must be attached to anchor element to prevent bubbling
            e.preventDefault();
            $(this).parent("li").toggleClass("hover");
        });
    }
    else if (ww >= 768) {
        $(".toggleMenu").css("display", "none");
        $(".nav").show();
        $(".nav li").removeClass("hover");
        $(".nav li a").unbind('click');
        $(".nav li").unbind('mouseenter mouseleave').bind('mouseenter mouseleave', function() {
            // must be attached to li so that mouseleave is not triggered when hover over submenu
            $(this).toggleClass('hover');
        });
    }

};

