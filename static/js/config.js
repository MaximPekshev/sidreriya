(function($) {
    $(function() {
      if (!$.cookie('smartCookies')) {

        function getWindow(){
          $('.offer').arcticmodal({
            closeOnOverlayClick: false,
            closeOnEsc: false
          });
        };

        setTimeout (getWindow, 500);
      }

      $.cookie('smartCookies', true, {
        expires: 180, 
        path: '/'
      });

    })
  })(jQuery)