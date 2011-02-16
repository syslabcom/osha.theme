jq(document).ready(
    function(){
        jq('.publicationURL a').bind('click', function(event){
        $url = this['href'];
        $url=$url.replace(/(http:\/\/[\S]+?)\/(\S|$)/gim, '$1/Events/PDF/$2');
        $url = $url.replace('/at_download/file', '');
        pageTracker._trackPageview($url);
        return true;
        });
    }
)

