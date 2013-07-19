
/* Merged Plone Javascript file
 * This file is dynamically assembled from separate parts.
 * Some of these parts have 3rd party licenses or copyright information attached
 * Such information is valid for that section,
 * not for the entire composite file
 * originating files are separated by - filename.js -
 */

/* - ++resource++linkcollection.js - */
// http://osha.europa.eu/portal_javascripts/++resource++linkcollection.js?original=1
var LinkCollection={};LinkCollection.maxheight=0;LinkCollection.render_doc=function render_doc(node,uid){jq('a.current-linklist-item').removeClass('current-linklist-item');jq(node).addClass('current-linklist-item');jq('div.prefetched-docs').each(
function(i){if(jq(this).is(':visible')){jq(this).hide()}});var doc=jq('div#doc-'+uid);doc.fadeIn(300);if(doc.height()>LinkCollection.maxheight){LinkCollection.maxheight=doc.height()}
doc.height(LinkCollection.maxheight);linkbox=jq('div#slc-linkcollection-linkbox');linkboxtop=linkbox.offset().top;body=jq('html,body');body.scrollTop(linkboxtop);return false}


/* - osha.js - */
// http://osha.europa.eu/portal_javascripts/osha.js?original=1
var OSHA=OSHA?OSHA:new Object();portal_url='http://osha.europa.eu';
function adjustTitle(elem){var newTitle='(neues Fenster)';titleVal=elem.getAttribute('title');if(titleVal){if(titleVal.lastIndexOf(newTitle)==-1){titleVal=titleVal+' '+newTitle}}
else{titleVal='Externer Link: '+newTitle}
elem.setAttribute('title',titleVal)}
function osha_gotoURL(x){if(x==''){document.forms['networkchooser'].reset();return} else{if(x.substr(5,11)=='http://'){loc=x} else{loc='http://'+x}
window.location.href=loc}}
function getContentArea(){node=document.getElementById('region-content')
if(!node){node=document.getElementById('content')}
return node}
function getPortlets(){portlets=new Array();left=document.getElementById('portal-column-one');right=document.getElementById('portal-column-two');if(left){portlets.push(left)}
if(right){portlets.push(right)}
return portlets}
function scanforlinks(){if(!document.getElementsByTagName){return false};if(!document.getElementById){return false};contentarea=getContentArea();if(contentarea&&contentarea.getAttribute('scanforlinks')=='done'){return false}
if(typeof external_links_open_new_window=='string')
var elonw=external_links_open_new_window.toLowerCase()=='true';else elonw=false;portlets=getPortlets();if(!contentarea&&portlets.length<=0){return false}
var links=contentarea.getElementsByTagName('a');for(i=0;i<links.length;i++){modifyLinkTag(links[i],elonw)}
for(i=0;i<portlets.length;i++){var plinks=portlets[i].getElementsByTagName('a');for(j=0;j<plinks.length;j++){modifyLinkTag(plinks[j],elonw)}}
contentarea.setAttribute('scanforlinks','done')}
function injectNode(node,injectedtype,injectedclass){var injectednode=document.createElement(injectedtype)
var injectedtext=document.createTextNode(String.fromCharCode(160));injectednode.appendChild(injectedtext);injectednode.className=injectedclass;node.parentNode.insertBefore(injectednode,node)}
function modifyLinkTag(node,elonw){linkname=node.getAttribute('name');if(linkname){if(linkname.indexOf('navigationlink')==0){return}}
if(node.getAttribute('href')&&node.className.indexOf('link-plain')==-1){var linkval=node.getAttribute('href')
if(linkval.toLowerCase().indexOf(window.location.protocol+'//'+window.location.host)==0){} else if(linkval.indexOf('http:')!=0){protocols=['ftp','news','irc','callto']
for(p=0;p<protocols.length;p++){if(linkval.indexOf(protocols[p]+':')==0){linkclass='link-'+protocols[p]
injectNode(node,'span',linkclass+'-js')
if(node.className==linkclass||node.className==linkclass+'-js'){node.removeAttribute('class')}
break}}}
else{if(node.getElementsByTagName('img').length==0){if(elonw){node.setAttribute('target','_blank')}}}
pathelems=linkval.split('/');filename=pathelems[pathelems.length-1];fileelems=filename.split('.');if(filename.indexOf('?')<0&&fileelems.length>1&&node.getElementsByTagName('img').length==0){ending=fileelems[fileelems.length-1].toLowerCase();endings=['pdf','doc','xls','ppt','zip'];for(e=0;e<endings.length;e++){if(ending==endings[e]){linkclass='link-'+ending+'-js';injectNode(node,'span',linkclass);break}}}}}
registerPloneFunction(scanforlinks)
OSHA.slideSwitch=function(){var active=jq('#slideswitch IMG.active');if(active.length==0) active=jq('#slideswitch IMG:last');var next=active.next().length?active.next():jq('#slideswitch IMG:first');active.addClass('last-active');next.css({opacity:0.0}).removeClass('inactive').addClass('active').animate({opacity:1.0},1000, function(){active.removeClass('active last-active')});active.animate({opacity:0.0},1000, function(){active.addClass('inactive')})}
OSHA.startSlide=function(){setInterval("OSHA.slideSwitch()",5000)}
registerPloneFunction(OSHA.startSlide)
OSHA.toggleHiddenField=function(id){var hidden_field=jq("#"+id);if(hidden_field.val()=='True') hidden_field.val('');else hidden_field.val('True')}
function registerPloneFunction(func){if(window.addEventListener) window.addEventListener("load",func,false);else if(window.attachEvent) window.attachEvent("onload",func)}
function unRegisterPloneFunction(func){if(window.removeEventListener) window.removeEventListener("load",func,false);else if(window.detachEvent) window.detachEvent("onload",func)}


