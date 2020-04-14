(function($){
    "use strict"; // Start of use strict
    var stickyHeaderTop =0;
    if( $('.header .main-menu').length > 0){
      stickyHeaderTop = $('.header .main-menu').offset().top;
    }

    function is_ie() {
        var ua = window.navigator.userAgent;
        var msie = ua.indexOf("MSIE ");

        if (msie > 0 || !!navigator.userAgent.match(/Trident.*rv\:11\./))  // If Internet Explorer, return version number
        {
           return true;
        }
        else  // If another browser, return 0
        {
           return false;
        }
    }
     /* ---------------------------------------------
     Stick menu
     --------------------------------------------- */
     function kt_stick_menu(){
      if($('#header .main-menu').length >0){
        var h = $(window).scrollTop();
          var width = $(window).width();
          if(width > 991){
              if((h > stickyHeaderTop) ){
                  clone_header_ontop();
                  $('#header-ontop').addClass('on-sticky');
                  $('#header-ontop').find('.header').addClass('ontop');
              }else{
                  $('#header-ontop').removeClass('on-sticky');
                  $('#header-ontop').find('.header').removeClass('ontop');
              }
          }else{
              $('#header-ontop').find('.header').removeClass('ontop');
              $('#header-ontop').removeClass('on-sticky');
          }
      }
     }
    /* ---------------------------------------------
     Owl carousel
     --------------------------------------------- */
    function kt_carousel(){
        $('.owl-carousel').each(function(){
          var config = $(this).data();
          config.navText = ['<i class="fa fa-angle-left"></i>','<i class="fa fa-angle-right"></i>'];
          var animateOut = $(this).data('animateout');
          var animateIn = $(this).data('animatein');
          var smartSpeed = $(this).data('smartspeed');

          if(typeof animateOut != 'undefined' ){
            config.animateOut = animateOut;
          }
          if(typeof animateIn != 'undefined' ){
            config.animateIn = animateIn;
          }

          if( typeof smartSpeed != 'undefined'){
              config.smartSpeed = smartSpeed;
          }else{
            config.smartSpeed = 500;
          }
          var owl = $(this);
          owl.owlCarousel(config);
        });
    }

    /* ---------------------------------------------
     Owl carousel mobile
     --------------------------------------------- */
    function kt_carousel_mobile(){
        var window_size = jQuery('body').innerWidth();
        window_size += kt_get_scrollbar_width();
        if( window_size < 768 ){
          $('.owl-carousel-mobile').each(function(){
            var config = $(this).data();
             config.navText = ['<i class="fa fa-angle-left"></i>','<i class="fa fa-angle-right"></i>'];
             var animateOut = $(this).data('animateout');
             var animateIn = $(this).data('animatein');
             var smartSpeed = $(this).data('smartspeed');

             if(typeof animateOut != 'undefined' ){
               config.animateOut = animateOut;
             }
             if(typeof animateIn != 'undefined' ){
               config.animateIn = animateIn;
             }

             if( typeof smartSpeed != 'undefined'){
                 config.smartSpeed = smartSpeed;
             }else{
               config.smartSpeed = 500;
             }
             var owl = $(this);
             owl.owlCarousel(config);
          });
        }
        
    }
    /* ---------------------------------------------
     MENU REPONSIIVE
     --------------------------------------------- */
     function kt_menu_reposive(){
          var kt_is_mobile = (Modernizr.touch) ? true : false;
          if(kt_is_mobile === true){
            $(document).on('click', '.kt-nav .menu-item-has-children > a', function(e){
              var licurrent = $(this).closest('li');
              var liItem = $('.kt-nav .menu-item-has-children');
              if ( !licurrent.hasClass('show-submenu') ) {
                liItem.removeClass('show-submenu');
                licurrent.parents().each(function (){
                    if($(this).hasClass('menu-item-has-children')){
                     $(this).addClass('show-submenu');   
                    }
                      if($(this).hasClass('main-menu')){
                          return false;
                      }
                })
                licurrent.addClass('show-submenu');
                // Close all child submenu if parent submenu is closed
                if ( !licurrent.hasClass('show-submenu') ) {
                  licurrent.find('li').removeClass('show-submenu');
                  }
                  return false;
                  e.preventDefault();
              }else{
                var href = $this.attr('href');
                  if ( $.trim( href ) == '' || $.trim( href ) == '#' ) {
                      licurrent.toggleClass('show-submenu');
                  }
                  else{
                      window.location = href;
                  } 
              }
              // Close all child submenu if parent submenu is closed
                  if ( !licurrent.hasClass('show-submenu') ) {
                      //licurrent.find('li').removeClass('show-submenu');
                  }
                  e.stopPropagation();
          });
          $(document).on('click', function(e){
              var target = $( e.target );
              if ( !target.closest('.show-submenu').length || !target.closest('.kt-nav').length ) {
                  $('.show-submenu').removeClass('show-submenu');
              }
          }); 
          // On Desktop
          }else{
              $(document).on('mousemove','.kt-nav .menu-item-has-children',function(){
                  $(this).addClass('show-submenu');
              })
              $(document).on('mouseout','.kt-nav .menu-item-has-children',function(){
                  $(this).removeClass('show-submenu');
              })
          }
     }
    /* ---------------------------------------------
     Resize mega menu
     --------------------------------------------- */
     function kt_resizeMegamenu(){
        var window_size = jQuery('body').innerWidth();
        window_size += kt_get_scrollbar_width();
        if( window_size > 767 ){
          if( $('.main-menu-wapper').length >0){
            var container = $('.main-menu-wapper');
            if( container!= 'undefined'){
              var container_width = 0;
              container_width = container.innerWidth();
              var container_offset = container.offset();
              setTimeout(function(){
                  $('.main-menu .item-megamenu').each(function(index,element){
                      $(element).children('.megamenu').css({'max-width':container_width+'px'});
                      var sub_menu_width = $(element).children('.megamenu').outerWidth();
                      var item_width = $(element).outerWidth();
                      $(element).children('.megamenu').css({'left':'-'+(sub_menu_width/2 - item_width/2)+'px'});
                      var container_left = container_offset.left;
                      var container_right = (container_left + container_width);
                      var item_left = $(element).offset().left;
                      var overflow_left = (sub_menu_width/2 > (item_left - container_left));
                      var overflow_right = ((sub_menu_width/2 + item_left) > container_right);
                      if( overflow_left ){
                        var left = (item_left - container_left);
                        $(element).children('.megamenu').css({'left':-left+'px'});
                      }
                      if( overflow_right && !overflow_left ){
                        var left = (item_left - container_left);
                        left = left - ( container_width - sub_menu_width );
                        $(element).children('.megamenu').css({'left':-left+'px'});
                      }
                  })
              },100);
            }
          }
        }
     }
     
     function kt_get_scrollbar_width() {
        var $inner = jQuery('<div style="width: 100%; height:200px;">test</div>'),
            $outer = jQuery('<div style="width:200px;height:150px; position: absolute; top: 0; left: 0; visibility: hidden; overflow:hidden;"></div>').append($inner),
            inner = $inner[0],
            outer = $outer[0];
        jQuery('body').append(outer);
        var width1 = inner.offsetWidth;
        $outer.css('overflow', 'scroll');
        var width2 = outer.clientWidth;
        $outer.remove();
        return (width1 - width2);
    }

    /**==============================
    Auto width Vertical menu
    ===============================**/
    function kt_auto_width_vertical_menu(){
        var full_width = parseInt($('.container').innerWidth());

        //full_width = $( document ).width();
        var menu_width = parseInt($('.verticalmenu-content').actual('width'));
        var w = (full_width - menu_width)-32;
        $('.verticalmenu-content').find('.megamenu').each(function(){

            $(this).css('max-width',w+'px');
        });
    }

    /* ---------------------------------------------
     Height Full
     --------------------------------------------- */

    function kt_height_full(){
        var height = $(window).outerHeight();
        $(".full-height").css("height",height);  
    }
    function kt_width_full(){
        var width = $(window).outerWidth();
        $(".full-width").css("width",width);
    }

    function kt_home_slide(){
        var window_size = jQuery('body').innerWidth();
        window_size += kt_get_scrollbar_width();

        $('.kt_home_slide').each(function(){

          // Seting
          $(this).find('.item-slide').each(function(){
            var background = $(this).data('background');
            var height = $(this).data('height');
            var reponsive = $(this).data('reponsive');
            if( typeof(background) != 'undefined'){
              $(this).css({
               'background-image':'url('+background+')'
              });
            }
            if( typeof(height) != 'undefined'){
              height = height+'px';
              $(this).css({
               'height':height
              });
            }

            if (typeof(reponsive) != 'undefined'){
              //console.log(window_size);
               for (var k in reponsive){
                    if (typeof reponsive[k] !== 'function') {
                        if( window_size <= k ){
                          if( reponsive[k] > 0 ){
                            $(this).css({
                              'min-height':reponsive[k]+'px',
                              'height':reponsive[k]+'px'
                            });
                            break;
                          }
                        }
                    }
                }
             }
          })

          /* OWL */
          var owl = $(this);
          var config = $(this).data();
          config.navText = ['<i class="fa fa-angle-left"></i>','<i class="fa fa-angle-right"></i>'];
          var animateOut = $(this).data('animateout');
          var animateIn = $(this).data('animatein');
          var smartSpeed = $(this).data('smartspeed');
          
          
          if(typeof (animateOut) != 'undefined' ){
            config.animateOut = animateOut;
          }
          if(typeof (animateIn) != 'undefined' ){
            config.animateIn = animateIn;
          }

          if( typeof smartSpeed != 'undefined'){
              config.smartSpeed = smartSpeed;
          }else{
            config.smartSpeed = 800;
          }



          owl.owlCarousel(config);
          owl.trigger('next.owl.carousel');
          owl.on('changed.owl.carousel', function(property) {
            var current = property.item.index;
            $(property.target).find(".owl-item").eq(current).find(".caption").each(function(i){
                var t = $(this);
                var style = $(this).attr("style");
                style     = ( style == undefined ) ? '' : style;
                var delay  = i+1 * 1000;
                var animate = t.data('animate');
                t.attr("style", style +
                          ";-webkit-animation-delay:" + delay + "ms;"
                        + "-moz-animation-delay:" + delay + "ms;"
                        + "-o-animation-delay:" + delay + "ms;"
                        + "animation-delay:" + delay + "ms;"
                ).addClass('animated '+ animate).one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
                    $(this).removeClass('animated '+animate);
                });
                
            })
          })
        });
    }

    /* ---------------------------------------------
     OWL TAB EFFECT
     --------------------------------------------- */
    function kt_tab_fadeeffect(){
      // effect first tab
      if(! is_ie() ){
          // var sleep = 0;
          // $('.kt-tab-fadeeffect .nav-tab>li.active a[data-toggle="tab"]').each(function(){
          //   var tabElement = $(this);
          //   setTimeout(function() {
          //       tabElement.trigger('click');
          //   }, sleep);
          //   sleep += 10000
          // })
          // effect click
          $(document).on('click','.kt-tab-fadeeffect a[data-toggle="tab"]',function(){
            var item = '.product-item';

            var tab_id = $(this).attr('href');
            var tab_animated = $(this).data('animated');
            tab_animated = ( tab_animated == undefined ) ? 'fadeInUp' : tab_animated;

            if( $(tab_id).find('.owl-carousel').length > 0 ){
              item = '.owl-item.active';
            }
            $(tab_id).find(item).each(function(i){
                var t = $(this);
                var style = $(this).attr("style");
                style     = ( style == undefined ) ? '' : style;
                var delay  = i * 200;
                t.attr("style", style +
                          ";-webkit-animation-delay:" + delay + "ms;"
                        + "-moz-animation-delay:" + delay + "ms;"
                        + "-o-animation-delay:" + delay + "ms;"
                        + "animation-delay:" + delay + "ms;"
                ).addClass(tab_animated+' animated').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
                    t.removeClass(tab_animated+' animated');
                    t.attr("style", style);
                });
            })
          })
      }
    }
    /* ---------------------------------------------
     Parallax
     --------------------------------------------- */
     function kt_parallax(){
        var window_size = jQuery('body').innerWidth();
        window_size += kt_get_scrollbar_width();
        if( window_size > 767){
            //$('.bg-parallax').parallax('50%', 0.3);
        }
     }
     /* ---------------------------------------------
     COUNTDOWN
     --------------------------------------------- */
     function kt_countdown(){
        if($('.kt-countdown').length >0){
          var labels = ['Years', 'Months', 'Weeks', 'Days', 'Hrs', 'Mins', 'Secs'];
          var layout = '<span class="box-count day"><span class="number">{dnn}</span> <span class="text">Days</span></span><span class="dot">:</span><span class="box-count hrs"><span class="number">{hnn}</span> <span class="text">Hrs</span></span><span class="dot">:</span><span class="box-count min"><span class="number">{mnn}</span> <span class="text">Mins</span></span><span class="dot">:</span><span class="box-count secs"><span class="number">{snn}</span> <span class="text">Secs</span></span>';
          $('.kt-countdown').each(function() {
              var austDay = new Date($(this).data('y'),$(this).data('m') - 1,$(this).data('d'),$(this).data('h'),$(this).data('i'),$(this).data('s'));
              $(this).countdown({
                  until: austDay,
                  labels: labels, 
                  layout: layout
              });
          });
        }
     }

     function kt_banner(){
      //Shortcode Banner
      $('.kt-banner').each(function(){
        var window_size = jQuery('body').innerWidth();
        window_size += kt_get_scrollbar_width();
         var minHeight = $(this).data('height'),
         bgimg = $(this).data('background'),
         bgcolor = $(this).data('bgcolor'),
         positiontop = $(this).data('positiontop'),
         positionleft = $(this).data('positionleft'),
         positionright = $(this).data('positionright'),
         positionbottom = $(this).data('positionbottom'),
         verticalmiddle = $(this).data('verticalmiddle');
         var bgcontainer =  $(this).find('.bg-image');
         var content = $(this).find('.content');
         var reponsive = $(this).data('reponsive');
         bgcontainer.css({
            'min-height':minHeight+'px',
            'height':minHeight+'px'
         });

       if( typeof (bgimg)!= 'undefined' && bgimg !=""){
            bgcontainer.css({
             'background-image':'url('+bgimg+')'
            });
         }

         if( typeof (bgcolor) != 'undefined' && bgcolor !=""){
            bgcontainer.css({
             'background-color':bgcolor
            });
         }
         
         if( typeof (positiontop) != 'undefined' && positiontop !=""){
            content.css({
             'top':positiontop
            });
         }
         if( typeof (positionleft) != 'undefined' && positionleft !=""){
            content.css({
             'left':positionleft
            });
         }
         if( typeof (positionright) != 'undefined' && positionright !=""){
            content.css({
             'right':positionright
            });
         }
         if( typeof (positionbottom) != 'undefined' && positionbottom !=""){
            content.css({
             'bottom':positionbottom
            });
         }

         if( typeof (verticalmiddle) != 'undefined' && verticalmiddle != "" && verticalmiddle =="middle" ){
            content.css({
             '-webkit-transform':'translateY(-50%)',
             '-ms-transform': 'translateY(-50%)',
             '-o-transform': 'translateY(-50%)',
             'transform': 'translateY(-50%)',
             'top':'50%'
            });
         }

         if (typeof(reponsive) != 'undefined'){
          //console.log(window_size);
           for (var k in reponsive){
                if (typeof reponsive[k] !== 'function') {
                    if( window_size <= k ){
                      if( reponsive[k] > 0 ){
                        bgcontainer.css({
                          'min-height':reponsive[k]+'px',
                          'height':reponsive[k]+'px'
                        });
                        break;
                      }
                    }
                }
            }
         }
      });
     }

     function kt_hiden_orther_veticalmenu(){

         if( $( '.box-vertical-megamenus' ).length > 0 ){
          $( '.box-vertical-megamenus' ).each(function(){
            var all_item = 0;
            var limit_item = $(this).data('items')-1;

            var all_item = $(this).find('.verticalmenu-list>li').length;
            if( all_item > (limit_item + 1) ){
               $(this).addClass('show-button-all');
            }else{
               $(this).addClass('hiden-button-all');
            }

            $(this).find('.verticalmenu-list>li').each(function(i){
                all_item = all_item + 1;
                if(i > limit_item){
                  $(this).addClass('orther-link');
                }
            })
          })
        }
     }
     function clone_main_menu(){
        if( $('.clone-main-menu').length > 0 && $('#box-mobile-menu').length > 0){
          $( ".clone-main-menu" ).clone().appendTo( "#box-mobile-menu .box-inner" );
        }
    }

    function clone_header_ontop(){
        if( $('#header').length > 0 && $('#header-ontop').length >0 && $('#header-ontop').hasClass('is-sticky')){
          if( $('#header-ontop').find('.header').length <= 0 ){
            var content = $( "#header" ).clone();
            content.removeAttr('id');
            content.appendTo( "#header-ontop" );
          }
        }
    }
    /* ---------------------------------------------
     Init popup
     --------------------------------------------- */
    function init_popup(){
        if($(window).width() + kt_get_scrollbar_width() >= 768){
            if($('body').hasClass('home')){
                //Open directly via API
                $.magnificPopup.open({
                  items: {
                    src: '<div class="white-popup"><div class="kt-popup-newsletter"><div class="popup-title"><h3>Luckyshop</h3><p class="notice">enter your email and get  <span class="text-primary">25% off</span> YOUR first purchase!</p></div><form class="form-subscribe"><input class="input" placeholder="Your email here" type="text" /><button class="button">NO THANKS!</button><button class="button primary">Enter</button></form><div class="checkbox"><label><input type="checkbox" value="">Dont show this popup again!</label></div></div></div>',  //can be a HTML string, jQuery object, or CSS selector
                    type: 'inline'
                  }
                });
            }
        }
    }
    function fireOnResizeEvent() {
        var width, height;
        if (navigator.appName.indexOf("Microsoft") != -1) {
            width  = document.body.offsetWidth;
            height = document.body.offsetHeight;
        } else {
            width  = window.outerWidth;
            height = window.outerHeight;
        }
        console.log('xx');
        window.resizeTo(width - 1, height);
        window.resizeTo(width + 1, height);
    }
    /* ---------------------------------------------
     Scripts initialization
     --------------------------------------------- */
    $(window).load(function() {
      clone_main_menu();
      // Resize Megamenu
      kt_menu_reposive();
      kt_resizeMegamenu();
      kt_height_full();
      kt_width_full();
      kt_parallax();
      kt_carousel_mobile();
      kt_hiden_orther_veticalmenu();
      kt_auto_width_vertical_menu();
      kt_stick_menu();
      init_popup();
      // Slide home 1
        if( $('.slide-home1 .slide-container').length > 0 ){
          $('.slide-home1 .slide-container').bxSlider({
            pagerCustom: '.slide-home1 .thumbs',
            controls:false,
            auto:true
          });
        }
    });
    /* ---------------------------------------------
     Scripts resize
     --------------------------------------------- */
    $(window).on("resize", function() {
      kt_resizeMegamenu();
      kt_height_full();
      kt_width_full();
      kt_carousel_mobile();
      kt_auto_width_vertical_menu();
      kt_stick_menu();
      kt_home_slide();
      kt_banner();
    });
    /* ---------------------------------------------
     Scripts scroll
     --------------------------------------------- */
    $(window).scroll(function(){
      kt_stick_menu();
      kt_resizeMegamenu();
      // Show hide scrolltop button
      if( $(window).scrollTop() == 0 ) {
          $('.scroll_top').stop(false,true).fadeOut(600);
      }else{
          $('.scroll_top').stop(false,true).fadeIn(600);
      }
    });
    /* ---------------------------------------------
     Scripts ready
     --------------------------------------------- */
    $(document).ready(function() {
        kt_carousel();
        //SELECT CHOSEN
        $("select").chosen();
        kt_resizeMegamenu();
        kt_home_slide();
        kt_height_full();
        kt_width_full();
        kt_tab_fadeeffect();
        kt_countdown();
        kt_banner();
        kt_carousel_mobile();
        kt_stick_menu();
        // CATEGORY FILTER 
        $('.slider-range-price').each(function(){
            var min             = $(this).data('min');
            var max             = $(this).data('max');
            var unit            = $(this).data('unit');
            var value_min       = $(this).data('value-min');
            var value_max       = $(this).data('value-max');
            var label_reasult   = $(this).data('label-reasult');
            var t               = $(this);
            $( this ).slider({
              range: true,
              min: min,
              max: max,
              values: [ value_min, value_max ],
              slide: function( event, ui ) {
                var result = label_reasult +" <span>"+ unit + ui.values[ 0 ] +' </span> - <span> '+ unit +ui.values[ 1 ]+'</span>';
                t.closest('.price_slider_wrapper').find('.amount-range-price').html(result);
              }
            });
        });

        // Scroll top 
        $(document).on('click','.scroll_top',function(){
          $('body,html').animate({scrollTop:0},400);
          return false;
        });
        // Sections backgrounds
        var itembackground = $(".item-background");
        itembackground.each(function(index){
          if ($(this).attr("data-background")){
              $(this).css("background-image", "url(" + $(this).data("background") + ")");
          }
        });
       // Fancybox
       if( $('.kt-images').length > 0 ){
          $('.kt-images').magnificPopup({
            delegate: 'a', // child items selector, by clicking on it popup will open
            type: 'image',
            gallery:{enabled:true},
            zoom: {
                enabled: true, // By default it's false, so don't forget to enable it

                duration: 300, // duration of the effect, in milliseconds
                easing: 'ease-in-out', // CSS transition easing function

                // The "opener" function should return the element from which popup will be zoomed in
                // and to which popup will be scaled down
                // By defailt it looks for an image tag:
                opener: function(openerElement) {
                  // openerElement is the element on which popup was initialized, in this case its <a> tag
                  // you don't need to add "opener" option if this code matches your needs, it's defailt one.
                  return openerElement.is('img') ? openerElement : openerElement.find('img');
                }
              }

            // other options
          });
       } 

       // daily-deal zoom 

       $(document).on('click','.block-daily-deal .thumbs a',function(){
         var imagemedium = $(this).data('imagemedium');
         var imagefull = $(this).data('imagefull');
         $(this).closest('.thumbs').find('a').each(function(){
            $(this).removeClass('selected');
         })
         $(this).addClass('selected');

         $(this).closest('.block-daily-deal').find('.product-detail .mainImage').attr('href',imagefull).find('img').attr('src',imagemedium);
         return false;
       })

       /** ALL CAT **/
        $(document).on('click','.box-vertical-megamenus .viewall.closed',function(){
            $(this).closest('.box-vertical-megamenus').find('li.orther-link').each(function(){
                $(this).slideDown();
            });
            var closetext = $(this).data('closetext');
            closetext = '<span class="text">'+closetext+'</span>';
            $(this).addClass('open').removeClass('closed').html( closetext );
            return false;
        });

        /* Close category */
        $(document).on('click','.box-vertical-megamenus .viewall.open',function(){
            $(this).closest('.box-vertical-megamenus').find('li.orther-link').each(function(){
                $(this).slideUp();
            });
            var opentext = $(this).data('opentext');
            opentext = '<span class="text">'+opentext+'</span>';
            $(this).addClass('closed').removeClass('open').html(opentext);
            return false;
        });

        var wow = new WOW(
          {
            boxClass:     'wow',      // default
            animateClass: 'animated', // default
            offset:       0,          // default
            mobile:       false,       // default
            live:         true        // default
          }
        )
        wow.init();

        

        // BOX MOBILE MENU
        $(document).on('click','.mobile-navigation',function(){
          $('#box-mobile-menu').addClass('open');
        });
        // Close box menu
        $(document).on('click','#box-mobile-menu .close-menu',function(){
            $('#box-mobile-menu').removeClass('open');
        });
        //  Box mobile menu
        if($('#box-mobile-menu').length >0 ){
            $("#box-mobile-menu").mCustomScrollbar();
        }

        $(document).on('click','.topbar-bar',function(){
            $(this).closest('.header').find('.top-bar').toggleClass('open');
        })

        // Vertical menu

        $(document).on('click','.box-vertical-megamenus .title',function(){
          $(this).closest('.box-vertical-megamenus').find('.verticalmenu-content').slideToggle();
        })

        // Quickview

        $(document).on('click','.button.quick-view',function(){
           var data = {}
            $.post('quick_view.html', data, function(response){
                $.magnificPopup.open({
                  items: {
                    src: '<div class="kt-quickview-popup">'+response+'</div>',  //can be a HTML string, jQuery object, or CSS selector
                    type: 'inline'
                  }
                });
               $(window).trigger('resize');
                
            })
            return false;
        })

        // Instantiate EasyZoom instances
        if( $('.kt-easyzoom').length > 0 ){
            var $easyzoom = $('.kt-easyzoom').easyZoom();

          // Setup thumbnails example
          var api1 = $easyzoom.filter('.easyzoom--with-thumbnails').data('easyZoom');

          $('.kt-zoom-thumbnails').on('click', 'a', function(e) {
            var $this = $(this);
            e.preventDefault();
            // Use EasyZoom's `swap` method
            api1.swap($this.data('standard'), $this.attr('href'));
          });
        }

        /* Send conttact*/
        $(document).on('click','#btn-send-contact',function(){
                var email   = $('#email').val(),
                name = $('#name').val(),
                content = $('#content').val(),
                subject = $('#subject').val();
            var data = {
                email:email,
                content:content,
                name:name,
                subject:subject
            }

            $(this).html('Loading...');
            var t = $(this);
            $.post('ajax_contact.php',data,function(result){
                if(result.trim()=="done"){
                    $('#email').val('');
                    $('#content').val('');
                    $('#name').val('');
                    $('#subject').val('');
                    $('#message-box-conact').html('<div class="alert alert-info">Your message was sent successfully. Thanks</div>');
                }else{
                    $('#message-box-conact').html(result);
                }
                t.html('SEND MESSAGE');
            })
        })
        
        // SETINGS KT BOX
        if( $('.kt-box').length > 0 ){
            $('.kt-box').each(function(){
              var bg = $(this).data('bg'),
              color = $(this).data('color'),
              titlecolor = $(this).data('titlecolor');

              if( typeof(bg) != 'undefined' && bg != "" ){
                $(this).find('.block-head').css({'background-color':bg});
              }
              if( typeof(color) != 'undefined' && color != "" ){
                $(this).find('.block-head').css({'color':color});
              }
              if( typeof(titlecolor) != 'undefined' && titlecolor != "" ){
                $(this).find('.block-head .title').css({'color':titlecolor});
              }
            })
        }

        // HOVER DIV
        $('.banner-category').each( function() {
          $(this).hoverdir(); 
        });

        // Topbar search

        $(document).on('click','.topbar-search .icon',function(){
            $(this).closest('form').find('.inner').toggle();
        })

        //floor-elevator 
        $('.floor-elevator').each(function(i){
          $(this).attr('id','kt-elevator-'+i);
          $(this).find('.btn-elevator.up').attr('href','#kt-elevator-'+(i-1))
          $(this).find('.btn-elevator.down').attr('href','#kt-elevator-'+(i+1))
        })
        /* elevator click*/ 
        $(document).on('click','a.btn-elevator',function(e){
            var header_ontop_h = $('#header-ontop').find('.header').height(); 
            e.preventDefault();
            var target = this.hash;
            if($(document).find(target).length <=0){
                return false;
            }
            var $target = $(target);
            $('html, body').stop().animate({
                'scrollTop': $target.offset().top-(header_ontop_h+30)
            }, 500);
            return false;
        })


        // Custom post nav owl
        $('.owl-custom-nav-postion').each(function(){
            var margin = $(this).data('navigation_margin');
            var top = '-'+margin+'px';
            if( typeof (margin) != 'undefined' && margin >=0 ){
                $(this).find('.owl-nav, .owl-nav').css({'top':top});
            }
        })

        // close header banner
        $(document).on('click','.banner-header .close-banner',function(){
          $(this).closest('.banner-header').slideUp();
          return false;
        })

        // Tab categoy sub category
        $(document).on('click','.kt-category-tabs .tab-head .title',function(){
          $(this).closest('.kt-category-tabs').find('.sub-category').toggle();
          return false;
        })
    });

})(jQuery); // End of use strict