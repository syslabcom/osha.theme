var videoPlayer = function () {
	"use strict";
	return {
		showVideo: function (videoId) {
			var videos = $videos, video = videos[videoId];
			jQuery("#video_container").show("slow");
			jwplayer("video").setup({
				modes: [
					{ type: "html5" },
					{ type: "flash",
					  src: "++resource++osha.theme.resources/jwplayer/player.swf"
                    }
				],
				width: $video_width,
				height: $video_height,
				image: video.image,
				levels: [
					{file: video.video_mp4},
					{file: video.video_webm},
					{file: video.video_ogv}
				],
			});
		}
	};
}();

jQuery(document).ready (function() {
	"use strict";
	var videos = jQuery("div#content a.video");
	jQuery(videos).each(function () {
		var video = jQuery(this);
		video.click(function () {
			videoPlayer.showVideo(video.attr("id"));
			return false;
		});
	});
	jQuery("#video_close").click(function () {
		jQuery("#video_container")
			.hide("slow", function () {
				jwplayer("video").remove();
			});
	})
});
