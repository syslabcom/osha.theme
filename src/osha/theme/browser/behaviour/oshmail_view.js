function displaynl () {
    jQuery('.fadercontrol').hide();
    jQuery('.older-newsletter').fadeIn('slow');
}

function loadOshmailContent() {
    jQuery.ajax({
        async: false,
        type: 'GET',
        url: this.href,
        success: function(data) {
            jQuery("#oshmail-overlay *")
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
            'onStart' : loadOshmailContent,
            'content' : jQuery('#oshmail-overlay'),
        });
    }
})
