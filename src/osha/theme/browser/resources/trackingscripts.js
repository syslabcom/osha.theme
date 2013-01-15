jQuery(document).ready(
    function(){
        jQuery('.publicationURL a').bind('click', function(event){
        $url = this['href'];
        $url=$url.replace(/(http[s]?:\/\/[\S]+?)\/(\S|$)/gim, '/Events/PDF/$2');
        $url = $url.replace('/at_download/file', '');
        pageTracker._trackPageview($url);
        return true;
        });
    }
)

