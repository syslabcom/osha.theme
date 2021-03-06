var OSHMAIL = {};



/* Replaced by #4002 request to change oshmail design. Instead of loading the 
   original collage view we now load the generated email output directly into 
   a fancybox iframe 
   can be removed if not needed after 10.2012 */
   
OSHMAIL.loadOshmailContent = function (linkObj) {
    "use strict";

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
        url: linkObj.href + "&ajax_load=1",
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

    jQuery("a[rel=oshmail-overlay]").fancybox({
         'width' : '75%',
         'height' : '75%',
         'autoScale' : false,
         'transitionIn' : 'none',
         'transitionOut' : 'none',
         'type' : 'iframe'
     });
 

    jQuery(".older-newsletter").hide();

    jQuery("#displaynl").click(function () {
        jQuery('.fadercontrol').hide();
        jQuery('.older-newsletter').fadeIn('slow');
        return false;
    });


    /* Replaced by #4002 request to change oshmail design. Instead of loading the 
       original collage view we now load the generated email output directly into 
       a fancybox iframe 
       can be removed if not needed after 10.2012 */
       
/*    jQuery("a[rel=oshmail-overlay]")
        .click(function () {
            OSHMAIL.loadOshmailContent(this);
            return false;
        });
  */  

    jQuery(".osha-overlay-close").click(function () {
        jQuery(".osha-overlay.full").hide("slow");
    });
});

