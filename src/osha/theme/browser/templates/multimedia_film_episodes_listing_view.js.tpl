videoPlayer = function () {
	return {
		showVideo: function() {
			var videos = $videos;
			var videoId = jQuery(this).attr("id");
			var video = videos[videoId];
			jwplayer("video_container").setup({
				players: [{ type: "flash",
							src: "/++resource++jwplayer.swf" },
						  { type: "html5" }],
				width: $video_width,
				height: $video_height,
				image: video["image"],
				levels: [
					{file: video["video_mp4"]},
					{file: video["video_webm"]},
					{file: video["video_ogv"]}
				] });
		},

		hideVideo: function() {
			jQuery("#video_container_wrapper").fadeOut();
		},
	};

}();

jQuery(document).ready(function() {
	videos = jQuery("div#content a.video");
	if (videos.length>0) {
		videos.click(videoPlayer.showVideo);
		videos.fancybox({
			'transitionIn' : 'elastic',
			'transitionOut' : 'elastic',
			'titlePosition' : 'over',
			'overlayOpacity' : 0.7,
			'overlayColor' : '#000',
			'autoDimensions' : false,
			'onCleanup' : videoPlayer.hideVideo,
			'showNavArrows' : false,
			'titlePosition' : 'outside',
			'width' : $video_width,
			'height' : $video_height
		});
	}
})
