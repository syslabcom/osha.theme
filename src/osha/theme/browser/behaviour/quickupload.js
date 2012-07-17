/* Open the collective.quickupload ajax view in an overlay when #contentview-upload (an action) is clicked. 

   The hidden input field is wrapped in a form in the main template: form#quickuploader
*/

var OSHUPLOAD = {}

OSHUPLOAD.showUploader = function () {
    // If it gets called again when it's already opened it loads the
    // content of the page into the element
    if ( jQuery(".quick-uploader").length < 1 ) {
        jQuery(this).addClass("selected");
        jQuery("form#quickuploader").each(function(){
            var uploadUrl =  jQuery('.uploadUrl', this).val();
            var uploadData =  jQuery('.uploadData', this).val();
            var UlDiv = jQuery(this);
            jQuery.ajax({
                type: 'GET',
                url: uploadUrl,
                data: uploadData,
                dataType: 'html',
                contentType: 'text/html; charset=utf-8',
                success: function(html) {
                    UlDiv.html(html);
                } });
        });
    };
};


jQuery(document).ready( function () {
    // workaround this MSIE bug :
    // https://dev.plone.org/plone/ticket/10894
    if (jQuery.browser.msie) jQuery("#settings").remove();
    var Browser = {};
    Browser.onUploadComplete = function() {
        window.location.reload();
    }

    // Disable the action link
    uploadAction = jQuery("#contentview-upload")
        .find("a")
        .removeAttr("href");

    jQuery("#contentview-upload").click(OSHUPLOAD.showUploader);
})