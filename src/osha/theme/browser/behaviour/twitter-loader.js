jQuery(document).ready(function() {
    jQuery("dl.portlet-static-latest-tweets")
        .parent()
        .load("/en/twitter?ajax_load=True dl.latest-tweets-tweet");
});
