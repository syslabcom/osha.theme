function displaynl() {
    "use strict";
    jQuery('.fadercontrol').hide();
    jQuery('.older-newsletter').fadeIn('slow');
}

var OSHMAIL = {};

OSHMAIL.loadOshmailContent = function (linkObj) {
    "use strict";
    // We can ignore ?set_language if it is set in the href
    var href = linkObj.href.split("?")[0];
    jQuery("#overlay-spinner").show();
    jQuery.ajax({
        async: false,
        type: 'GET',
        url: href + "?ajax_load=1",
        success: function (data) {
            jQuery("#oshmail-overlay #collage")
                .replaceWith(jQuery(data).find("#collage"));
            jQuery("#overlay-spinner").hide();
        }
    });
};

jQuery(document).ready(function () {
    "use strict";
    if (jQuery("a[rel=oshmail-fancybox]").length > 0) {
        jQuery("a[rel=oshmail-fancybox]")
            .click(function () {
                jQuery(".osha-overlay").show("slow");
                OSHMAIL.loadOshmailContent(this);
                return false;
            });
    }
    jQuery(".osha-overlay-close").click(function () {
        jQuery(".osha-overlay").hide("slow");
    });
});