/* - flashobject.js - */
// http://osha.europa.eu/portal_javascripts/flashobject.js?original=1
if(typeof com=="undefined"){var com=new Object()}
if(typeof com.deconcept=="undefined"){com.deconcept=new Object()}
if(typeof com.deconcept.util=="undefined"){com.deconcept.util=new Object()}
if(typeof com.deconcept.FlashObjectUtil=="undefined"){com.deconcept.FlashObjectUtil=new Object()}
com.deconcept.FlashObject=function(_1,id,w,h,_5,c,_7,_8,_9,_a,_b){if(!document.createElement||!document.getElementById){return}
this.DETECT_KEY=_b?_b:"detectflash";this.skipDetect=com.deconcept.util.getRequestParameter(this.DETECT_KEY);this.params=new Object();this.variables=new Object();this.attributes=new Array();this.useExpressInstall=_7;if(_1){this.setAttribute("swf",_1)}
if(id){this.setAttribute("id",id)}
if(w){this.setAttribute("width",w)}
if(h){this.setAttribute("height",h)}
if(_5){this.setAttribute("version",new com.deconcept.PlayerVersion(_5.toString().split(".")))}
this.installedVer=com.deconcept.FlashObjectUtil.getPlayerVersion(this.getAttribute("version"),_7);if(c){this.addParam("bgcolor",c)}
var q=_8?_8:"high";this.addParam("quality",q);var _d=(_9)?_9:window.location;this.setAttribute("xiRedirectUrl",_d);this.setAttribute("redirectUrl","");if(_a){this.setAttribute("redirectUrl",_a)}};com.deconcept.FlashObject.prototype={setAttribute:function(_e,_f){this.attributes[_e]=_f},getAttribute:function(_10){return this.attributes[_10]},addParam:function(_11,_12){this.params[_11]=_12},getParams:function(){return this.params},addVariable:function(_13,_14){this.variables[_13]=_14},getVariable:function(_15){return this.variables[_15]},getVariables:function(){return this.variables},createParamTag:function(n,v){var p=document.createElement("param");p.setAttribute("name",n);p.setAttribute("value",v);return p},getVariablePairs:function(){var _19=new Array();var key;var _1b=this.getVariables();for(key in _1b){_19.push(key+"="+_1b[key])}
return _19},getFlashHTML:function(){var _1c="";if(navigator.plugins&&navigator.mimeTypes&&navigator.mimeTypes.length){if(this.getAttribute("doExpressInstall")){this.addVariable("MMplayerType","PlugIn")}
_1c="<embed type=\"application/x-shockwave-flash\" src=\""+this.getAttribute("swf")+"\" width=\""+this.getAttribute("width")+"\" height=\""+this.getAttribute("height")+"\"";_1c+=" id=\""+this.getAttribute("id")+"\" name=\""+this.getAttribute("id")+"\" ";var _1d=this.getParams();for(var key in _1d){_1c+=[key]+"=\""+_1d[key]+"\" "}
var _1f=this.getVariablePairs().join("&");if(_1f.length>0){_1c+="flashvars=\""+_1f+"\""}
_1c+="/>"}else{if(this.getAttribute("doExpressInstall")){this.addVariable("MMplayerType","ActiveX")}
_1c="<object id=\""+this.getAttribute("id")+"\" classid=\"clsid:D27CDB6E-AE6D-11cf-96B8-444553540000\" width=\""+this.getAttribute("width")+"\" height=\""+this.getAttribute("height")+"\">";_1c+="<param name=\"movie\" value=\""+this.getAttribute("swf")+"\" />";var _20=this.getParams();for(var key in _20){_1c+="<param name=\""+key+"\" value=\""+_20[key]+"\" />"}
var _22=this.getVariablePairs().join("&");if(_22.length>0){_1c+="<param name=\"flashvars\" value=\""+_22+"\" />"}_1c+="</object>"}
return _1c},write:function(_23){if(this.useExpressInstall){var _24=new com.deconcept.PlayerVersion([6,0,65]);if(this.installedVer.versionIsValid(_24)&&!this.installedVer.versionIsValid(this.getAttribute("version"))){this.setAttribute("doExpressInstall",true);this.addVariable("MMredirectURL",escape(this.getAttribute("xiRedirectUrl")));document.title=document.title.slice(0,47)+" - Flash Player Installation";this.addVariable("MMdoctitle",document.title)}}else{this.setAttribute("doExpressInstall",false)}
if(this.skipDetect||this.getAttribute("doExpressInstall")||this.installedVer.versionIsValid(this.getAttribute("version"))){var n=(typeof _23=="string")?document.getElementById(_23):_23;n.innerHTML=this.getFlashHTML()}else{if(this.getAttribute("redirectUrl")!=""){document.location.replace(this.getAttribute("redirectUrl"))}}}};com.deconcept.FlashObjectUtil.getPlayerVersion=function(_26,_27){var _28=new com.deconcept.PlayerVersion(0,0,0);if(navigator.plugins&&navigator.mimeTypes.length){var x=navigator.plugins["Shockwave Flash"];if(x&&x.description){_28=new com.deconcept.PlayerVersion(x.description.replace(/([a-z]|[A-Z]|\s)+/,"").replace(/(\s+r|\s+b[0-9]+)/,".").split("."))}}else{try{var axo=new ActiveXObject("ShockwaveFlash.ShockwaveFlash");for(var i=3;axo!=null;i++){axo=new ActiveXObject("ShockwaveFlash.ShockwaveFlash."+i);_28=new com.deconcept.PlayerVersion([i,0,0])}}
catch(e){}
if(_26&&_28.major>_26.major){return _28}
if(!_26||((_26.minor!=0||_26.rev!=0)&&_28.major==_26.major)||_28.major!=6||_27){try{_28=new com.deconcept.PlayerVersion(axo.GetVariable("$version").split(" ")[1].split(","))}catch(e){}}}
return _28};com.deconcept.PlayerVersion=function(_2c){this.major=parseInt(_2c[0])||0;this.minor=parseInt(_2c[1])||0;this.rev=parseInt(_2c[2])||0};com.deconcept.PlayerVersion.prototype.versionIsValid=function(fv){if(this.major<fv.major){return false}
if(this.major>fv.major){return true}
if(this.minor<fv.minor){return false}
if(this.minor>fv.minor){return true}
if(this.rev<fv.rev){return false}
return true};com.deconcept.util={getRequestParameter:function(_2e){var q=document.location.search||document.location.href.hash;if(q){var _30=q.indexOf(_2e+"=");var _31=(q.indexOf("&",_30)>-1)?q.indexOf("&",_30):q.length;if(q.length>1&&_30>-1){return q.substring(q.indexOf("=",_30)+1,_31)}}return ""},removeChildren:function(n){while(n.hasChildNodes()){n.removeChild(n.firstChild)}}};if(Array.prototype.push==null){Array.prototype.push=function(_33){this[this.length]=_33;return this.length}}
var getQueryParamValue=com.deconcept.util.getRequestParameter;var FlashObject=com.deconcept.FlashObject;

