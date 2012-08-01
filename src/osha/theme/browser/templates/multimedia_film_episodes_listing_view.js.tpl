videoPlayer = function () {
	return {
		showVideo: function(videoId) {
			var videos = $videos, video = videos[videoId];
			jwplayer("video_container").setup({
			players: [
                { type: "html5" },
                { type: "flash",
				  src: "/++resource++osha.theme.resources/jwplayer/player.swf" },],
				width: $video_width,
				height: $video_height,
				image: video["image"],
				levels: [
					{file: video["video_mp4"]},
					{file: video["video_webm"]},
					{file: video["video_ogv"]}
				],
                events: {
                    onReady: function(event) {
                        jQuery("#video_container").overlay({load: true, effect: "osha", css: {"z-index": 10}});
                    }
                }
            });
		},
	};
}();

jQuery(document).ready(function() {
    /* A custom effect which allows custom css to be applied to the
       overlay which does not work directly from css, e.g. z-index */
    jQuery.tools.overlay.addEffect(
        "osha", 
        function(css, done) {
            var conf = this.getConf(),
            overlay = this.getOverlay();
            
            // Seems to be necessary to allow for setting top and left
            if (conf.fixed)  {
                css.position = 'fixed';
            } else {
                css.top += jQuery(window).scrollTop();
                css.left += jQuery(window).scrollLeft();
                css.position = 'absolute';
            }
            
            jQuery.extend(css, conf.css)
            overlay.css(css).show();
        }, 
        function(done) { 
            var overlay = this.getOverlay();
            overlay.hide();
            done.call();
        }
    );

	videos = jQuery("div#content a.video");
    jQuery(videos).each(function () {
        var video = jQuery(this);
        video.click(function () {
            videoPlayer.showVideo(video.attr("id"));
            return false;
        });
    });
})
