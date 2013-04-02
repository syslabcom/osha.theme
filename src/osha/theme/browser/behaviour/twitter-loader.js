jQuery(document).ready(function() {
    jQuery("dl.portlet-static-twitter")
        .parent()
        .load("/en/twitter?ajax_load=True dl.twitter-tweet");
});