/* - fckeditor.js - */
// http://osha.europa.eu/portal_javascripts/fckeditor.js?original=1
var FCKeditor=function(instanceName,width,height,toolbarSet,value){this.InstanceName=instanceName ;this.Width=width||'100%' ;this.Height=height||'200' ;this.ToolbarSet=toolbarSet||'Default' ;this.Value=value||'' ;this.BasePath=FCKeditor.BasePath ;this.CheckBrowser=true ;this.DisplayErrors=true ;this.Config=new Object() ;this.OnError=null }
FCKeditor.BasePath='/fckeditor/' ;FCKeditor.MinHeight=200 ;FCKeditor.MinWidth=750 ;FCKeditor.prototype.Version='2.6.3' ;FCKeditor.prototype.VersionBuild='19836' ;FCKeditor.prototype.Create=function(){document.write(this.CreateHtml()) }
FCKeditor.prototype.CreateHtml=function(){if(!this.InstanceName||this.InstanceName.length==0){this._ThrowError(701,'You must specify an instance name.') ;return '' }
var sHtml='' ;if(!this.CheckBrowser||this._IsCompatibleBrowser()){sHtml+='<input type="hidden" id="'+this.InstanceName+'" name="'+this.InstanceName+'" value="'+this._HTMLEncode(this.Value)+'" style="display:none" />' ;sHtml+=this._GetConfigHtml() ;sHtml+=this._GetIFrameHtml() }
else{var sWidth=this.Width.toString().indexOf('%')>0?this.Width:this.Width+'px' ;var sHeight=this.Height.toString().indexOf('%')>0?this.Height:this.Height+'px' ;sHtml+='<textarea name="'+this.InstanceName+'" rows="4" cols="40" style="width:'+sWidth+';height:'+sHeight ;if(this.TabIndex)
sHtml+='" tabindex="'+this.TabIndex ;sHtml+='">'+this._HTMLEncode(this.Value)+'<\/textarea>' }
return sHtml }
FCKeditor.prototype.ReplaceTextarea=function(){if(!this.CheckBrowser||this._IsCompatibleBrowser()){var oTextarea=document.getElementById(this.InstanceName) ;var colElementsByName=document.getElementsByName(this.InstanceName) ;var i=0;while(oTextarea||i==0){if(oTextarea&&oTextarea.tagName.toLowerCase()=='textarea')
break ;oTextarea=colElementsByName[i++] }
if(!oTextarea){alert('Error: The TEXTAREA with id or name set to "'+this.InstanceName+'" was not found') ;return }
oTextarea.style.display='none' ;if(oTextarea.tabIndex)
this.TabIndex=oTextarea.tabIndex ;this._InsertHtmlBefore(this._GetConfigHtml(),oTextarea) ;this._InsertHtmlBefore(this._GetIFrameHtml(),oTextarea) }}
FCKeditor.prototype._InsertHtmlBefore=function(html,element){if(element.insertAdjacentHTML)
element.insertAdjacentHTML('beforeBegin',html) ;else{var oRange=document.createRange() ;oRange.setStartBefore(element) ;var oFragment=oRange.createContextualFragment(html);element.parentNode.insertBefore(oFragment,element) }}
FCKeditor.prototype._GetConfigHtml=function(){var sConfig='' ;for(var o in this.Config){if(sConfig.length>0) sConfig+='&amp;' ;sConfig+=encodeURIComponent(o)+'='+encodeURIComponent(this.Config[o]) }
return '<input type="hidden" id="'+this.InstanceName+'___Config" value="'+sConfig+'" style="display:none" />' }
FCKeditor.prototype._GetIFrameHtml=function(){var sFile='fckeditor.html' ;try{if((/fcksource=true/i).test(window.top.location.search))
sFile='fckeditor.original.html' }
catch(e){}
var sLink=this.BasePath+'editor/'+sFile+'?InstanceName='+encodeURIComponent(this.InstanceName) ;if(this.ToolbarSet)
sLink+='&amp;Toolbar='+this.ToolbarSet ;html='<iframe id="'+this.InstanceName+'___Frame" src="'+sLink+'" width="'+this.Width+'" height="'+this.Height ;if(this.TabIndex)
html+='" tabindex="'+this.TabIndex ;html+='" frameborder="0" scrolling="no"></iframe>' ;return html }
FCKeditor.prototype._IsCompatibleBrowser=function(){return FCKeditor_IsCompatibleBrowser() }
FCKeditor.prototype._ThrowError=function(errorNumber,errorDescription){this.ErrorNumber=errorNumber ;this.ErrorDescription=errorDescription ;if(this.DisplayErrors){document.write('<div style="COLOR: #ff0000">') ;document.write('[ FCKeditor Error '+this.ErrorNumber+': '+this.ErrorDescription+' ]') ;document.write('</div>') }
if(typeof(this.OnError)=='function')
this.OnError(this,errorNumber,errorDescription) }
FCKeditor.prototype._HTMLEncode=function(text){if(typeof(text)!="string")
text=text.toString() ;text=text.replace(/&/g,"&amp;").replace(/"/g, "&quot;").replace(/</g,"&lt;").replace(/>/g,"&gt;") ;return text }
;(function(){var textareaToEditor=function(textarea){var editor=new FCKeditor(textarea.name) ;editor.Width=Math.max(textarea.offsetWidth,FCKeditor.MinWidth) ;editor.Height=Math.max(textarea.offsetHeight,FCKeditor.MinHeight) ;return editor }
FCKeditor.ReplaceAllTextareas=function(){var textareas=document.getElementsByTagName('textarea') ;for(var i=0 ;i<textareas.length ;i++){var editor=null ;var textarea=textareas[i] ;var name=textarea.name ;if(!name||name.length==0)
continue ;if(typeof arguments[0]=='string'){var classRegex=new RegExp('(?:^| )'+arguments[0]+'(?:$| )') ;if(!classRegex.test(textarea.className))
continue }
else if(typeof arguments[0]=='function'){editor=textareaToEditor(textarea) ;if(arguments[0](textarea,editor)===false)
continue }
if(!editor)
editor=textareaToEditor(textarea) ;editor.ReplaceTextarea() }}})() ;
function FCKeditor_IsCompatibleBrowser(){var sAgent=navigator.userAgent.toLowerCase() ;if(/*@cc_on!@*/false&&sAgent.indexOf("mac")==-1){var sBrowserVersion=navigator.appVersion.match(/MSIE (.\..)/)[1] ;return(sBrowserVersion>=5.5) }
if(navigator.product=="Gecko"&&navigator.productSub>=20030210&&!(typeof(opera)=='object'&&opera.postError))
return true ;if(window.opera&&window.opera.version&&parseFloat(window.opera.version())>=9.5)
return true ;if(sAgent.indexOf(' adobeair/')!=-1)
return(sAgent.match(/ adobeair\/(\d+)/ )[1] >= 1 ) ;	// Build must be at least v1
if(sAgent.indexOf(' applewebkit/')!=-1)
return(sAgent.match(/ applewebkit\/(\d+)/ )[1] >= 522 ) ;	// Build must be at least 522(v3)
return false }


/* - fck_plone.js - */
// http://osha.europa.eu/portal_javascripts/fck_plone.js?original=1
var FCKBaseHref={};makeLinksRelative=function(basehref,contents){var base=basehref.replace('http://osha.europa.eu','');var href=base.replace(/\/[^\/]*$/,'/');var hrefparts=href.split('/');return contents.replace(/(<[^>]* (?:src|href)=")([^"]*)"/g,
function(str,tag,url,offset,contents){url=url.replace('http://osha.europa.eu','');if(url.substring(0,1)=='#'){str=tag+url+'"'}
else{var urlparts=url.split('#');var anchor=urlparts[1]||'';url=urlparts[0];var urlparts=url.split('/');var common=0;while(common<urlparts.length&&common<hrefparts.length&&urlparts[common]==hrefparts[common])
common++;var last=urlparts[common];if(common+1==urlparts.length&&last=='emptypage'){urlparts[common]=''}
if(common>0){var path=new Array();var i=0;for(;i+common<hrefparts.length-1;i++){path[i]='..'};while(common<urlparts.length){path[i++]=urlparts[common++]};if(i==0){path[i++]='.'}
str=path.join('/');if(anchor){str=[str,anchor].join('#')}
str=tag+str+'"'}}
return str})};finalizePublication=function(editorInstance){var oField=editorInstance.LinkedField;var fieldName=oField.name;var baseHref=FCKBaseHref[fieldName];if(baseHref){relativeLinksHtml=makeLinksRelative(FCKBaseHref[fieldName],editorInstance.GetXHTML());oField.value=relativeLinksHtml}
else oField.value=editorInstance.GetXHTML()}
getParamValue=function(id){value=document.getElementById(id).value;if(value=='true') return true;if(value=='false') return false;return value}
FCKeditor_Plone_start_instance=function(fckContainer,inputname){var inputContainer=document.getElementById(inputname+'_'+'cleaninput');if(inputContainer){var fckParams=['path_user','base_path','fck_basehref','links_basehref','input_url','allow_server_browsing','browser_root','allow_file_upload','allow_image_upload','allow_flash_upload','fck_skin_path','lang','fck_default_r2l','force_paste_as_text','allow_latin_entities','spellchecker','keyboard_entermode','keyboard_shiftentermode','fck_toolbar','editor_width','editor_height'];var fckValues={};for(var i=0;i<fckParams.length;i++){var id=inputname+'_'+fckParams [i];fckValues [fckParams [i]]=getParamValue(id)}
var oFck=new FCKeditor(inputname);var pathUser=fckValues ['path_user']+'/';oFck.BasePath=fckValues ['base_path']+'/';oFck.Config['CustomConfigurationsPath']=fckValues ['input_url']+'/fckconfigPlone.js?field_name='+inputname;oFck.BaseHref=fckValues ['fck_basehref'];FCKBaseHref[inputname]=fckValues ['links_basehref'];if(inputContainer.innerText!=undefined) oFck.Value=inputContainer.innerText;else oFck.Value=inputContainer.textContent;oFck.Config['LinkBrowser']=fckValues ['allow_server_browsing'];oFck.Config['LinkBrowserURL']=fckValues ['base_path']+'/fckbrowser/browser.html?field_name='+inputname+'&Connector='+fckValues ['input_url']+'/connectorPlone&ServerPath='+fckValues ['browser_root']+'&CurrentPath='+pathUser ;oFck.Config['LinkUpload']=fckValues ['allow_file_upload'] ;oFck.Config['LinkUploadURL']=fckValues ['input_url']+'/uploadPlone?field_name='+inputname+'&CurrentPath='+pathUser;oFck.Config['ImageBrowser']=fckValues ['allow_server_browsing'];oFck.Config['ImageBrowserURL']=fckValues ['base_path']+'/fckbrowser/browser.html?field_name='+inputname+'&Type=Image&Connector='+fckValues ['input_url']+'/connectorPlone&ServerPath='+fckValues ['browser_root']+'&CurrentPath='+pathUser ;oFck.Config['ImageUpload']=fckValues ['allow_image_upload'] ;oFck.Config['ImageUploadURL']=fckValues ['input_url']+'/uploadPlone?field_name='+inputname+'&CurrentPath='+pathUser;oFck.Config['FlashBrowser']=fckValues ['allow_server_browsing'];oFck.Config['FlashBrowserURL']=fckValues ['base_path']+'/fckbrowser/browser.html?field_name='+inputname+'&Type=Flash&Connector='+fckValues ['input_url']+'/connectorPlone&ServerPath='+fckValues ['browser_root']+'&CurrentPath='+pathUser ;oFck.Config['FlashUpload']=fckValues ['allow_flash_upload'] ;oFck.Config['FlashUploadURL']=fckValues ['input_url']+'/uploadPlone?field_name='+inputname+'&CurrentPath='+pathUser;oFck.Config['MediaBrowser']=fckValues ['allow_server_browsing'];oFck.Config['MediaBrowserURL']=fckValues ['base_path']+'/fckbrowser/browser.html?field_name='+inputname+'&Type=Media&Connector='+fckValues ['input_url']+'/connectorPlone&ServerPath='+fckValues ['browser_root']+'&CurrentPath='+pathUser ;oFck.Config['SkinPath']=fckValues ['base_path']+'/editor/'+fckValues ['fck_skin_path'];oFck.Config['AutoDetectLanguage']=false;oFck.Config['DefaultLanguage']=fckValues ['lang'];oFck.Config['ForcePasteAsPlainText']=fckValues ['force_paste_as_text'];oFck.Config['IncludeLatinEntities']=fckValues ['allow_latin_entities'];oFck.Config['SpellChecker']=fckValues ['spellchecker'];oFck.Config['EnterMode']=fckValues ['keyboard_entermode'];oFck.Config['ShiftEnterMode']=fckValues ['keyboard_shiftentermode'];oFck.ToolbarSet=fckValues ['fck_toolbar'];oFck.Width=fckValues ['editor_width'];oFck.Height=fckValues ['editor_height'];try{fckContainer.innerHTML=oFck.CreateHtml();document.getElementById(inputname+'_fckLoading').style.display='none'}
catch(e){document.getElementById(inputname+'_fckLoading').style.display='none';document.getElementById(inputname+'_fckError').style.display='block'}}}
Save_inline=function(fieldname,form,editorInstance){if(editorInstance.Commands.GetCommand('FitWindow').GetState()){kukit.log('Full screen mode must be disabled before saving inline');editorInstance.Commands.GetCommand('FitWindow').Execute()} ;saveField=document.getElementById(fieldname+'_fckSaveField');if(saveField){kukit.log('Fire the savekupu server event = save inline without submitting');saveField.style.visibility='visible';if(saveField.fireEvent){saveField.fireEvent('onChange')}
else{var evt=document.createEvent("HTMLEvents");evt.initEvent("change",true,true);saveField.dispatchEvent(evt)}
comp=(setTimeout("saveField.style.visibility='hidden'",2000));return false}
else{kukit.log('Try to submit the form in portal_factory');window.onbeforeunload=null;form.submit()}}


/* - ++resource++slc.linguatools.static/linguatools.js - */
// http://osha.europa.eu/portal_javascripts/++resource++slc.linguatools.static/linguatools.js?original=1
jq(document).ready(function(){jq(".toggle_container").hide();jq(".trigger").toggle(function(){jq(this).addClass("active")}, function(){jq(this).removeClass("active")});jq(".trigger").click(function(){jq(this).next(".toggle_container").slideToggle("medium")})});
