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

    /* IE8 crashes if replaceWith is used, and appending directly to
       .osha-overlay.full causes the content to be display behind the
       overlay (in IE8) even though the DOM looks correct
    */
    jQuery(".osha-overlay.full").find("#overlay-content").remove();

    jQuery(".osha-overlay.full").show();
    jQuery("#overlay-spinner").show();
    jQuery.ajax({
        async: true,
        type: 'GET',
        url: href + "?ajax_load=1",
        success: function (data) {
            var collage = jQuery(data).find("#collage");
            jQuery(".osha-overlay.full").append("<span id='overlay-content'/>");
            jQuery("#overlay-content").append(collage);
            jQuery("#overlay-spinner").hide(); 
        }
    });
};

jQuery(document).ready(function () {
    "use strict";

    jQuery(".older-newsletter").hide();

    jQuery("#displaynl").click(function () {
        displaynl();
        return false;
    });

    jQuery("a[rel=oshmail-overlay]")
        .click(function () {
            OSHMAIL.loadOshmailContent(this);
            return false;
        });
    

    jQuery(".osha-overlay-close").click(function () {
        jQuery(".osha-overlay.full").hide("slow");
    });
});

