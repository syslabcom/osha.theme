function displaynl () {
    jQuery('.fadercontrol').hide();
    jQuery('.older-newsletter').fadeIn('slow');
}

var OSHMAIL = {}

OSHMAIL.loadOshmailContent = function () {
    jQuery.fancybox.showActivity();
    jQuery.ajax({
        async: false,
        type: 'GET',
        url: this.href,
        success: function(data) {
            jQuery("#oshmail-overlay #collage")
                .replaceWith(jQuery(data)
                             .find("#collage"));
        }
    });
};

jQuery(document).ready(function() {
    if (jQuery("a[rel=oshmail-fancybox]").length>0) {
        jQuery("a[rel=oshmail-fancybox]").fancybox({
            'transitionIn' : 'elastic',
            'transitionOut' : 'elastic',
            'titlePosition' : 'over',
            'overlayOpacity' : 0.7,
            'overlayColor' : '#000',
            'onStart' : OSHMAIL.loadOshmailContent,
            'content' : jQuery('#oshmail-overlay'),
        });
    }
})
