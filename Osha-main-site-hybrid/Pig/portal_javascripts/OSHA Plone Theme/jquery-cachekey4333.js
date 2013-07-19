
var __dEcOdE=function(a,c,k,e,d){e=function(c){return(c<a?"":e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--)d["$"+e(c)]=k[c]||e(c);k=[function(e){r=d["$"+e];return r!=undefined?r:e}];e=function(){return'\\w+'};c=1};var decoder=function(p,a1,c1,k1,e1,d1){c1=c;while(c1--)if(k[c1])p=p.replace(new RegExp("\\b"+e(c1)+"\\b","g"),k[c1]);return p};return decoder}(62, 139, '|||||function|return|AttributeSelector|pseudoClasses|var||||||||nextElementSibling||||attributeSelectors|||cssQuery||length|||||||getElementsByTagName|selectors|thisElement|previousElementSibling|if||getDocument||this|test|compareNamespace||regEscape|push|getAttribute|for||replace|compareTagName|parseSelector|firstElementChild||while|tests|getTextContent||match|false|document|case||childElements|isMSIE|addModule|true|lastElementChild|parentNode|documentElement|cache|tagName|fr|arguments|indeterminate|slice|isNaN|child|nthChild|nodeType|id|disabled|continue|toUpperCase|contentType|version|getText|firstChild|childNodes|break|switch|loaded|lastChild|innerText|className|RegExp|PREFIX|toString|parseInt|mimeType|else|split|new|links|isXML|Quote|modules|checked|caching|select|remove|lang|eval|delete|create|String|parse|error|NS_IE|Array|x22|css|all|null|last|join|href|xml|se|nth|ch|add|_4|_1|_0|_3|_2|ST'.split('|'), 0, {});

/* Merged Plone Javascript file
 * This file is dynamically assembled from separate parts.
 * Some of these parts have 3rd party licenses or copyright information attached
 * Such information is valid for that section,
 * not for the entire composite file
 * originating files are separated by - filename.js -
 */

/* - jquery.js - */
/*
 * jQuery JavaScript Library v1.3.2
 * http://jquery.com/
 *
 * Copyright (c) 2009 John Resig
 * Dual licensed under the MIT and GPL licenses.
 * http://docs.jquery.com/License
 *
 * Date: 2009-02-19 17:34:21 -0500 (Thu, 19 Feb 2009)
 * Revision: 6246
 */
(function(){var l=this,g,y=l.jQuery,p=l.$,o=l.jQuery=l.$=function(E,F){return new o.fn.init(E,F)},D=/^[^<]*(<(.|\s)+>)[^>]*$|^#([\w-]+)$/,f=/^.[^:#\[\.,]*$/;o.fn=o.prototype={init:function(E,H){E=E||document;if(E.nodeType){this[0]=E;this.length=1;this.context=E;return this}if(typeof E==="string"){var G=D.exec(E);if(G&&(G[1]||!H)){if(G[1]){E=o.clean([G[1]],H)}else{var I=document.getElementById(G[3]);if(I&&I.id!=G[3]){return o().find(E)}var F=o(I||[]);F.context=document;F.selector=E;return F}}else{return o(H).find(E)}}else{if(o.isFunction(E)){return o(document).ready(E)}}if(E.selector&&E.context){this.selector=E.selector;this.context=E.context}return this.setArray(o.isArray(E)?E:o.makeArray(E))},selector:"",jquery:"1.3.2",size:function(){return this.length},get:function(E){return E===g?Array.prototype.slice.call(this):this[E]},pushStack:function(F,H,E){var G=o(F);G.prevObject=this;G.context=this.context;if(H==="find"){G.selector=this.selector+(this.selector?" ":"")+E}else{if(H){G.selector=this.selector+"."+H+"("+E+")"}}return G},setArray:function(E){this.length=0;Array.prototype.push.apply(this,E);return this},each:function(F,E){return o.each(this,F,E)},index:function(E){return o.inArray(E&&E.jquery?E[0]:E,this)},attr:function(F,H,G){var E=F;if(typeof F==="string"){if(H===g){return this[0]&&o[G||"attr"](this[0],F)}else{E={};E[F]=H}}return this.each(function(I){for(F in E){o.attr(G?this.style:this,F,o.prop(this,E[F],G,I,F))}})},css:function(E,F){if((E=="width"||E=="height")&&parseFloat(F)<0){F=g}return this.attr(E,F,"curCSS")},text:function(F){if(typeof F!=="object"&&F!=null){return this.empty().append((this[0]&&this[0].ownerDocument||document).createTextNode(F))}var E="";o.each(F||this,function(){o.each(this.childNodes,function(){if(this.nodeType!=8){E+=this.nodeType!=1?this.nodeValue:o.fn.text([this])}})});return E},wrapAll:function(E){if(this[0]){var F=o(E,this[0].ownerDocument).clone();if(this[0].parentNode){F.insertBefore(this[0])}F.map(function(){var G=this;while(G.firstChild){G=G.firstChild}return G}).append(this)}return this},wrapInner:function(E){return this.each(function(){o(this).contents().wrapAll(E)})},wrap:function(E){return this.each(function(){o(this).wrapAll(E)})},append:function(){return this.domManip(arguments,true,function(E){if(this.nodeType==1){this.appendChild(E)}})},prepend:function(){return this.domManip(arguments,true,function(E){if(this.nodeType==1){this.insertBefore(E,this.firstChild)}})},before:function(){return this.domManip(arguments,false,function(E){this.parentNode.insertBefore(E,this)})},after:function(){return this.domManip(arguments,false,function(E){this.parentNode.insertBefore(E,this.nextSibling)})},end:function(){return this.prevObject||o([])},push:[].push,sort:[].sort,splice:[].splice,find:function(E){if(this.length===1){var F=this.pushStack([],"find",E);F.length=0;o.find(E,this[0],F);return F}else{return this.pushStack(o.unique(o.map(this,function(G){return o.find(E,G)})),"find",E)}},clone:function(G){var E=this.map(function(){if(!o.support.noCloneEvent&&!o.isXMLDoc(this)){var I=this.outerHTML;if(!I){var J=this.ownerDocument.createElement("div");J.appendChild(this.cloneNode(true));I=J.innerHTML}return o.clean([I.replace(/ jQuery\d+="(?:\d+|null)"/g,"").replace(/^\s*/,"")])[0]}else{return this.cloneNode(true)}});if(G===true){var H=this.find("*").andSelf(),F=0;E.find("*").andSelf().each(function(){if(this.nodeName!==H[F].nodeName){return}var I=o.data(H[F],"events");for(var K in I){for(var J in I[K]){o.event.add(this,K,I[K][J],I[K][J].data)}}F++})}return E},filter:function(E){return this.pushStack(o.isFunction(E)&&o.grep(this,function(G,F){return E.call(G,F)})||o.multiFilter(E,o.grep(this,function(F){return F.nodeType===1})),"filter",E)},closest:function(E){var G=o.expr.match.POS.test(E)?o(E):null,F=0;return this.map(function(){var H=this;while(H&&H.ownerDocument){if(G?G.index(H)>-1:o(H).is(E)){o.data(H,"closest",F);return H}H=H.parentNode;F++}})},not:function(E){if(typeof E==="string"){if(f.test(E)){return this.pushStack(o.multiFilter(E,this,true),"not",E)}else{E=o.multiFilter(E,this)}}var F=E.length&&E[E.length-1]!==g&&!E.nodeType;return this.filter(function(){return F?o.inArray(this,E)<0:this!=E})},add:function(E){return this.pushStack(o.unique(o.merge(this.get(),typeof E==="string"?o(E):o.makeArray(E))))},is:function(E){return !!E&&o.multiFilter(E,this).length>0},hasClass:function(E){return !!E&&this.is("."+E)},val:function(K){if(K===g){var E=this[0];if(E){if(o.nodeName(E,"option")){return(E.attributes.value||{}).specified?E.value:E.text}if(o.nodeName(E,"select")){var I=E.selectedIndex,L=[],M=E.options,H=E.type=="select-one";if(I<0){return null}for(var F=H?I:0,J=H?I+1:M.length;F<J;F++){var G=M[F];if(G.selected){K=o(G).val();if(H){return K}L.push(K)}}return L}return(E.value||"").replace(/\r/g,"")}return g}if(typeof K==="number"){K+=""}return this.each(function(){if(this.nodeType!=1){return}if(o.isArray(K)&&/radio|checkbox/.test(this.type)){this.checked=(o.inArray(this.value,K)>=0||o.inArray(this.name,K)>=0)}else{if(o.nodeName(this,"select")){var N=o.makeArray(K);o("option",this).each(function(){this.selected=(o.inArray(this.value,N)>=0||o.inArray(this.text,N)>=0)});if(!N.length){this.selectedIndex=-1}}else{this.value=K}}})},html:function(E){return E===g?(this[0]?this[0].innerHTML.replace(/ jQuery\d+="(?:\d+|null)"/g,""):null):this.empty().append(E)},replaceWith:function(E){return this.after(E).remove()},eq:function(E){return this.slice(E,+E+1)},slice:function(){return this.pushStack(Array.prototype.slice.apply(this,arguments),"slice",Array.prototype.slice.call(arguments).join(","))},map:function(E){return this.pushStack(o.map(this,function(G,F){return E.call(G,F,G)}))},andSelf:function(){return this.add(this.prevObject)},domManip:function(J,M,L){if(this[0]){var I=(this[0].ownerDocument||this[0]).createDocumentFragment(),F=o.clean(J,(this[0].ownerDocument||this[0]),I),H=I.firstChild;if(H){for(var G=0,E=this.length;G<E;G++){L.call(K(this[G],H),this.length>1||G>0?I.cloneNode(true):I)}}if(F){o.each(F,z)}}return this;function K(N,O){return M&&o.nodeName(N,"table")&&o.nodeName(O,"tr")?(N.getElementsByTagName("tbody")[0]||N.appendChild(N.ownerDocument.createElement("tbody"))):N}}};o.fn.init.prototype=o.fn;function z(E,F){if(F.src){o.ajax({url:F.src,async:false,dataType:"script"})}else{o.globalEval(F.text||F.textContent||F.innerHTML||"")}if(F.parentNode){F.parentNode.removeChild(F)}}function e(){return +new Date}o.extend=o.fn.extend=function(){var J=arguments[0]||{},H=1,I=arguments.length,E=false,G;if(typeof J==="boolean"){E=J;J=arguments[1]||{};H=2}if(typeof J!=="object"&&!o.isFunction(J)){J={}}if(I==H){J=this;--H}for(;H<I;H++){if((G=arguments[H])!=null){for(var F in G){var K=J[F],L=G[F];if(J===L){continue}if(E&&L&&typeof L==="object"&&!L.nodeType){J[F]=o.extend(E,K||(L.length!=null?[]:{}),L)}else{if(L!==g){J[F]=L}}}}}return J};var b=/z-?index|font-?weight|opacity|zoom|line-?height/i,q=document.defaultView||{},s=Object.prototype.toString;o.extend({noConflict:function(E){l.$=p;if(E){l.jQuery=y}return o},isFunction:function(E){return s.call(E)==="[object Function]"},isArray:function(E){return s.call(E)==="[object Array]"},isXMLDoc:function(E){return E.nodeType===9&&E.documentElement.nodeName!=="HTML"||!!E.ownerDocument&&o.isXMLDoc(E.ownerDocument)},globalEval:function(G){if(G&&/\S/.test(G)){var F=document.getElementsByTagName("head")[0]||document.documentElement,E=document.createElement("script");E.type="text/javascript";if(o.support.scriptEval){E.appendChild(document.createTextNode(G))}else{E.text=G}F.insertBefore(E,F.firstChild);F.removeChild(E)}},nodeName:function(F,E){return F.nodeName&&F.nodeName.toUpperCase()==E.toUpperCase()},each:function(G,K,F){var E,H=0,I=G.length;if(F){if(I===g){for(E in G){if(K.apply(G[E],F)===false){break}}}else{for(;H<I;){if(K.apply(G[H++],F)===false){break}}}}else{if(I===g){for(E in G){if(K.call(G[E],E,G[E])===false){break}}}else{for(var J=G[0];H<I&&K.call(J,H,J)!==false;J=G[++H]){}}}return G},prop:function(H,I,G,F,E){if(o.isFunction(I)){I=I.call(H,F)}return typeof I==="number"&&G=="curCSS"&&!b.test(E)?I+"px":I},className:{add:function(E,F){o.each((F||"").split(/\s+/),function(G,H){if(E.nodeType==1&&!o.className.has(E.className,H)){E.className+=(E.className?" ":"")+H}})},remove:function(E,F){if(E.nodeType==1){E.className=F!==g?o.grep(E.className.split(/\s+/),function(G){return !o.className.has(F,G)}).join(" "):""}},has:function(F,E){return F&&o.inArray(E,(F.className||F).toString().split(/\s+/))>-1}},swap:function(H,G,I){var E={};for(var F in G){E[F]=H.style[F];H.style[F]=G[F]}I.call(H);for(var F in G){H.style[F]=E[F]}},css:function(H,F,J,E){if(F=="width"||F=="height"){var L,G={position:"absolute",visibility:"hidden",display:"block"},K=F=="width"?["Left","Right"]:["Top","Bottom"];function I(){L=F=="width"?H.offsetWidth:H.offsetHeight;if(E==="border"){return}o.each(K,function(){if(!E){L-=parseFloat(o.curCSS(H,"padding"+this,true))||0}if(E==="margin"){L+=parseFloat(o.curCSS(H,"margin"+this,true))||0}else{L-=parseFloat(o.curCSS(H,"border"+this+"Width",true))||0}})}if(H.offsetWidth!==0){I()}else{o.swap(H,G,I)}return Math.max(0,Math.round(L))}return o.curCSS(H,F,J)},curCSS:function(I,F,G){var L,E=I.style;if(F=="opacity"&&!o.support.opacity){L=o.attr(E,"opacity");return L==""?"1":L}if(F.match(/float/i)){F=w}if(!G&&E&&E[F]){L=E[F]}else{if(q.getComputedStyle){if(F.match(/float/i)){F="float"}F=F.replace(/([A-Z])/g,"-$1").toLowerCase();var M=q.getComputedStyle(I,null);if(M){L=M.getPropertyValue(F)}if(F=="opacity"&&L==""){L="1"}}else{if(I.currentStyle){var J=F.replace(/\-(\w)/g,function(N,O){return O.toUpperCase()});L=I.currentStyle[F]||I.currentStyle[J];if(!/^\d+(px)?$/i.test(L)&&/^\d/.test(L)){var H=E.left,K=I.runtimeStyle.left;I.runtimeStyle.left=I.currentStyle.left;E.left=L||0;L=E.pixelLeft+"px";E.left=H;I.runtimeStyle.left=K}}}}return L},clean:function(F,K,I){K=K||document;if(typeof K.createElement==="undefined"){K=K.ownerDocument||K[0]&&K[0].ownerDocument||document}if(!I&&F.length===1&&typeof F[0]==="string"){var H=/^<(\w+)\s*\/?>$/.exec(F[0]);if(H){return[K.createElement(H[1])]}}var G=[],E=[],L=K.createElement("div");o.each(F,function(P,S){if(typeof S==="number"){S+=""}if(!S){return}if(typeof S==="string"){S=S.replace(/(<(\w+)[^>]*?)\/>/g,function(U,V,T){return T.match(/^(abbr|br|col|img|input|link|meta|param|hr|area|embed)$/i)?U:V+"></"+T+">"});var O=S.replace(/^\s+/,"").substring(0,10).toLowerCase();var Q=!O.indexOf("<opt")&&[1,"<select multiple='multiple'>","</select>"]||!O.indexOf("<leg")&&[1,"<fieldset>","</fieldset>"]||O.match(/^<(thead|tbody|tfoot|colg|cap)/)&&[1,"<table>","</table>"]||!O.indexOf("<tr")&&[2,"<table><tbody>","</tbody></table>"]||(!O.indexOf("<td")||!O.indexOf("<th"))&&[3,"<table><tbody><tr>","</tr></tbody></table>"]||!O.indexOf("<col")&&[2,"<table><tbody></tbody><colgroup>","</colgroup></table>"]||!o.support.htmlSerialize&&[1,"div<div>","</div>"]||[0,"",""];L.innerHTML=Q[1]+S+Q[2];while(Q[0]--){L=L.lastChild}if(!o.support.tbody){var R=/<tbody/i.test(S),N=!O.indexOf("<table")&&!R?L.firstChild&&L.firstChild.childNodes:Q[1]=="<table>"&&!R?L.childNodes:[];for(var M=N.length-1;M>=0;--M){if(o.nodeName(N[M],"tbody")&&!N[M].childNodes.length){N[M].parentNode.removeChild(N[M])}}}if(!o.support.leadingWhitespace&&/^\s/.test(S)){L.insertBefore(K.createTextNode(S.match(/^\s*/)[0]),L.firstChild)}S=o.makeArray(L.childNodes)}if(S.nodeType){G.push(S)}else{G=o.merge(G,S)}});if(I){for(var J=0;G[J];J++){if(o.nodeName(G[J],"script")&&(!G[J].type||G[J].type.toLowerCase()==="text/javascript")){E.push(G[J].parentNode?G[J].parentNode.removeChild(G[J]):G[J])}else{if(G[J].nodeType===1){G.splice.apply(G,[J+1,0].concat(o.makeArray(G[J].getElementsByTagName("script"))))}I.appendChild(G[J])}}return E}return G},attr:function(J,G,K){if(!J||J.nodeType==3||J.nodeType==8){return g}var H=!o.isXMLDoc(J),L=K!==g;G=H&&o.props[G]||G;if(J.tagName){var F=/href|src|style/.test(G);if(G=="selected"&&J.parentNode){J.parentNode.selectedIndex}if(G in J&&H&&!F){if(L){if(G=="type"&&o.nodeName(J,"input")&&J.parentNode){throw"type property can't be changed"}J[G]=K}if(o.nodeName(J,"form")&&J.getAttributeNode(G)){return J.getAttributeNode(G).nodeValue}if(G=="tabIndex"){var I=J.getAttributeNode("tabIndex");return I&&I.specified?I.value:J.nodeName.match(/(button|input|object|select|textarea)/i)?0:J.nodeName.match(/^(a|area)$/i)&&J.href?0:g}return J[G]}if(!o.support.style&&H&&G=="style"){return o.attr(J.style,"cssText",K)}if(L){J.setAttribute(G,""+K)}var E=!o.support.hrefNormalized&&H&&F?J.getAttribute(G,2):J.getAttribute(G);return E===null?g:E}if(!o.support.opacity&&G=="opacity"){if(L){J.zoom=1;J.filter=(J.filter||"").replace(/alpha\([^)]*\)/,"")+(parseInt(K)+""=="NaN"?"":"alpha(opacity="+K*100+")")}return J.filter&&J.filter.indexOf("opacity=")>=0?(parseFloat(J.filter.match(/opacity=([^)]*)/)[1])/100)+"":""}G=G.replace(/-([a-z])/ig,function(M,N){return N.toUpperCase()});if(L){J[G]=K}return J[G]},trim:function(E){return(E||"").replace(/^\s+|\s+$/g,"")},makeArray:function(G){var E=[];if(G!=null){var F=G.length;if(F==null||typeof G==="string"||o.isFunction(G)||G.setInterval){E[0]=G}else{while(F){E[--F]=G[F]}}}return E},inArray:function(G,H){for(var E=0,F=H.length;E<F;E++){if(H[E]===G){return E}}return -1},merge:function(H,E){var F=0,G,I=H.length;if(!o.support.getAll){while((G=E[F++])!=null){if(G.nodeType!=8){H[I++]=G}}}else{while((G=E[F++])!=null){H[I++]=G}}return H},unique:function(K){var F=[],E={};try{for(var G=0,H=K.length;G<H;G++){var J=o.data(K[G]);if(!E[J]){E[J]=true;F.push(K[G])}}}catch(I){F=K}return F},grep:function(F,J,E){var G=[];for(var H=0,I=F.length;H<I;H++){if(!E!=!J(F[H],H)){G.push(F[H])}}return G},map:function(E,J){var F=[];for(var G=0,H=E.length;G<H;G++){var I=J(E[G],G);if(I!=null){F[F.length]=I}}return F.concat.apply([],F)}});var C=navigator.userAgent.toLowerCase();o.browser={version:(C.match(/.+(?:rv|it|ra|ie)[\/: ]([\d.]+)/)||[0,"0"])[1],safari:/webkit/.test(C),opera:/opera/.test(C),msie:/msie/.test(C)&&!/opera/.test(C),mozilla:/mozilla/.test(C)&&!/(compatible|webkit)/.test(C)};o.each({parent:function(E){return E.parentNode},parents:function(E){return o.dir(E,"parentNode")},next:function(E){return o.nth(E,2,"nextSibling")},prev:function(E){return o.nth(E,2,"previousSibling")},nextAll:function(E){return o.dir(E,"nextSibling")},prevAll:function(E){return o.dir(E,"previousSibling")},siblings:function(E){return o.sibling(E.parentNode.firstChild,E)},children:function(E){return o.sibling(E.firstChild)},contents:function(E){return o.nodeName(E,"iframe")?E.contentDocument||E.contentWindow.document:o.makeArray(E.childNodes)}},function(E,F){o.fn[E]=function(G){var H=o.map(this,F);if(G&&typeof G=="string"){H=o.multiFilter(G,H)}return this.pushStack(o.unique(H),E,G)}});o.each({appendTo:"append",prependTo:"prepend",insertBefore:"before",insertAfter:"after",replaceAll:"replaceWith"},function(E,F){o.fn[E]=function(G){var J=[],L=o(G);for(var K=0,H=L.length;K<H;K++){var I=(K>0?this.clone(true):this).get();o.fn[F].apply(o(L[K]),I);J=J.concat(I)}return this.pushStack(J,E,G)}});o.each({removeAttr:function(E){o.attr(this,E,"");if(this.nodeType==1){this.removeAttribute(E)}},addClass:function(E){o.className.add(this,E)},removeClass:function(E){o.className.remove(this,E)},toggleClass:function(F,E){if(typeof E!=="boolean"){E=!o.className.has(this,F)}o.className[E?"add":"remove"](this,F)},remove:function(E){if(!E||o.filter(E,[this]).length){o("*",this).add([this]).each(function(){o.event.remove(this);o.removeData(this)});if(this.parentNode){this.parentNode.removeChild(this)}}},empty:function(){o(this).children().remove();while(this.firstChild){this.removeChild(this.firstChild)}}},function(E,F){o.fn[E]=function(){return this.each(F,arguments)}});function j(E,F){return E[0]&&parseInt(o.curCSS(E[0],F,true),10)||0}var h="jQuery"+e(),v=0,A={};o.extend({cache:{},data:function(F,E,G){F=F==l?A:F;var H=F[h];if(!H){H=F[h]=++v}if(E&&!o.cache[H]){o.cache[H]={}}if(G!==g){o.cache[H][E]=G}return E?o.cache[H][E]:H},removeData:function(F,E){F=F==l?A:F;var H=F[h];if(E){if(o.cache[H]){delete o.cache[H][E];E="";for(E in o.cache[H]){break}if(!E){o.removeData(F)}}}else{try{delete F[h]}catch(G){if(F.removeAttribute){F.removeAttribute(h)}}delete o.cache[H]}},queue:function(F,E,H){if(F){E=(E||"fx")+"queue";var G=o.data(F,E);if(!G||o.isArray(H)){G=o.data(F,E,o.makeArray(H))}else{if(H){G.push(H)}}}return G},dequeue:function(H,G){var E=o.queue(H,G),F=E.shift();if(!G||G==="fx"){F=E[0]}if(F!==g){F.call(H)}}});o.fn.extend({data:function(E,G){var H=E.split(".");H[1]=H[1]?"."+H[1]:"";if(G===g){var F=this.triggerHandler("getData"+H[1]+"!",[H[0]]);if(F===g&&this.length){F=o.data(this[0],E)}return F===g&&H[1]?this.data(H[0]):F}else{return this.trigger("setData"+H[1]+"!",[H[0],G]).each(function(){o.data(this,E,G)})}},removeData:function(E){return this.each(function(){o.removeData(this,E)})},queue:function(E,F){if(typeof E!=="string"){F=E;E="fx"}if(F===g){return o.queue(this[0],E)}return this.each(function(){var G=o.queue(this,E,F);if(E=="fx"&&G.length==1){G[0].call(this)}})},dequeue:function(E){return this.each(function(){o.dequeue(this,E)})}});
/*
 * Sizzle CSS Selector Engine - v0.9.3
 *  Copyright 2009, The Dojo Foundation
 *  Released under the MIT, BSD, and GPL Licenses.
 *  More information: http://sizzlejs.com/
 */
(function(){var R=/((?:\((?:\([^()]+\)|[^()]+)+\)|\[(?:\[[^[\]]*\]|['"][^'"]*['"]|[^[\]'"]+)+\]|\\.|[^ >+~,(\[\\]+)+|[>+~])(\s*,\s*)?/g,L=0,H=Object.prototype.toString;var F=function(Y,U,ab,ac){ab=ab||[];U=U||document;if(U.nodeType!==1&&U.nodeType!==9){return[]}if(!Y||typeof Y!=="string"){return ab}var Z=[],W,af,ai,T,ad,V,X=true;R.lastIndex=0;while((W=R.exec(Y))!==null){Z.push(W[1]);if(W[2]){V=RegExp.rightContext;break}}if(Z.length>1&&M.exec(Y)){if(Z.length===2&&I.relative[Z[0]]){af=J(Z[0]+Z[1],U)}else{af=I.relative[Z[0]]?[U]:F(Z.shift(),U);while(Z.length){Y=Z.shift();if(I.relative[Y]){Y+=Z.shift()}af=J(Y,af)}}}else{var ae=ac?{expr:Z.pop(),set:E(ac)}:F.find(Z.pop(),Z.length===1&&U.parentNode?U.parentNode:U,Q(U));af=F.filter(ae.expr,ae.set);if(Z.length>0){ai=E(af)}else{X=false}while(Z.length){var ah=Z.pop(),ag=ah;if(!I.relative[ah]){ah=""}else{ag=Z.pop()}if(ag==null){ag=U}I.relative[ah](ai,ag,Q(U))}}if(!ai){ai=af}if(!ai){throw"Syntax error, unrecognized expression: "+(ah||Y)}if(H.call(ai)==="[object Array]"){if(!X){ab.push.apply(ab,ai)}else{if(U.nodeType===1){for(var aa=0;ai[aa]!=null;aa++){if(ai[aa]&&(ai[aa]===true||ai[aa].nodeType===1&&K(U,ai[aa]))){ab.push(af[aa])}}}else{for(var aa=0;ai[aa]!=null;aa++){if(ai[aa]&&ai[aa].nodeType===1){ab.push(af[aa])}}}}}else{E(ai,ab)}if(V){F(V,U,ab,ac);if(G){hasDuplicate=false;ab.sort(G);if(hasDuplicate){for(var aa=1;aa<ab.length;aa++){if(ab[aa]===ab[aa-1]){ab.splice(aa--,1)}}}}}return ab};F.matches=function(T,U){return F(T,null,null,U)};F.find=function(aa,T,ab){var Z,X;if(!aa){return[]}for(var W=0,V=I.order.length;W<V;W++){var Y=I.order[W],X;if((X=I.match[Y].exec(aa))){var U=RegExp.leftContext;if(U.substr(U.length-1)!=="\\"){X[1]=(X[1]||"").replace(/\\/g,"");Z=I.find[Y](X,T,ab);if(Z!=null){aa=aa.replace(I.match[Y],"");break}}}}if(!Z){Z=T.getElementsByTagName("*")}return{set:Z,expr:aa}};F.filter=function(ad,ac,ag,W){var V=ad,ai=[],aa=ac,Y,T,Z=ac&&ac[0]&&Q(ac[0]);while(ad&&ac.length){for(var ab in I.filter){if((Y=I.match[ab].exec(ad))!=null){var U=I.filter[ab],ah,af;T=false;if(aa==ai){ai=[]}if(I.preFilter[ab]){Y=I.preFilter[ab](Y,aa,ag,ai,W,Z);if(!Y){T=ah=true}else{if(Y===true){continue}}}if(Y){for(var X=0;(af=aa[X])!=null;X++){if(af){ah=U(af,Y,X,aa);var ae=W^!!ah;if(ag&&ah!=null){if(ae){T=true}else{aa[X]=false}}else{if(ae){ai.push(af);T=true}}}}}if(ah!==g){if(!ag){aa=ai}ad=ad.replace(I.match[ab],"");if(!T){return[]}break}}}if(ad==V){if(T==null){throw"Syntax error, unrecognized expression: "+ad}else{break}}V=ad}return aa};var I=F.selectors={order:["ID","NAME","TAG"],match:{ID:/#((?:[\w\u00c0-\uFFFF_-]|\\.)+)/,CLASS:/\.((?:[\w\u00c0-\uFFFF_-]|\\.)+)/,NAME:/\[name=['"]*((?:[\w\u00c0-\uFFFF_-]|\\.)+)['"]*\]/,ATTR:/\[\s*((?:[\w\u00c0-\uFFFF_-]|\\.)+)\s*(?:(\S?=)\s*(['"]*)(.*?)\3|)\s*\]/,TAG:/^((?:[\w\u00c0-\uFFFF\*_-]|\\.)+)/,CHILD:/:(only|nth|last|first)-child(?:\((even|odd|[\dn+-]*)\))?/,POS:/:(nth|eq|gt|lt|first|last|even|odd)(?:\((\d*)\))?(?=[^-]|$)/,PSEUDO:/:((?:[\w\u00c0-\uFFFF_-]|\\.)+)(?:\((['"]*)((?:\([^\)]+\)|[^\2\(\)]*)+)\2\))?/},attrMap:{"class":"className","for":"htmlFor"},attrHandle:{href:function(T){return T.getAttribute("href")}},relative:{"+":function(aa,T,Z){var X=typeof T==="string",ab=X&&!/\W/.test(T),Y=X&&!ab;if(ab&&!Z){T=T.toUpperCase()}for(var W=0,V=aa.length,U;W<V;W++){if((U=aa[W])){while((U=U.previousSibling)&&U.nodeType!==1){}aa[W]=Y||U&&U.nodeName===T?U||false:U===T}}if(Y){F.filter(T,aa,true)}},">":function(Z,U,aa){var X=typeof U==="string";if(X&&!/\W/.test(U)){U=aa?U:U.toUpperCase();for(var V=0,T=Z.length;V<T;V++){var Y=Z[V];if(Y){var W=Y.parentNode;Z[V]=W.nodeName===U?W:false}}}else{for(var V=0,T=Z.length;V<T;V++){var Y=Z[V];if(Y){Z[V]=X?Y.parentNode:Y.parentNode===U}}if(X){F.filter(U,Z,true)}}},"":function(W,U,Y){var V=L++,T=S;if(!U.match(/\W/)){var X=U=Y?U:U.toUpperCase();T=P}T("parentNode",U,V,W,X,Y)},"~":function(W,U,Y){var V=L++,T=S;if(typeof U==="string"&&!U.match(/\W/)){var X=U=Y?U:U.toUpperCase();T=P}T("previousSibling",U,V,W,X,Y)}},find:{ID:function(U,V,W){if(typeof V.getElementById!=="undefined"&&!W){var T=V.getElementById(U[1]);return T?[T]:[]}},NAME:function(V,Y,Z){if(typeof Y.getElementsByName!=="undefined"){var U=[],X=Y.getElementsByName(V[1]);for(var W=0,T=X.length;W<T;W++){if(X[W].getAttribute("name")===V[1]){U.push(X[W])}}return U.length===0?null:U}},TAG:function(T,U){return U.getElementsByTagName(T[1])}},preFilter:{CLASS:function(W,U,V,T,Z,aa){W=" "+W[1].replace(/\\/g,"")+" ";if(aa){return W}for(var X=0,Y;(Y=U[X])!=null;X++){if(Y){if(Z^(Y.className&&(" "+Y.className+" ").indexOf(W)>=0)){if(!V){T.push(Y)}}else{if(V){U[X]=false}}}}return false},ID:function(T){return T[1].replace(/\\/g,"")},TAG:function(U,T){for(var V=0;T[V]===false;V++){}return T[V]&&Q(T[V])?U[1]:U[1].toUpperCase()},CHILD:function(T){if(T[1]=="nth"){var U=/(-?)(\d*)n((?:\+|-)?\d*)/.exec(T[2]=="even"&&"2n"||T[2]=="odd"&&"2n+1"||!/\D/.test(T[2])&&"0n+"+T[2]||T[2]);T[2]=(U[1]+(U[2]||1))-0;T[3]=U[3]-0}T[0]=L++;return T},ATTR:function(X,U,V,T,Y,Z){var W=X[1].replace(/\\/g,"");if(!Z&&I.attrMap[W]){X[1]=I.attrMap[W]}if(X[2]==="~="){X[4]=" "+X[4]+" "}return X},PSEUDO:function(X,U,V,T,Y){if(X[1]==="not"){if(X[3].match(R).length>1||/^\w/.test(X[3])){X[3]=F(X[3],null,null,U)}else{var W=F.filter(X[3],U,V,true^Y);if(!V){T.push.apply(T,W)}return false}}else{if(I.match.POS.test(X[0])||I.match.CHILD.test(X[0])){return true}}return X},POS:function(T){T.unshift(true);return T}},filters:{enabled:function(T){return T.disabled===false&&T.type!=="hidden"},disabled:function(T){return T.disabled===true},checked:function(T){return T.checked===true},selected:function(T){T.parentNode.selectedIndex;return T.selected===true},parent:function(T){return !!T.firstChild},empty:function(T){return !T.firstChild},has:function(V,U,T){return !!F(T[3],V).length},header:function(T){return/h\d/i.test(T.nodeName)},text:function(T){return"text"===T.type},radio:function(T){return"radio"===T.type},checkbox:function(T){return"checkbox"===T.type},file:function(T){return"file"===T.type},password:function(T){return"password"===T.type},submit:function(T){return"submit"===T.type},image:function(T){return"image"===T.type},reset:function(T){return"reset"===T.type},button:function(T){return"button"===T.type||T.nodeName.toUpperCase()==="BUTTON"},input:function(T){return/input|select|textarea|button/i.test(T.nodeName)}},setFilters:{first:function(U,T){return T===0},last:function(V,U,T,W){return U===W.length-1},even:function(U,T){return T%2===0},odd:function(U,T){return T%2===1},lt:function(V,U,T){return U<T[3]-0},gt:function(V,U,T){return U>T[3]-0},nth:function(V,U,T){return T[3]-0==U},eq:function(V,U,T){return T[3]-0==U}},filter:{PSEUDO:function(Z,V,W,aa){var U=V[1],X=I.filters[U];if(X){return X(Z,W,V,aa)}else{if(U==="contains"){return(Z.textContent||Z.innerText||"").indexOf(V[3])>=0}else{if(U==="not"){var Y=V[3];for(var W=0,T=Y.length;W<T;W++){if(Y[W]===Z){return false}}return true}}}},CHILD:function(T,W){var Z=W[1],U=T;switch(Z){case"only":case"first":while(U=U.previousSibling){if(U.nodeType===1){return false}}if(Z=="first"){return true}U=T;case"last":while(U=U.nextSibling){if(U.nodeType===1){return false}}return true;case"nth":var V=W[2],ac=W[3];if(V==1&&ac==0){return true}var Y=W[0],ab=T.parentNode;if(ab&&(ab.sizcache!==Y||!T.nodeIndex)){var X=0;for(U=ab.firstChild;U;U=U.nextSibling){if(U.nodeType===1){U.nodeIndex=++X}}ab.sizcache=Y}var aa=T.nodeIndex-ac;if(V==0){return aa==0}else{return(aa%V==0&&aa/V>=0)}}},ID:function(U,T){return U.nodeType===1&&U.getAttribute("id")===T},TAG:function(U,T){return(T==="*"&&U.nodeType===1)||U.nodeName===T},CLASS:function(U,T){return(" "+(U.className||U.getAttribute("class"))+" ").indexOf(T)>-1},ATTR:function(Y,W){var V=W[1],T=I.attrHandle[V]?I.attrHandle[V](Y):Y[V]!=null?Y[V]:Y.getAttribute(V),Z=T+"",X=W[2],U=W[4];return T==null?X==="!=":X==="="?Z===U:X==="*="?Z.indexOf(U)>=0:X==="~="?(" "+Z+" ").indexOf(U)>=0:!U?Z&&T!==false:X==="!="?Z!=U:X==="^="?Z.indexOf(U)===0:X==="$="?Z.substr(Z.length-U.length)===U:X==="|="?Z===U||Z.substr(0,U.length+1)===U+"-":false},POS:function(X,U,V,Y){var T=U[2],W=I.setFilters[T];if(W){return W(X,V,U,Y)}}}};var M=I.match.POS;for(var O in I.match){I.match[O]=RegExp(I.match[O].source+/(?![^\[]*\])(?![^\(]*\))/.source)}var E=function(U,T){U=Array.prototype.slice.call(U);if(T){T.push.apply(T,U);return T}return U};try{Array.prototype.slice.call(document.documentElement.childNodes)}catch(N){E=function(X,W){var U=W||[];if(H.call(X)==="[object Array]"){Array.prototype.push.apply(U,X)}else{if(typeof X.length==="number"){for(var V=0,T=X.length;V<T;V++){U.push(X[V])}}else{for(var V=0;X[V];V++){U.push(X[V])}}}return U}}var G;if(document.documentElement.compareDocumentPosition){G=function(U,T){var V=U.compareDocumentPosition(T)&4?-1:U===T?0:1;if(V===0){hasDuplicate=true}return V}}else{if("sourceIndex" in document.documentElement){G=function(U,T){var V=U.sourceIndex-T.sourceIndex;if(V===0){hasDuplicate=true}return V}}else{if(document.createRange){G=function(W,U){var V=W.ownerDocument.createRange(),T=U.ownerDocument.createRange();V.selectNode(W);V.collapse(true);T.selectNode(U);T.collapse(true);var X=V.compareBoundaryPoints(Range.START_TO_END,T);if(X===0){hasDuplicate=true}return X}}}}(function(){var U=document.createElement("form"),V="script"+(new Date).getTime();U.innerHTML="<input name='"+V+"'/>";var T=document.documentElement;T.insertBefore(U,T.firstChild);if(!!document.getElementById(V)){I.find.ID=function(X,Y,Z){if(typeof Y.getElementById!=="undefined"&&!Z){var W=Y.getElementById(X[1]);return W?W.id===X[1]||typeof W.getAttributeNode!=="undefined"&&W.getAttributeNode("id").nodeValue===X[1]?[W]:g:[]}};I.filter.ID=function(Y,W){var X=typeof Y.getAttributeNode!=="undefined"&&Y.getAttributeNode("id");return Y.nodeType===1&&X&&X.nodeValue===W}}T.removeChild(U)})();(function(){var T=document.createElement("div");T.appendChild(document.createComment(""));if(T.getElementsByTagName("*").length>0){I.find.TAG=function(U,Y){var X=Y.getElementsByTagName(U[1]);if(U[1]==="*"){var W=[];for(var V=0;X[V];V++){if(X[V].nodeType===1){W.push(X[V])}}X=W}return X}}T.innerHTML="<a href='#'></a>";if(T.firstChild&&typeof T.firstChild.getAttribute!=="undefined"&&T.firstChild.getAttribute("href")!=="#"){I.attrHandle.href=function(U){return U.getAttribute("href",2)}}})();if(document.querySelectorAll){(function(){var T=F,U=document.createElement("div");U.innerHTML="<p class='TEST'></p>";if(U.querySelectorAll&&U.querySelectorAll(".TEST").length===0){return}F=function(Y,X,V,W){X=X||document;if(!W&&X.nodeType===9&&!Q(X)){try{return E(X.querySelectorAll(Y),V)}catch(Z){}}return T(Y,X,V,W)};F.find=T.find;F.filter=T.filter;F.selectors=T.selectors;F.matches=T.matches})()}if(document.getElementsByClassName&&document.documentElement.getElementsByClassName){(function(){var T=document.createElement("div");T.innerHTML="<div class='test e'></div><div class='test'></div>";if(T.getElementsByClassName("e").length===0){return}T.lastChild.className="e";if(T.getElementsByClassName("e").length===1){return}I.order.splice(1,0,"CLASS");I.find.CLASS=function(U,V,W){if(typeof V.getElementsByClassName!=="undefined"&&!W){return V.getElementsByClassName(U[1])}}})()}function P(U,Z,Y,ad,aa,ac){var ab=U=="previousSibling"&&!ac;for(var W=0,V=ad.length;W<V;W++){var T=ad[W];if(T){if(ab&&T.nodeType===1){T.sizcache=Y;T.sizset=W}T=T[U];var X=false;while(T){if(T.sizcache===Y){X=ad[T.sizset];break}if(T.nodeType===1&&!ac){T.sizcache=Y;T.sizset=W}if(T.nodeName===Z){X=T;break}T=T[U]}ad[W]=X}}}function S(U,Z,Y,ad,aa,ac){var ab=U=="previousSibling"&&!ac;for(var W=0,V=ad.length;W<V;W++){var T=ad[W];if(T){if(ab&&T.nodeType===1){T.sizcache=Y;T.sizset=W}T=T[U];var X=false;while(T){if(T.sizcache===Y){X=ad[T.sizset];break}if(T.nodeType===1){if(!ac){T.sizcache=Y;T.sizset=W}if(typeof Z!=="string"){if(T===Z){X=true;break}}else{if(F.filter(Z,[T]).length>0){X=T;break}}}T=T[U]}ad[W]=X}}}var K=document.compareDocumentPosition?function(U,T){return U.compareDocumentPosition(T)&16}:function(U,T){return U!==T&&(U.contains?U.contains(T):true)};var Q=function(T){return T.nodeType===9&&T.documentElement.nodeName!=="HTML"||!!T.ownerDocument&&Q(T.ownerDocument)};var J=function(T,aa){var W=[],X="",Y,V=aa.nodeType?[aa]:aa;while((Y=I.match.PSEUDO.exec(T))){X+=Y[0];T=T.replace(I.match.PSEUDO,"")}T=I.relative[T]?T+"*":T;for(var Z=0,U=V.length;Z<U;Z++){F(T,V[Z],W)}return F.filter(X,W)};o.find=F;o.filter=F.filter;o.expr=F.selectors;o.expr[":"]=o.expr.filters;F.selectors.filters.hidden=function(T){return T.offsetWidth===0||T.offsetHeight===0};F.selectors.filters.visible=function(T){return T.offsetWidth>0||T.offsetHeight>0};F.selectors.filters.animated=function(T){return o.grep(o.timers,function(U){return T===U.elem}).length};o.multiFilter=function(V,T,U){if(U){V=":not("+V+")"}return F.matches(V,T)};o.dir=function(V,U){var T=[],W=V[U];while(W&&W!=document){if(W.nodeType==1){T.push(W)}W=W[U]}return T};o.nth=function(X,T,V,W){T=T||1;var U=0;for(;X;X=X[V]){if(X.nodeType==1&&++U==T){break}}return X};o.sibling=function(V,U){var T=[];for(;V;V=V.nextSibling){if(V.nodeType==1&&V!=U){T.push(V)}}return T};return;l.Sizzle=F})();o.event={add:function(I,F,H,K){if(I.nodeType==3||I.nodeType==8){return}if(I.setInterval&&I!=l){I=l}if(!H.guid){H.guid=this.guid++}if(K!==g){var G=H;H=this.proxy(G);H.data=K}var E=o.data(I,"events")||o.data(I,"events",{}),J=o.data(I,"handle")||o.data(I,"handle",function(){return typeof o!=="undefined"&&!o.event.triggered?o.event.handle.apply(arguments.callee.elem,arguments):g});J.elem=I;o.each(F.split(/\s+/),function(M,N){var O=N.split(".");N=O.shift();H.type=O.slice().sort().join(".");var L=E[N];if(o.event.specialAll[N]){o.event.specialAll[N].setup.call(I,K,O)}if(!L){L=E[N]={};if(!o.event.special[N]||o.event.special[N].setup.call(I,K,O)===false){if(I.addEventListener){I.addEventListener(N,J,false)}else{if(I.attachEvent){I.attachEvent("on"+N,J)}}}}L[H.guid]=H;o.event.global[N]=true});I=null},guid:1,global:{},remove:function(K,H,J){if(K.nodeType==3||K.nodeType==8){return}var G=o.data(K,"events"),F,E;if(G){if(H===g||(typeof H==="string"&&H.charAt(0)==".")){for(var I in G){this.remove(K,I+(H||""))}}else{if(H.type){J=H.handler;H=H.type}o.each(H.split(/\s+/),function(M,O){var Q=O.split(".");O=Q.shift();var N=RegExp("(^|\\.)"+Q.slice().sort().join(".*\\.")+"(\\.|$)");if(G[O]){if(J){delete G[O][J.guid]}else{for(var P in G[O]){if(N.test(G[O][P].type)){delete G[O][P]}}}if(o.event.specialAll[O]){o.event.specialAll[O].teardown.call(K,Q)}for(F in G[O]){break}if(!F){if(!o.event.special[O]||o.event.special[O].teardown.call(K,Q)===false){if(K.removeEventListener){K.removeEventListener(O,o.data(K,"handle"),false)}else{if(K.detachEvent){K.detachEvent("on"+O,o.data(K,"handle"))}}}F=null;delete G[O]}}})}for(F in G){break}if(!F){var L=o.data(K,"handle");if(L){L.elem=null}o.removeData(K,"events");o.removeData(K,"handle")}}},trigger:function(I,K,H,E){var G=I.type||I;if(!E){I=typeof I==="object"?I[h]?I:o.extend(o.Event(G),I):o.Event(G);if(G.indexOf("!")>=0){I.type=G=G.slice(0,-1);I.exclusive=true}if(!H){I.stopPropagation();if(this.global[G]){o.each(o.cache,function(){if(this.events&&this.events[G]){o.event.trigger(I,K,this.handle.elem)}})}}if(!H||H.nodeType==3||H.nodeType==8){return g}I.result=g;I.target=H;K=o.makeArray(K);K.unshift(I)}I.currentTarget=H;var J=o.data(H,"handle");if(J){J.apply(H,K)}if((!H[G]||(o.nodeName(H,"a")&&G=="click"))&&H["on"+G]&&H["on"+G].apply(H,K)===false){I.result=false}if(!E&&H[G]&&!I.isDefaultPrevented()&&!(o.nodeName(H,"a")&&G=="click")){this.triggered=true;try{H[G]()}catch(L){}}this.triggered=false;if(!I.isPropagationStopped()){var F=H.parentNode||H.ownerDocument;if(F){o.event.trigger(I,K,F,true)}}},handle:function(K){var J,E;K=arguments[0]=o.event.fix(K||l.event);K.currentTarget=this;var L=K.type.split(".");K.type=L.shift();J=!L.length&&!K.exclusive;var I=RegExp("(^|\\.)"+L.slice().sort().join(".*\\.")+"(\\.|$)");E=(o.data(this,"events")||{})[K.type];for(var G in E){var H=E[G];if(J||I.test(H.type)){K.handler=H;K.data=H.data;var F=H.apply(this,arguments);if(F!==g){K.result=F;if(F===false){K.preventDefault();K.stopPropagation()}}if(K.isImmediatePropagationStopped()){break}}}},props:"altKey attrChange attrName bubbles button cancelable charCode clientX clientY ctrlKey currentTarget data detail eventPhase fromElement handler keyCode metaKey newValue originalTarget pageX pageY prevValue relatedNode relatedTarget screenX screenY shiftKey srcElement target toElement view wheelDelta which".split(" "),fix:function(H){if(H[h]){return H}var F=H;H=o.Event(F);for(var G=this.props.length,J;G;){J=this.props[--G];H[J]=F[J]}if(!H.target){H.target=H.srcElement||document}if(H.target.nodeType==3){H.target=H.target.parentNode}if(!H.relatedTarget&&H.fromElement){H.relatedTarget=H.fromElement==H.target?H.toElement:H.fromElement}if(H.pageX==null&&H.clientX!=null){var I=document.documentElement,E=document.body;H.pageX=H.clientX+(I&&I.scrollLeft||E&&E.scrollLeft||0)-(I.clientLeft||0);H.pageY=H.clientY+(I&&I.scrollTop||E&&E.scrollTop||0)-(I.clientTop||0)}if(!H.which&&((H.charCode||H.charCode===0)?H.charCode:H.keyCode)){H.which=H.charCode||H.keyCode}if(!H.metaKey&&H.ctrlKey){H.metaKey=H.ctrlKey}if(!H.which&&H.button){H.which=(H.button&1?1:(H.button&2?3:(H.button&4?2:0)))}return H},proxy:function(F,E){E=E||function(){return F.apply(this,arguments)};E.guid=F.guid=F.guid||E.guid||this.guid++;return E},special:{ready:{setup:B,teardown:function(){}}},specialAll:{live:{setup:function(E,F){o.event.add(this,F[0],c)},teardown:function(G){if(G.length){var E=0,F=RegExp("(^|\\.)"+G[0]+"(\\.|$)");o.each((o.data(this,"events").live||{}),function(){if(F.test(this.type)){E++}});if(E<1){o.event.remove(this,G[0],c)}}}}}};o.Event=function(E){if(!this.preventDefault){return new o.Event(E)}if(E&&E.type){this.originalEvent=E;this.type=E.type}else{this.type=E}this.timeStamp=e();this[h]=true};function k(){return false}function u(){return true}o.Event.prototype={preventDefault:function(){this.isDefaultPrevented=u;var E=this.originalEvent;if(!E){return}if(E.preventDefault){E.preventDefault()}E.returnValue=false},stopPropagation:function(){this.isPropagationStopped=u;var E=this.originalEvent;if(!E){return}if(E.stopPropagation){E.stopPropagation()}E.cancelBubble=true},stopImmediatePropagation:function(){this.isImmediatePropagationStopped=u;this.stopPropagation()},isDefaultPrevented:k,isPropagationStopped:k,isImmediatePropagationStopped:k};var a=function(F){var E=F.relatedTarget;while(E&&E!=this){try{E=E.parentNode}catch(G){E=this}}if(E!=this){F.type=F.data;o.event.handle.apply(this,arguments)}};o.each({mouseover:"mouseenter",mouseout:"mouseleave"},function(F,E){o.event.special[E]={setup:function(){o.event.add(this,F,a,E)},teardown:function(){o.event.remove(this,F,a)}}});o.fn.extend({bind:function(F,G,E){return F=="unload"?this.one(F,G,E):this.each(function(){o.event.add(this,F,E||G,E&&G)})},one:function(G,H,F){var E=o.event.proxy(F||H,function(I){o(this).unbind(I,E);return(F||H).apply(this,arguments)});return this.each(function(){o.event.add(this,G,E,F&&H)})},unbind:function(F,E){return this.each(function(){o.event.remove(this,F,E)})},trigger:function(E,F){return this.each(function(){o.event.trigger(E,F,this)})},triggerHandler:function(E,G){if(this[0]){var F=o.Event(E);F.preventDefault();F.stopPropagation();o.event.trigger(F,G,this[0]);return F.result}},toggle:function(G){var E=arguments,F=1;while(F<E.length){o.event.proxy(G,E[F++])}return this.click(o.event.proxy(G,function(H){this.lastToggle=(this.lastToggle||0)%F;H.preventDefault();return E[this.lastToggle++].apply(this,arguments)||false}))},hover:function(E,F){return this.mouseenter(E).mouseleave(F)},ready:function(E){B();if(o.isReady){E.call(document,o)}else{o.readyList.push(E)}return this},live:function(G,F){var E=o.event.proxy(F);E.guid+=this.selector+G;o(document).bind(i(G,this.selector),this.selector,E);return this},die:function(F,E){o(document).unbind(i(F,this.selector),E?{guid:E.guid+this.selector+F}:null);return this}});function c(H){var E=RegExp("(^|\\.)"+H.type+"(\\.|$)"),G=true,F=[];o.each(o.data(this,"events").live||[],function(I,J){if(E.test(J.type)){var K=o(H.target).closest(J.data)[0];if(K){F.push({elem:K,fn:J})}}});F.sort(function(J,I){return o.data(J.elem,"closest")-o.data(I.elem,"closest")});o.each(F,function(){if(this.fn.call(this.elem,H,this.fn.data)===false){return(G=false)}});return G}function i(F,E){return["live",F,E.replace(/\./g,"`").replace(/ /g,"|")].join(".")}o.extend({isReady:false,readyList:[],ready:function(){if(!o.isReady){o.isReady=true;if(o.readyList){o.each(o.readyList,function(){this.call(document,o)});o.readyList=null}o(document).triggerHandler("ready")}}});var x=false;function B(){if(x){return}x=true;if(document.addEventListener){document.addEventListener("DOMContentLoaded",function(){document.removeEventListener("DOMContentLoaded",arguments.callee,false);o.ready()},false)}else{if(document.attachEvent){document.attachEvent("onreadystatechange",function(){if(document.readyState==="complete"){document.detachEvent("onreadystatechange",arguments.callee);o.ready()}});if(document.documentElement.doScroll&&l==l.top){(function(){if(o.isReady){return}try{document.documentElement.doScroll("left")}catch(E){setTimeout(arguments.callee,0);return}o.ready()})()}}}o.event.add(l,"load",o.ready)}o.each(("blur,focus,load,resize,scroll,unload,click,dblclick,mousedown,mouseup,mousemove,mouseover,mouseout,mouseenter,mouseleave,change,select,submit,keydown,keypress,keyup,error").split(","),function(F,E){o.fn[E]=function(G){return G?this.bind(E,G):this.trigger(E)}});o(l).bind("unload",function(){for(var E in o.cache){if(E!=1&&o.cache[E].handle){o.event.remove(o.cache[E].handle.elem)}}});(function(){o.support={};var F=document.documentElement,G=document.createElement("script"),K=document.createElement("div"),J="script"+(new Date).getTime();K.style.display="none";K.innerHTML='   <link/><table></table><a href="/a" style="color:red;float:left;opacity:.5;">a</a><select><option>text</option></select><object><param/></object>';var H=K.getElementsByTagName("*"),E=K.getElementsByTagName("a")[0];if(!H||!H.length||!E){return}o.support={leadingWhitespace:K.firstChild.nodeType==3,tbody:!K.getElementsByTagName("tbody").length,objectAll:!!K.getElementsByTagName("object")[0].getElementsByTagName("*").length,htmlSerialize:!!K.getElementsByTagName("link").length,style:/red/.test(E.getAttribute("style")),hrefNormalized:E.getAttribute("href")==="/a",opacity:E.style.opacity==="0.5",cssFloat:!!E.style.cssFloat,scriptEval:false,noCloneEvent:true,boxModel:null};G.type="text/javascript";try{G.appendChild(document.createTextNode("window."+J+"=1;"))}catch(I){}F.insertBefore(G,F.firstChild);if(l[J]){o.support.scriptEval=true;delete l[J]}F.removeChild(G);if(K.attachEvent&&K.fireEvent){K.attachEvent("onclick",function(){o.support.noCloneEvent=false;K.detachEvent("onclick",arguments.callee)});K.cloneNode(true).fireEvent("onclick")}o(function(){var L=document.createElement("div");L.style.width=L.style.paddingLeft="1px";document.body.appendChild(L);o.boxModel=o.support.boxModel=L.offsetWidth===2;document.body.removeChild(L).style.display="none"})})();var w=o.support.cssFloat?"cssFloat":"styleFloat";o.props={"for":"htmlFor","class":"className","float":w,cssFloat:w,styleFloat:w,readonly:"readOnly",maxlength:"maxLength",cellspacing:"cellSpacing",rowspan:"rowSpan",tabindex:"tabIndex"};o.fn.extend({_load:o.fn.load,load:function(G,J,K){if(typeof G!=="string"){return this._load(G)}var I=G.indexOf(" ");if(I>=0){var E=G.slice(I,G.length);G=G.slice(0,I)}var H="GET";if(J){if(o.isFunction(J)){K=J;J=null}else{if(typeof J==="object"){J=o.param(J);H="POST"}}}var F=this;o.ajax({url:G,type:H,dataType:"html",data:J,complete:function(M,L){if(L=="success"||L=="notmodified"){F.html(E?o("<div/>").append(M.responseText.replace(/<script(.|\s)*?\/script>/g,"")).find(E):M.responseText)}if(K){F.each(K,[M.responseText,L,M])}}});return this},serialize:function(){return o.param(this.serializeArray())},serializeArray:function(){return this.map(function(){return this.elements?o.makeArray(this.elements):this}).filter(function(){return this.name&&!this.disabled&&(this.checked||/select|textarea/i.test(this.nodeName)||/text|hidden|password|search/i.test(this.type))}).map(function(E,F){var G=o(this).val();return G==null?null:o.isArray(G)?o.map(G,function(I,H){return{name:F.name,value:I}}):{name:F.name,value:G}}).get()}});o.each("ajaxStart,ajaxStop,ajaxComplete,ajaxError,ajaxSuccess,ajaxSend".split(","),function(E,F){o.fn[F]=function(G){return this.bind(F,G)}});var r=e();o.extend({get:function(E,G,H,F){if(o.isFunction(G)){H=G;G=null}return o.ajax({type:"GET",url:E,data:G,success:H,dataType:F})},getScript:function(E,F){return o.get(E,null,F,"script")},getJSON:function(E,F,G){return o.get(E,F,G,"json")},post:function(E,G,H,F){if(o.isFunction(G)){H=G;G={}}return o.ajax({type:"POST",url:E,data:G,success:H,dataType:F})},ajaxSetup:function(E){o.extend(o.ajaxSettings,E)},ajaxSettings:{url:location.href,global:true,type:"GET",contentType:"application/x-www-form-urlencoded",processData:true,async:true,xhr:function(){return l.ActiveXObject?new ActiveXObject("Microsoft.XMLHTTP"):new XMLHttpRequest()},accepts:{xml:"application/xml, text/xml",html:"text/html",script:"text/javascript, application/javascript",json:"application/json, text/javascript",text:"text/plain",_default:"*/*"}},lastModified:{},ajax:function(M){M=o.extend(true,M,o.extend(true,{},o.ajaxSettings,M));var W,F=/=\?(&|$)/g,R,V,G=M.type.toUpperCase();if(M.data&&M.processData&&typeof M.data!=="string"){M.data=o.param(M.data)}if(M.dataType=="jsonp"){if(G=="GET"){if(!M.url.match(F)){M.url+=(M.url.match(/\?/)?"&":"?")+(M.jsonp||"callback")+"=?"}}else{if(!M.data||!M.data.match(F)){M.data=(M.data?M.data+"&":"")+(M.jsonp||"callback")+"=?"}}M.dataType="json"}if(M.dataType=="json"&&(M.data&&M.data.match(F)||M.url.match(F))){W="jsonp"+r++;if(M.data){M.data=(M.data+"").replace(F,"="+W+"$1")}M.url=M.url.replace(F,"="+W+"$1");M.dataType="script";l[W]=function(X){V=X;I();L();l[W]=g;try{delete l[W]}catch(Y){}if(H){H.removeChild(T)}}}if(M.dataType=="script"&&M.cache==null){M.cache=false}if(M.cache===false&&G=="GET"){var E=e();var U=M.url.replace(/(\?|&)_=.*?(&|$)/,"$1_="+E+"$2");M.url=U+((U==M.url)?(M.url.match(/\?/)?"&":"?")+"_="+E:"")}if(M.data&&G=="GET"){M.url+=(M.url.match(/\?/)?"&":"?")+M.data;M.data=null}if(M.global&&!o.active++){o.event.trigger("ajaxStart")}var Q=/^(\w+:)?\/\/([^\/?#]+)/.exec(M.url);if(M.dataType=="script"&&G=="GET"&&Q&&(Q[1]&&Q[1]!=location.protocol||Q[2]!=location.host)){var H=document.getElementsByTagName("head")[0];var T=document.createElement("script");T.src=M.url;if(M.scriptCharset){T.charset=M.scriptCharset}if(!W){var O=false;T.onload=T.onreadystatechange=function(){if(!O&&(!this.readyState||this.readyState=="loaded"||this.readyState=="complete")){O=true;I();L();T.onload=T.onreadystatechange=null;H.removeChild(T)}}}H.appendChild(T);return g}var K=false;var J=M.xhr();if(M.username){J.open(G,M.url,M.async,M.username,M.password)}else{J.open(G,M.url,M.async)}try{if(M.data){J.setRequestHeader("Content-Type",M.contentType)}if(M.ifModified){J.setRequestHeader("If-Modified-Since",o.lastModified[M.url]||"Thu, 01 Jan 1970 00:00:00 GMT")}J.setRequestHeader("X-Requested-With","XMLHttpRequest");J.setRequestHeader("Accept",M.dataType&&M.accepts[M.dataType]?M.accepts[M.dataType]+", */*":M.accepts._default)}catch(S){}if(M.beforeSend&&M.beforeSend(J,M)===false){if(M.global&&!--o.active){o.event.trigger("ajaxStop")}J.abort();return false}if(M.global){o.event.trigger("ajaxSend",[J,M])}var N=function(X){if(J.readyState==0){if(P){clearInterval(P);P=null;if(M.global&&!--o.active){o.event.trigger("ajaxStop")}}}else{if(!K&&J&&(J.readyState==4||X=="timeout")){K=true;if(P){clearInterval(P);P=null}R=X=="timeout"?"timeout":!o.httpSuccess(J)?"error":M.ifModified&&o.httpNotModified(J,M.url)?"notmodified":"success";if(R=="success"){try{V=o.httpData(J,M.dataType,M)}catch(Z){R="parsererror"}}if(R=="success"){var Y;try{Y=J.getResponseHeader("Last-Modified")}catch(Z){}if(M.ifModified&&Y){o.lastModified[M.url]=Y}if(!W){I()}}else{o.handleError(M,J,R)}L();if(X){J.abort()}if(M.async){J=null}}}};if(M.async){var P=setInterval(N,13);if(M.timeout>0){setTimeout(function(){if(J&&!K){N("timeout")}},M.timeout)}}try{J.send(M.data)}catch(S){o.handleError(M,J,null,S)}if(!M.async){N()}function I(){if(M.success){M.success(V,R)}if(M.global){o.event.trigger("ajaxSuccess",[J,M])}}function L(){if(M.complete){M.complete(J,R)}if(M.global){o.event.trigger("ajaxComplete",[J,M])}if(M.global&&!--o.active){o.event.trigger("ajaxStop")}}return J},handleError:function(F,H,E,G){if(F.error){F.error(H,E,G)}if(F.global){o.event.trigger("ajaxError",[H,F,G])}},active:0,httpSuccess:function(F){try{return !F.status&&location.protocol=="file:"||(F.status>=200&&F.status<300)||F.status==304||F.status==1223}catch(E){}return false},httpNotModified:function(G,E){try{var H=G.getResponseHeader("Last-Modified");return G.status==304||H==o.lastModified[E]}catch(F){}return false},httpData:function(J,H,G){var F=J.getResponseHeader("content-type"),E=H=="xml"||!H&&F&&F.indexOf("xml")>=0,I=E?J.responseXML:J.responseText;if(E&&I.documentElement.tagName=="parsererror"){throw"parsererror"}if(G&&G.dataFilter){I=G.dataFilter(I,H)}if(typeof I==="string"){if(H=="script"){o.globalEval(I)}if(H=="json"){I=l["eval"]("("+I+")")}}return I},param:function(E){var G=[];function H(I,J){G[G.length]=encodeURIComponent(I)+"="+encodeURIComponent(J)}if(o.isArray(E)||E.jquery){o.each(E,function(){H(this.name,this.value)})}else{for(var F in E){if(o.isArray(E[F])){o.each(E[F],function(){H(F,this)})}else{H(F,o.isFunction(E[F])?E[F]():E[F])}}}return G.join("&").replace(/%20/g,"+")}});var m={},n,d=[["height","marginTop","marginBottom","paddingTop","paddingBottom"],["width","marginLeft","marginRight","paddingLeft","paddingRight"],["opacity"]];function t(F,E){var G={};o.each(d.concat.apply([],d.slice(0,E)),function(){G[this]=F});return G}o.fn.extend({show:function(J,L){if(J){return this.animate(t("show",3),J,L)}else{for(var H=0,F=this.length;H<F;H++){var E=o.data(this[H],"olddisplay");this[H].style.display=E||"";if(o.css(this[H],"display")==="none"){var G=this[H].tagName,K;if(m[G]){K=m[G]}else{var I=o("<"+G+" />").appendTo("body");K=I.css("display");if(K==="none"){K="block"}I.remove();m[G]=K}o.data(this[H],"olddisplay",K)}}for(var H=0,F=this.length;H<F;H++){this[H].style.display=o.data(this[H],"olddisplay")||""}return this}},hide:function(H,I){if(H){return this.animate(t("hide",3),H,I)}else{for(var G=0,F=this.length;G<F;G++){var E=o.data(this[G],"olddisplay");if(!E&&E!=="none"){o.data(this[G],"olddisplay",o.css(this[G],"display"))}}for(var G=0,F=this.length;G<F;G++){this[G].style.display="none"}return this}},_toggle:o.fn.toggle,toggle:function(G,F){var E=typeof G==="boolean";return o.isFunction(G)&&o.isFunction(F)?this._toggle.apply(this,arguments):G==null||E?this.each(function(){var H=E?G:o(this).is(":hidden");o(this)[H?"show":"hide"]()}):this.animate(t("toggle",3),G,F)},fadeTo:function(E,G,F){return this.animate({opacity:G},E,F)},animate:function(I,F,H,G){var E=o.speed(F,H,G);return this[E.queue===false?"each":"queue"](function(){var K=o.extend({},E),M,L=this.nodeType==1&&o(this).is(":hidden"),J=this;for(M in I){if(I[M]=="hide"&&L||I[M]=="show"&&!L){return K.complete.call(this)}if((M=="height"||M=="width")&&this.style){K.display=o.css(this,"display");K.overflow=this.style.overflow}}if(K.overflow!=null){this.style.overflow="hidden"}K.curAnim=o.extend({},I);o.each(I,function(O,S){var R=new o.fx(J,K,O);if(/toggle|show|hide/.test(S)){R[S=="toggle"?L?"show":"hide":S](I)}else{var Q=S.toString().match(/^([+-]=)?([\d+-.]+)(.*)$/),T=R.cur(true)||0;if(Q){var N=parseFloat(Q[2]),P=Q[3]||"px";if(P!="px"){J.style[O]=(N||1)+P;T=((N||1)/R.cur(true))*T;J.style[O]=T+P}if(Q[1]){N=((Q[1]=="-="?-1:1)*N)+T}R.custom(T,N,P)}else{R.custom(T,S,"")}}});return true})},stop:function(F,E){var G=o.timers;if(F){this.queue([])}this.each(function(){for(var H=G.length-1;H>=0;H--){if(G[H].elem==this){if(E){G[H](true)}G.splice(H,1)}}});if(!E){this.dequeue()}return this}});o.each({slideDown:t("show",1),slideUp:t("hide",1),slideToggle:t("toggle",1),fadeIn:{opacity:"show"},fadeOut:{opacity:"hide"}},function(E,F){o.fn[E]=function(G,H){return this.animate(F,G,H)}});o.extend({speed:function(G,H,F){var E=typeof G==="object"?G:{complete:F||!F&&H||o.isFunction(G)&&G,duration:G,easing:F&&H||H&&!o.isFunction(H)&&H};E.duration=o.fx.off?0:typeof E.duration==="number"?E.duration:o.fx.speeds[E.duration]||o.fx.speeds._default;E.old=E.complete;E.complete=function(){if(E.queue!==false){o(this).dequeue()}if(o.isFunction(E.old)){E.old.call(this)}};return E},easing:{linear:function(G,H,E,F){return E+F*G},swing:function(G,H,E,F){return((-Math.cos(G*Math.PI)/2)+0.5)*F+E}},timers:[],fx:function(F,E,G){this.options=E;this.elem=F;this.prop=G;if(!E.orig){E.orig={}}}});o.fx.prototype={update:function(){if(this.options.step){this.options.step.call(this.elem,this.now,this)}(o.fx.step[this.prop]||o.fx.step._default)(this);if((this.prop=="height"||this.prop=="width")&&this.elem.style){this.elem.style.display="block"}},cur:function(F){if(this.elem[this.prop]!=null&&(!this.elem.style||this.elem.style[this.prop]==null)){return this.elem[this.prop]}var E=parseFloat(o.css(this.elem,this.prop,F));return E&&E>-10000?E:parseFloat(o.curCSS(this.elem,this.prop))||0},custom:function(I,H,G){this.startTime=e();this.start=I;this.end=H;this.unit=G||this.unit||"px";this.now=this.start;this.pos=this.state=0;var E=this;function F(J){return E.step(J)}F.elem=this.elem;if(F()&&o.timers.push(F)&&!n){n=setInterval(function(){var K=o.timers;for(var J=0;J<K.length;J++){if(!K[J]()){K.splice(J--,1)}}if(!K.length){clearInterval(n);n=g}},13)}},show:function(){this.options.orig[this.prop]=o.attr(this.elem.style,this.prop);this.options.show=true;this.custom(this.prop=="width"||this.prop=="height"?1:0,this.cur());o(this.elem).show()},hide:function(){this.options.orig[this.prop]=o.attr(this.elem.style,this.prop);this.options.hide=true;this.custom(this.cur(),0)},step:function(H){var G=e();if(H||G>=this.options.duration+this.startTime){this.now=this.end;this.pos=this.state=1;this.update();this.options.curAnim[this.prop]=true;var E=true;for(var F in this.options.curAnim){if(this.options.curAnim[F]!==true){E=false}}if(E){if(this.options.display!=null){this.elem.style.overflow=this.options.overflow;this.elem.style.display=this.options.display;if(o.css(this.elem,"display")=="none"){this.elem.style.display="block"}}if(this.options.hide){o(this.elem).hide()}if(this.options.hide||this.options.show){for(var I in this.options.curAnim){o.attr(this.elem.style,I,this.options.orig[I])}}this.options.complete.call(this.elem)}return false}else{var J=G-this.startTime;this.state=J/this.options.duration;this.pos=o.easing[this.options.easing||(o.easing.swing?"swing":"linear")](this.state,J,0,1,this.options.duration);this.now=this.start+((this.end-this.start)*this.pos);this.update()}return true}};o.extend(o.fx,{speeds:{slow:600,fast:200,_default:400},step:{opacity:function(E){o.attr(E.elem.style,"opacity",E.now)},_default:function(E){if(E.elem.style&&E.elem.style[E.prop]!=null){E.elem.style[E.prop]=E.now+E.unit}else{E.elem[E.prop]=E.now}}}});if(document.documentElement.getBoundingClientRect){o.fn.offset=function(){if(!this[0]){return{top:0,left:0}}if(this[0]===this[0].ownerDocument.body){return o.offset.bodyOffset(this[0])}var G=this[0].getBoundingClientRect(),J=this[0].ownerDocument,F=J.body,E=J.documentElement,L=E.clientTop||F.clientTop||0,K=E.clientLeft||F.clientLeft||0,I=G.top+(self.pageYOffset||o.boxModel&&E.scrollTop||F.scrollTop)-L,H=G.left+(self.pageXOffset||o.boxModel&&E.scrollLeft||F.scrollLeft)-K;return{top:I,left:H}}}else{o.fn.offset=function(){if(!this[0]){return{top:0,left:0}}if(this[0]===this[0].ownerDocument.body){return o.offset.bodyOffset(this[0])}o.offset.initialized||o.offset.initialize();var J=this[0],G=J.offsetParent,F=J,O=J.ownerDocument,M,H=O.documentElement,K=O.body,L=O.defaultView,E=L.getComputedStyle(J,null),N=J.offsetTop,I=J.offsetLeft;while((J=J.parentNode)&&J!==K&&J!==H){M=L.getComputedStyle(J,null);N-=J.scrollTop,I-=J.scrollLeft;if(J===G){N+=J.offsetTop,I+=J.offsetLeft;if(o.offset.doesNotAddBorder&&!(o.offset.doesAddBorderForTableAndCells&&/^t(able|d|h)$/i.test(J.tagName))){N+=parseInt(M.borderTopWidth,10)||0,I+=parseInt(M.borderLeftWidth,10)||0}F=G,G=J.offsetParent}if(o.offset.subtractsBorderForOverflowNotVisible&&M.overflow!=="visible"){N+=parseInt(M.borderTopWidth,10)||0,I+=parseInt(M.borderLeftWidth,10)||0}E=M}if(E.position==="relative"||E.position==="static"){N+=K.offsetTop,I+=K.offsetLeft}if(E.position==="fixed"){N+=Math.max(H.scrollTop,K.scrollTop),I+=Math.max(H.scrollLeft,K.scrollLeft)}return{top:N,left:I}}}o.offset={initialize:function(){if(this.initialized){return}var L=document.body,F=document.createElement("div"),H,G,N,I,M,E,J=L.style.marginTop,K='<div style="position:absolute;top:0;left:0;margin:0;border:5px solid #000;padding:0;width:1px;height:1px;"><div></div></div><table style="position:absolute;top:0;left:0;margin:0;border:5px solid #000;padding:0;width:1px;height:1px;" cellpadding="0" cellspacing="0"><tr><td></td></tr></table>';M={position:"absolute",top:0,left:0,margin:0,border:0,width:"1px",height:"1px",visibility:"hidden"};for(E in M){F.style[E]=M[E]}F.innerHTML=K;L.insertBefore(F,L.firstChild);H=F.firstChild,G=H.firstChild,I=H.nextSibling.firstChild.firstChild;this.doesNotAddBorder=(G.offsetTop!==5);this.doesAddBorderForTableAndCells=(I.offsetTop===5);H.style.overflow="hidden",H.style.position="relative";this.subtractsBorderForOverflowNotVisible=(G.offsetTop===-5);L.style.marginTop="1px";this.doesNotIncludeMarginInBodyOffset=(L.offsetTop===0);L.style.marginTop=J;L.removeChild(F);this.initialized=true},bodyOffset:function(E){o.offset.initialized||o.offset.initialize();var G=E.offsetTop,F=E.offsetLeft;if(o.offset.doesNotIncludeMarginInBodyOffset){G+=parseInt(o.curCSS(E,"marginTop",true),10)||0,F+=parseInt(o.curCSS(E,"marginLeft",true),10)||0}return{top:G,left:F}}};o.fn.extend({position:function(){var I=0,H=0,F;if(this[0]){var G=this.offsetParent(),J=this.offset(),E=/^body|html$/i.test(G[0].tagName)?{top:0,left:0}:G.offset();J.top-=j(this,"marginTop");J.left-=j(this,"marginLeft");E.top+=j(G,"borderTopWidth");E.left+=j(G,"borderLeftWidth");F={top:J.top-E.top,left:J.left-E.left}}return F},offsetParent:function(){var E=this[0].offsetParent||document.body;while(E&&(!/^body|html$/i.test(E.tagName)&&o.css(E,"position")=="static")){E=E.offsetParent}return o(E)}});o.each(["Left","Top"],function(F,E){var G="scroll"+E;o.fn[G]=function(H){if(!this[0]){return null}return H!==g?this.each(function(){this==l||this==document?l.scrollTo(!F?H:o(l).scrollLeft(),F?H:o(l).scrollTop()):this[G]=H}):this[0]==l||this[0]==document?self[F?"pageYOffset":"pageXOffset"]||o.boxModel&&document.documentElement[G]||document.body[G]:this[0][G]}});o.each(["Height","Width"],function(I,G){var E=I?"Left":"Top",H=I?"Right":"Bottom",F=G.toLowerCase();o.fn["inner"+G]=function(){return this[0]?o.css(this[0],F,false,"padding"):null};o.fn["outer"+G]=function(K){return this[0]?o.css(this[0],F,false,K?"margin":"border"):null};var J=G.toLowerCase();o.fn[J]=function(K){return this[0]==l?document.compatMode=="CSS1Compat"&&document.documentElement["client"+G]||document.body["client"+G]:this[0]==document?Math.max(document.documentElement["client"+G],document.body["scroll"+G],document.documentElement["scroll"+G],document.body["offset"+G],document.documentElement["offset"+G]):K===g?(this.length?o.css(this[0],J):null):this.css(J,typeof K==="string"?K:K+"px")}})})();

/* - jquery.autocomplete.js - */
// http://osha.europa.eu/portal_javascripts/jquery.autocomplete.js?original=1
;(function($){jQuery.autocomplete=function(input,options){var me=this;var $input=$(input).attr("autocomplete","off");if(options.inputClass) $input.addClass(options.inputClass);var results=document.createElement("div");var $results=$(results);$results.hide().addClass(options.resultsClass).css("position","absolute");if(options.width>0) $results.css("width",options.width);$("body").append(results);input.autocompleter=me;var timeout=null;var prev="";var active=-1;var cache={};var keyb=false;var hasFocus=false;var lastKeyPressCode=null;
function flushCache(){cache={};cache.data={};cache.length=0};flushCache();if(options.data!=null){var sFirstChar="",stMatchSets={},row=[];if(typeof options.url!="string") options.cacheLength=1;for(var i=0;i<options.data.length;i++){row=((typeof options.data[i]=="string")?[options.data[i]]:options.data[i]);if(row[0].length>0){sFirstChar=row[0].substring(0,1).toLowerCase();if(!stMatchSets[sFirstChar]) stMatchSets[sFirstChar]=[];stMatchSets[sFirstChar].push(row)}}
for(var k in stMatchSets){options.cacheLength++;addToCache(k,stMatchSets[k])}}
$input.keydown(function(e){lastKeyPressCode=e.keyCode;switch(e.keyCode){case 38:e.preventDefault();moveSelect(-1);break;case 40:e.preventDefault();moveSelect(1);break;case 9:case 13:if(selectCurrent()){$input.get(0).blur();e.preventDefault()}
break;default:active=-1;if(timeout) clearTimeout(timeout);timeout=setTimeout(function(){onChange()},options.delay);break}}).focus(function(){hasFocus=true}).blur(function(){hasFocus=false;hideResults()});hideResultsNow();
function onChange(){if(lastKeyPressCode==46||(lastKeyPressCode>8&&lastKeyPressCode<32)) return $results.hide();var v=$input.val();if(v==prev) return;prev=v;if(v.length>=options.minChars){$input.addClass(options.loadingClass);requestData(v)} else{$input.removeClass(options.loadingClass);$results.hide()}};
function moveSelect(step){var lis=$("li",results);if(!lis) return;active+=step;if(active<0){active=0} else if(active>=lis.size()){active=lis.size()-1}
lis.removeClass("ac_over");$(lis[active]).addClass("ac_over")};
function selectCurrent(){var li=$("li.ac_over",results)[0];if(!li){var $li=$("li",results);if(options.selectOnly){if($li.length==1) li=$li[0]} else if(options.selectFirst){li=$li[0]}}
if(li){selectItem(li);return true} else{return false}};
function selectItem(li){if(!li){li=document.createElement("li");li.extra=[];li.selectValue=""}
var v=$.trim(li.selectValue?li.selectValue:li.innerHTML);input.lastSelected=v;prev=v;$results.html("");$input.val(v);hideResultsNow();if(options.onItemSelect) setTimeout(function(){options.onItemSelect(li)},1)};
function createSelection(start,end){var field=$input.get(0);if(field.createTextRange){var selRange=field.createTextRange();selRange.collapse(true);selRange.moveStart("character",start);selRange.moveEnd("character",end);selRange.select()} else if(field.setSelectionRange){field.setSelectionRange(start,end)} else{if(field.selectionStart){field.selectionStart=start;field.selectionEnd=end}}
field.focus()};
function autoFill(sValue){if(lastKeyPressCode!=8){$input.val($input.val()+sValue.substring(prev.length));createSelection(prev.length,sValue.length)}};
function showResults(){var pos=findPos(input);var iWidth=(options.width>0)?options.width:$input.width();$results.css({width:parseInt(iWidth)+"px",top:(pos.y+input.offsetHeight)+"px",left:pos.x+"px"}).show()};
function hideResults(){if(timeout) clearTimeout(timeout);timeout=setTimeout(hideResultsNow,200)};
function hideResultsNow(){if(timeout) clearTimeout(timeout);$input.removeClass(options.loadingClass);if($results.is(":visible")){$results.hide()}
if(options.mustMatch){var v=$input.val();if(v!=input.lastSelected){selectItem(null)}}};
function receiveData(q,data){if(data){$input.removeClass(options.loadingClass);results.innerHTML="";if(!hasFocus||data.length==0) return hideResultsNow();if($.browser.msie){$results.append(document.createElement('iframe'))}
results.appendChild(dataToDom(data));if(options.autoFill&&($input.val().toLowerCase()==q.toLowerCase())) autoFill(data[0][0]);showResults()} else{hideResultsNow()}};
function parseData(data){if(!data) return null;var parsed=[];var rows=data.split(options.lineSeparator);for(var i=0;i<rows.length;i++){var row=$.trim(rows[i]);if(row){parsed[parsed.length]=row.split(options.cellSeparator)}}
return parsed};
function dataToDom(data){var ul=document.createElement("ul");var num=data.length;if((options.maxItemsToShow>0)&&(options.maxItemsToShow<num)) num=options.maxItemsToShow;for(var i=0;i<num;i++){var row=data[i];if(!row) continue;var li=document.createElement("li");if(options.formatItem){li.innerHTML=options.formatItem(row,i,num);li.selectValue=row[0]} else{li.innerHTML=row[0];li.selectValue=row[0]}
var extra=null;if(row.length>1){extra=[];for(var j=1;j<row.length;j++){extra[extra.length]=row[j]}}
li.extra=extra;ul.appendChild(li);$(li).hover(
function(){$("li",ul).removeClass("ac_over");$(this).addClass("ac_over");active=$("li",ul).indexOf($(this).get(0))},
function(){$(this).removeClass("ac_over")}).click(function(e){e.preventDefault();e.stopPropagation();selectItem(this)})}
return ul};
function requestData(q){if(!options.matchCase) q=q.toLowerCase();var data=options.cacheLength?loadFromCache(q):null;if(data&&data.length>0){receiveData(q,data)} else if((typeof options.url=="string")&&(options.url.length>0)){$.get(makeUrl(q), function(data){data=parseData(data);addToCache(q,data);receiveData(q,data)})} else{$input.removeClass(options.loadingClass)}};
function makeUrl(q){var url=options.url+"?q="+encodeURI(q);for(var i in options.extraParams){url+="&"+i+"="+encodeURI(options.extraParams[i])}
return url};
function loadFromCache(q){if(!q) return null;if(cache.data[q]) return cache.data[q];if(options.matchSubset){for(var i=q.length-1;i>=options.minChars;i--){var qs=q.substr(0,i);var c=cache.data[qs];if(c){var csub=[];for(var j=0;j<c.length;j++){var x=c[j];var x0=x[0];if(matchSubset(x0,q)){csub[csub.length]=x}}
return csub}}}
return null};
function matchSubset(s,sub){if(!options.matchCase) s=s.toLowerCase();var i=s.indexOf(sub);if(i==-1) return false;return i==0||options.matchContains};this.flushCache=function(){flushCache()};this.setExtraParams=function(p){options.extraParams=p};this.findValue=function(){var q=$input.val();if(!options.matchCase) q=q.toLowerCase();var data=options.cacheLength?loadFromCache(q):null;if(data){findValueCallback(q,data)} else if((typeof options.url=="string")&&(options.url.length>0)){$.get(makeUrl(q), function(data){data=parseData(data)
addToCache(q,data);findValueCallback(q,data)})} else{findValueCallback(q,null)}}
function findValueCallback(q,data){if(data) $input.removeClass(options.loadingClass);var num=(data)?data.length:0;var li=null;for(var i=0;i<num;i++){var row=data[i];if(row[0].toLowerCase()==q.toLowerCase()){li=document.createElement("li");if(options.formatItem){li.innerHTML=options.formatItem(row,i,num);li.selectValue=row[0]} else{li.innerHTML=row[0];li.selectValue=row[0]}
var extra=null;if(row.length>1){extra=[];for(var j=1;j<row.length;j++){extra[extra.length]=row[j]}}
li.extra=extra}}
if(options.onFindValue) setTimeout(function(){options.onFindValue(li)},1)}
function addToCache(q,data){if(!data||!q||!options.cacheLength) return;if(!cache.length||cache.length>options.cacheLength){flushCache();cache.length++} else if(!cache[q]){cache.length++}
cache.data[q]=data};
function findPos(obj){var curleft=obj.offsetLeft||0;var curtop=obj.offsetTop||0;while(obj=obj.offsetParent){curleft+=obj.offsetLeft
curtop+=obj.offsetTop}
return{x:curleft,y:curtop}}}
jQuery.fn.autocomplete=function(url,options,data){options=options||{};options.url=url;options.data=((typeof data=="object")&&(data.constructor==Array))?data:null;options.inputClass=options.inputClass||"ac_input";options.resultsClass=options.resultsClass||"ac_results";options.lineSeparator=options.lineSeparator||"\n";options.cellSeparator=options.cellSeparator||"|";options.minChars=options.minChars||1;options.delay=options.delay||400;options.matchCase=options.matchCase||0;options.matchSubset=options.matchSubset||1;options.matchContains=options.matchContains||0;options.cacheLength=options.cacheLength||1;options.mustMatch=options.mustMatch||0;options.extraParams=options.extraParams||{};options.loadingClass=options.loadingClass||"ac_loading";options.selectFirst=options.selectFirst||false;options.selectOnly=options.selectOnly||false;options.maxItemsToShow=options.maxItemsToShow||-1;options.autoFill=options.autoFill||false;options.width=parseInt(options.width,10)||0;this.each(function(){var input=this;new jQuery.autocomplete(input,options)});return this}
jQuery.fn.autocompleteArray=function(data,options){return this.autocomplete(null,options,data)}
jQuery.fn.indexOf=function(e){for(var i=0;i<this.length;i++){if(this[i]==e) return i}
return-1}})(jQuery);

/* - jquery.treeview.pack.js - */
// http://osha.europa.eu/portal_javascripts/jquery.treeview.pack.js?original=1
eval(function(p,a,c,k,e,r){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--)r[e(c)]=k[c]||e(c);k=[function(e){return r[e]}];e=function(){return'\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p}(';(4($){$.1l($.F,{E:4(b,c){l a=3.n(\'.\'+b);3.n(\'.\'+c).o(c).m(b);a.o(b).m(c);8 3},s:4(a,b){8 3.n(\'.\'+a).o(a).m(b).P()},1n:4(a){a=a||"1j";8 3.1j(4(){$(3).m(a)},4(){$(3).o(a)})},1h:4(b,a){b?3.1g({1e:"p"},b,a):3.x(4(){T(3)[T(3).1a(":U")?"H":"D"]();7(a)a.A(3,O)})},12:4(b,a){7(b){3.1g({1e:"D"},b,a)}1L{3.D();7(a)3.x(a)}},11:4(a){7(!a.1k){3.n(":r-1H:G(9)").m(k.r);3.n((a.1F?"":"."+k.X)+":G(."+k.W+")").6(">9").D()}8 3.n(":y(>9)")},S:4(b,c){3.n(":y(>9):G(:y(>a))").6(">1z").C(4(a){c.A($(3).19())}).w($("a",3)).1n();7(!b.1k){3.n(":y(>9:U)").m(k.q).s(k.r,k.t);3.G(":y(>9:U)").m(k.u).s(k.r,k.v);3.1r("<J 14=\\""+k.5+"\\"/>").6("J."+k.5).x(4(){l a="";$.x($(3).B().1o("14").13(" "),4(){a+=3+"-5 "});$(3).m(a)})}3.6("J."+k.5).C(c)},z:4(g){g=$.1l({N:"z"},g);7(g.w){8 3.1K("w",[g.w])}7(g.p){l d=g.p;g.p=4(){8 d.A($(3).B()[0],O)}}4 1m(b,c){4 L(a){8 4(){K.A($("J."+k.5,b).n(4(){8 a?$(3).B("."+a).1i:1I}));8 1G}}$("a:10(0)",c).C(L(k.u));$("a:10(1)",c).C(L(k.q));$("a:10(2)",c).C(L())}4 K(){$(3).B().6(">.5").E(k.Z,k.Y).E(k.I,k.M).P().E(k.u,k.q).E(k.v,k.t).6(">9").1h(g.1f,g.p);7(g.1E){$(3).B().1D().6(">.5").s(k.Z,k.Y).s(k.I,k.M).P().s(k.u,k.q).s(k.v,k.t).6(">9").12(g.1f,g.p)}}4 1d(){4 1C(a){8 a?1:0}l b=[];j.x(4(i,e){b[i]=$(e).1a(":y(>9:1B)")?1:0});$.V(g.N,b.1A(""))}4 1c(){l b=$.V(g.N);7(b){l a=b.13("");j.x(4(i,e){$(e).6(">9")[1y(a[i])?"H":"D"]()})}}3.m("z");l j=3.6("Q").11(g);1x(g.1w){18"V":l h=g.p;g.p=4(){1d();7(h){h.A(3,O)}};1c();17;18"1b":l f=3.6("a").n(4(){8 3.16.15()==1b.16.15()});7(f.1i){f.m("1v").1u("9, Q").w(f.19()).H()}17}j.S(g,K);7(g.R){1m(3,g.R);$(g.R).H()}8 3.1t("w",4(a,b){$(b).1s().o(k.r).o(k.v).o(k.t).6(">.5").o(k.I).o(k.M);$(b).6("Q").1q().11(g).S(g,K)})}});l k=$.F.z.1J={W:"W",X:"X",q:"q",Y:"q-5",M:"t-5",u:"u",Z:"u-5",I:"v-5",v:"v",t:"t",r:"r",5:"5"};$.F.1p=$.F.z})(T);',62,110,'|||this|function|hitarea|find|if|return|ul||||||||||||var|addClass|filter|removeClass|toggle|expandable|last|replaceClass|lastExpandable|collapsable|lastCollapsable|add|each|has|treeview|apply|parent|click|hide|swapClass|fn|not|show|lastCollapsableHitarea|div|toggler|handler|lastExpandableHitarea|cookieId|arguments|end|li|control|applyClasses|jQuery|hidden|cookie|open|closed|expandableHitarea|collapsableHitarea|eq|prepareBranches|heightHide|split|class|toLowerCase|href|break|case|next|is|location|deserialize|serialize|height|animated|animate|heightToggle|length|hover|prerendered|extend|treeController|hoverClass|attr|Treeview|andSelf|prepend|prev|bind|parents|selected|persist|switch|parseInt|span|join|visible|binary|siblings|unique|collapsed|false|child|true|classes|trigger|else'.split('|'),0,{}))

/* - base64.js - */
// http://osha.europa.eu/portal_javascripts/base64.js?original=1
var Base64={_keyStr:"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",encode: function(input){var output="";var chr1,chr2,chr3,enc1,enc2,enc3,enc4;var i=0;input=Base64._utf8_encode(input);while(i<input.length){chr1=input.charCodeAt(i++);chr2=input.charCodeAt(i++);chr3=input.charCodeAt(i++);enc1=chr1>>2;enc2=((chr1&3)<<4)|(chr2>>4);enc3=((chr2&15)<<2)|(chr3>>6);enc4=chr3&63;if(isNaN(chr2)){enc3=enc4=64} else if(isNaN(chr3)){enc4=64}
output=output+this._keyStr.charAt(enc1)+this._keyStr.charAt(enc2)+this._keyStr.charAt(enc3)+this._keyStr.charAt(enc4)}
return output},decode: function(input){var output="";var chr1,chr2,chr3;var enc1,enc2,enc3,enc4;var i=0;input=input.replace(/[^A-Za-z0-9\+\/\=]/g,"");while(i<input.length){enc1=this._keyStr.indexOf(input.charAt(i++));enc2=this._keyStr.indexOf(input.charAt(i++));enc3=this._keyStr.indexOf(input.charAt(i++));enc4=this._keyStr.indexOf(input.charAt(i++));chr1=(enc1<<2)|(enc2>>4);chr2=((enc2&15)<<4)|(enc3>>2);chr3=((enc3&3)<<6)|enc4;output=output+String.fromCharCode(chr1);if(enc3!=64){output=output+String.fromCharCode(chr2)}
if(enc4!=64){output=output+String.fromCharCode(chr3)}}
output=Base64._utf8_decode(output);return output},_utf8_encode: function(string){string=string.replace(/\r\n/g,"\n");var utftext="";for(var n=0;n<string.length;n++){var c=string.charCodeAt(n);if(c<128){utftext+=String.fromCharCode(c)}
else if((c>127)&&(c<2048)){utftext+=String.fromCharCode((c>>6)|192);utftext+=String.fromCharCode((c&63)|128)}
else{utftext+=String.fromCharCode((c>>12)|224);utftext+=String.fromCharCode(((c>>6)&63)|128);utftext+=String.fromCharCode((c&63)|128)}}
return utftext},_utf8_decode: function(utftext){var string="";var i=0;var c=c1=c2=0;while(i<utftext.length){c=utftext.charCodeAt(i);if(c<128){string+=String.fromCharCode(c);i++}
else if((c>191)&&(c<224)){c2=utftext.charCodeAt(i+1);string+=String.fromCharCode(((c&31)<<6)|(c2&63));i+=2}
else{c2=utftext.charCodeAt(i+1);c3=utftext.charCodeAt(i+2);string+=String.fromCharCode(((c&15)<<12)|((c2&63)<<6)|(c3&63));i+=3}}
return string}}

/* - itembrowser.js - */
// http://osha.europa.eu/portal_javascripts/itembrowser.js?original=1
function vocabularypicker_openBrowser(fieldName,at_url,fieldRealName,portal_type,level,root_node,nodesHaveCBs,sortAlphabetically,hide_id,server_url){vocabitempopup=window.open(server_url+'/'+at_url+'/itembrowser_popup?fieldName='+fieldName+'&fieldRealName='+fieldRealName+'&at_url='+at_url+'&portal_type='+portal_type+'&level:int='+level+'&root_node='+root_node+'&nodesHaveCBs='+nodesHaveCBs+'&sortAlphabetically='+sortAlphabetically+'&hide_id='+hide_id,'itembrowser_popup','toolbar=no,location=no,status=no,menubar=no,scrollbars=yes,resizable=yes,width=600, height=550')}
function decodeUID(uid){uid=uid.replace(/__equals__/g,'=');uid=uid.replace(/__plus__/g,'+');uid=uid.replace(/__minus__/g,'-');uid=uid.replace(/^N_/mg,"");uid=Base64.decode(uid);return uid}
function itembrowser_setItem(widget_id,uid,label,multi){if(multi==0){element=document.getElementById(widget_id)
label_element=document.getElementById(widget_id+'_label')
element.value=uid
label_element.value=label} else{var current_values=cssQuery('#'+widget_id+' input');for(var i=0;i<current_values.length;i++){if(current_values[i].value==uid){return false}}
list=document.getElementById(widget_id);li=document.createElement('li');label_element=document.createElement('label');input=document.createElement('input');input.type='checkbox';input.value=uid;input.checked=true;input.name=widget_id+':list';input.id=widget_id+'_'+uid;label_element.appendChild(input);label_element.appendChild(document.createTextNode(label));input.checked=true;li.appendChild(label_element);list.appendChild(li);document.getElementById(widget_id+'_'+uid).checked=true}}
function referencebrowser_removeReference(widget_id,multi){if(multi){list=document.getElementById(widget_id)
for(var x=list.length-1;x>=0;x--){if(list[x].selected){list[x]=null}}
for(var x=0;x<list.length;x++){list[x].selected='selected'}} else{element=document.getElementById(widget_id);label_element=document.getElementById(widget_id+'_label');label_element.value="";element.value=""}}
function handle_quicksearch_lines(li){var myId=li.extra[0];var myTitle=li.innerHTML;var myWidgetId=li.extra[1];jq('#quicksearch_'+myWidgetId)[0].value='';itembrowser_setItem(myWidgetId,myId,myTitle,1)}
var Base64={_keyStr:"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",encode: function(input){var output="";var chr1,chr2,chr3,enc1,enc2,enc3,enc4;var i=0;input=Base64._utf8_encode(input);while(i<input.length){chr1=input.charCodeAt(i++);chr2=input.charCodeAt(i++);chr3=input.charCodeAt(i++);enc1=chr1>>2;enc2=((chr1&3)<<4)|(chr2>>4);enc3=((chr2&15)<<2)|(chr3>>6);enc4=chr3&63;if(isNaN(chr2)){enc3=enc4=64} else if(isNaN(chr3)){enc4=64}
output=output+this._keyStr.charAt(enc1)+this._keyStr.charAt(enc2)+this._keyStr.charAt(enc3)+this._keyStr.charAt(enc4)}
return output},decode: function(input){var output="";var chr1,chr2,chr3;var enc1,enc2,enc3,enc4;var i=0;input=input.replace(/[^A-Za-z0-9\+\/\=]/g,"");while(i<input.length){enc1=this._keyStr.indexOf(input.charAt(i++));enc2=this._keyStr.indexOf(input.charAt(i++));enc3=this._keyStr.indexOf(input.charAt(i++));enc4=this._keyStr.indexOf(input.charAt(i++));chr1=(enc1<<2)|(enc2>>4);chr2=((enc2&15)<<4)|(enc3>>2);chr3=((enc3&3)<<6)|enc4;output=output+String.fromCharCode(chr1);if(enc3!=64){output=output+String.fromCharCode(chr2)}
if(enc4!=64){output=output+String.fromCharCode(chr3)}}
output=Base64._utf8_decode(output);return output},_utf8_encode: function(string){string=string.replace(/\r\n/g,"\n");var utftext="";for(var n=0;n<string.length;n++){var c=string.charCodeAt(n);if(c<128){utftext+=String.fromCharCode(c)}
else if((c>127)&&(c<2048)){utftext+=String.fromCharCode((c>>6)|192);utftext+=String.fromCharCode((c&63)|128)}
else{utftext+=String.fromCharCode((c>>12)|224);utftext+=String.fromCharCode(((c>>6)&63)|128);utftext+=String.fromCharCode((c&63)|128)}}
return utftext},_utf8_decode: function(utftext){var string="";var i=0;var c=c1=c2=0;while(i<utftext.length){c=utftext.charCodeAt(i);if(c<128){string+=String.fromCharCode(c);i++}
else if((c>191)&&(c<224)){c2=utftext.charCodeAt(i+1);string+=String.fromCharCode(((c&31)<<6)|(c2&63));i+=2}
else{c2=utftext.charCodeAt(i+1);c3=utftext.charCodeAt(i+2);string+=String.fromCharCode(((c&15)<<12)|((c2&63)<<6)|(c3&63));i+=3}}
return string}}


/* - cssQuery.js - */
// http://osha.europa.eu/portal_javascripts/cssQuery.js?original=1
eval(__dEcOdE('9 o=5(){9 1o="2.0.2";9 C=/\\s*,\\s*/;9 o=5(s,1b){try{9 m=[];9 u=1c.callee.1L&&!1b;9 b=(1b)?(1b.constructor==1W)?1b:[1b]:[Z];9 25=Q(s).1E(C),i;M(i=0;i<25.q;i++){s=29(25[i]);B(13&&s.1e(0,3).22("")==" *#"){s=s.1e(2);1b=2d([],b,s[1])}1D 1b=b;9 j=0,t,f,a,c="";T(j<s.q){t=s[j++];f=s[j++];c+=t+f;a="";B(s[j]=="("){T(s[j++]!=")"&&j<s.q){a+=s[j]}a=a.1e(0,-1);c+="("+a+")"}B(t==" "&&f=="*"&&s[j]=="#")1l;1b=(u&&19[c])?19[c]:1M(1b,t,f,a);B(u)19[c]=1b}m=m.concat(1b)}1Q o.1U;6 m}catch(e){o.1U=e;6 []}};o.1A=5(){6 "5 o() {\\n  [1o "+1o+"]\\n}"};9 19={};o.1L=Y;o.clearCache=5(s){B(s){s=29(s).22("");1Q 19[s]}1D 19={}};9 1J={};9 1u=Y;o.14=5(n,s){B(1u)1P("$script="+1S(s));1J[n]=1F s()};o.valueOf=5(c){6 c?1P(c):F};9 y={};9 8={};9 7={X:/\\[([\\w-]+(\\|[\\w-]+)?)\\s*(\\W?=)?\\s*([^\\]]*)\\]/};9 l=[];y[" "]=5(r,f,t,n){9 e,i,j;M(i=0;i<f.q;i++){9 s=x(f[i],t,n);M(j=0;(e=s[j]);j++){B(z(e)&&H(e,n))r.K(e)}}};y["#"]=5(r,f,i){9 e,j;B(f.q==1&&f[0]==Z){9 n=Z.getElementById(i);B(n)r.K(n)}1D{M(j=0;(e=f[j]);j++)B(e.1j==i){r.K(e);1s}}};y["."]=5(r,f,c){c=1F 1y("(^|\\\\s)"+c+"(\\\\s|$)");9 e,i;M(i=0;(e=f[i]);i++)B(c.G(e.1x))r.K(e)};y[":"]=5(r,f,p,a){9 t=8[p],e,i;B(t)M(i=0;(e=f[i]);i++)B(t(e,a))r.K(e)};8["link"]=5(e){9 d=D(e);B(d.1G)M(9 i=0;i<d.1G.q;i++){B(d.1G[i]==e)6 15}};8["visited"]=5(e){};9 z=5(e){6(e&&e.1i==1&&e.1a!="!")?e:20};9 A=5(e){T(e&&(e=e.previousSibling)&&!z(e))1l;6 e};9 h=5(e){T(e&&(e=e.nextSibling)&&!z(e))1l;6 e};9 R=5(e){6 z(e.1q)||h(e.1q)};9 16=5(e){6 z(e.1v)||A(e.1v)};9 12=5(e){9 c=[];e=R(e);T(e){c.K(e);e=h(e)}6 c};9 13=15;9 1H=5(e){9 d=D(e);6(typeof d.1C=="unknown")?/\\.24$/i.G(d.URL):Boolean(d.1C=="XML Document")};9 D=5(e){6 e.ownerDocument||e.Z};9 x=5(e,t){6(t=="*"&&e.1Z)?e.1Z:e.x(t)};9 P=5(e,t,n){B(t=="*")6 z(e);B(!H(e,n))6 Y;B(!1H(e))6 e.1a.1m()==t.1m();6 e.1a==t};9 H=5(e,n){6!n||(n=="*")||(e.scopeName==n)};9 V=5(e){6 e.1w};5 2d(r,f,1j){9 m,i,j;M(i=0;i<f.q;i++){B(m=f[i].1Z.item(1j)){B(m.1j==1j)r.K(m);1D B(m.q!=20){M(j=0;j<m.q;j++){B(m[j].1j==1j)r.K(m[j])}}}}6 r};B(![].K)1W.prototype.K=5(){M(9 i=0;i<1c.q;i++){F[F.q]=1c[i]}6 F.q};9 N=/\\|/;5 1M(1b,t,f,a){B(N.G(f)){f=f.1E(N);a=f[0];f=f[1]}9 r=[];B(y[t]){y[t](r,1b,f,a)}6 r};9 S=/^[^\\s>+~]/;9 2e=/[\\s#.:>+~()@]|[^\\s#.:>+~()@]+/g;5 29(s){B(S.G(s))s=" "+s;6 s.X(2e)||[]};9 W=/\\s*([\\s>+~(),]|^|$)\\s*/g;9 I=/([\\s>+~,]|[^(]\\+|^)([#.:@])/g;9 Q=5(s){6 s.O(W,"$1").O(I,"$1*$2")};9 1I={1A:5(){6 "\'"},X:/^(\'[^\']*\')|("[^"]*")$/,G:5(s){6 F.X.G(s)},28:5(s){6 F.G(s)?s:F+s+F},1N:5(s){6 F.G(s)?s.1e(1,-1):s}};9 1p=5(t){6 1I.1N(t)};9 E=/([\\/()[\\]?{}|*+-])/g;5 J(s){6 s.O(E,"\\\\$1")};o.14("1Y-standard",5(){13=1P("Y;/*@cc_on@B(@\\x5fwin32)13=15@end@*/");B(!13){x=5(e,t,n){6 n?e.getElementsByTagNameNS("*",t):e.x(t)};H=5(e,n){6!n||(n=="*")||(e.prefix==n)};1H=Z.1n? 5(e){6/24/i.G(D(e).1n)}:5(e){6 D(e).18.1a!="HTML"};V=5(e){6 e.textContent||e.1w||2b(e)};5 2b(e){9 t="",n,i;M(i=0;(n=e.1r[i]);i++){1t(n.1i){10 11:10 1:t+=2b(n);1s;10 3:t+=n.nodeValue;1s}}6 t}}});o.14("1Y-level2",5(){y[">"]=5(r,f,t,n){9 e,i,j;M(i=0;i<f.q;i++){9 s=12(f[i]);M(j=0;(e=s[j]);j++)B(P(e,t,n))r.K(e)}};y["+"]=5(r,f,t,n){M(9 i=0;i<f.q;i++){9 e=h(f[i]);B(e&&P(e,t,n))r.K(e)}};y["@"]=5(r,f,a){9 t=l[a].G;9 e,i;M(i=0;(e=f[i]);i++)B(t(e))r.K(e)};8["first-1g"]=5(e){6!A(e)};8["1O"]=5(e,c){c=1F 1y("^"+c,"i");T(e&&!e.L("1O"))e=e.17;6 e&&c.G(e.L("1O"))};7.1V=/\\\\:/g;7.1z="@";7.U={};7.O=5(m,a,n,c,v){9 k=F.1z+m;B(!l[k]){a=F.1R(a,c||"",v||"");l[k]=a;l.K(a)}6 l[k].1j};7.1T=5(s){s=s.O(F.1V,"|");9 m;T(m=s.X(F.X)){9 r=F.O(m[0],m[1],m[2],m[3],m[4]);s=s.O(F.X,r)}6 s};7.1R=5(p,t,v){9 a={};a.1j=F.1z+l.q;a.name=p;t=F.U[t];t=t?t(F.L(p),1p(v)):Y;a.G=1F Function("e","6 "+t);6 a};7.L=5(n){1t(n.toLowerCase()){10 "1j":6 "e.1j";10 "class":6 "e.1x";10 "M":6 "e.htmlFor";10 "23":B(13){6 "1S((e.outerHTML.X(/23=\\\\1X?([^\\\\s\\\\1X]*)\\\\1X?/)||[])[1]||\'\')"}}6 "e.L(\'"+n.O(N,":")+"\')"};7.U[""]=5(a){6 a};7.U["="]=5(a,v){6 a+"=="+1I.28(v)};7.U["~="]=5(a,v){6 "/(^| )"+J(v)+"( |$)/.G("+a+")"};7.U["|="]=5(a,v){6 "/^"+J(v)+"(-|$)/.G("+a+")"};9 2c=Q;Q=5(s){6 2c(7.1T(s))}});o.14("1Y-level3",5(){y["~"]=5(r,f,t,n){9 e,i;M(i=0;(e=f[i]);i++){T(e=h(e)){B(P(e,t,n))r.K(e)}}};8["contains"]=5(e,t){t=1F 1y(J(1p(t)));6 t.G(V(e))};8["root"]=5(e){6 e==D(e).18};8["empty"]=5(e){9 n,i;M(i=0;(n=e.1r[i]);i++){B(z(n)||n.1i==3)6 Y}6 15};8["21-1g"]=5(e){6!h(e)};8["only-1g"]=5(e){e=e.17;6 R(e)==16(e)};8["not"]=5(e,s){9 n=o(s,D(e));M(9 i=0;i<n.q;i++){B(n[i]==e)6 Y}6 15};8["26-1g"]=5(e,a){6 1h(e,a,A)};8["26-21-1g"]=5(e,a){6 1h(e,a,h)};8["target"]=5(e){6 e.1j==location.hash.1e(1)};8["1K"]=5(e){6 e.1K};8["enabled"]=5(e){6 e.1k===Y};8["1k"]=5(e){6 e.1k};8["1d"]=5(e){6 e.1d};7.U["^="]=5(a,v){6 "/^"+J(v)+"/.G("+a+")"};7.U["$="]=5(a,v){6 "/"+J(v)+"$/.G("+a+")"};7.U["*="]=5(a,v){6 "/"+J(v)+"/.G("+a+")"};5 1h(e,a,t){1t(a){10 "n":6 15;10 "even":a="2n";1s;10 "odd":a="2n+1"}9 27=12(e.17);5 2a(i){9 i=(t==h)?27.q-i:i-1;6 27[i]==e};B(!1f(a))6 2a(a);a=a.1E("n");9 m=1B(a[0]);9 s=1B(a[1]);B((1f(m)||m==1)&&s==0)6 15;B(m==0&&!1f(s))6 2a(s);B(1f(s))s=0;9 c=1;T(e=t(e))c++;B(1f(m)||m==1)6(t==h)?(c<=s):(s>=c);6(c%m)==s}});1u=15;6 o}();',62,139,'',0,{}))

/* - ++resource++jquery.ui/ui/ui.core.js - */
/*
 * jQuery UI 1.6rc5
 *
 * Copyright (c) 2009 AUTHORS.txt (http://ui.jquery.com/about)
 * Dual licensed under the MIT (MIT-LICENSE.txt)
 * and GPL (GPL-LICENSE.txt) licenses.
 *
 * http://docs.jquery.com/UI
 */
;(function($) {

var _remove = $.fn.remove,
	isFF2 = $.browser.mozilla && (parseFloat($.browser.version) < 1.9);

//Helper functions and ui object
$.ui = {
	version: "1.6rc5",

	// $.ui.plugin is deprecated.  Use the proxy pattern instead.
	plugin: {
		add: function(module, option, set) {
			var proto = $.ui[module].prototype;
			for(var i in set) {
				proto.plugins[i] = proto.plugins[i] || [];
				proto.plugins[i].push([option, set[i]]);
			}
		},
		call: function(instance, name, args) {
			var set = instance.plugins[name];
			if(!set) { return; }

			for (var i = 0; i < set.length; i++) {
				if (instance.options[set[i][0]]) {
					set[i][1].apply(instance.element, args);
				}
			}
		}
	},

	contains: function(a, b) {
		return document.compareDocumentPosition
			? a.compareDocumentPosition(b) & 16
			: a !== b && a.contains(b);
	},

	cssCache: {},
	css: function(name) {
		if ($.ui.cssCache[name]) { return $.ui.cssCache[name]; }
		var tmp = $('<div class="ui-gen"></div>').addClass(name).css({position:'absolute', top:'-5000px', left:'-5000px', display:'block'}).appendTo('body');

		//if (!$.browser.safari)
			//tmp.appendTo('body');

		//Opera and Safari set width and height to 0px instead of auto
		//Safari returns rgba(0,0,0,0) when bgcolor is not set
		$.ui.cssCache[name] = !!(
			(!(/auto|default/).test(tmp.css('cursor')) || (/^[1-9]/).test(tmp.css('height')) || (/^[1-9]/).test(tmp.css('width')) ||
			!(/none/).test(tmp.css('backgroundImage')) || !(/transparent|rgba\(0, 0, 0, 0\)/).test(tmp.css('backgroundColor')))
		);
		try { $('body').get(0).removeChild(tmp.get(0));	} catch(e){}
		return $.ui.cssCache[name];
	},

	hasScroll: function(el, a) {

		//If overflow is hidden, the element might have extra content, but the user wants to hide it
		if ($(el).css('overflow') == 'hidden') { return false; }

		var scroll = (a && a == 'left') ? 'scrollLeft' : 'scrollTop',
			has = false;

		if (el[scroll] > 0) { return true; }

		// TODO: determine which cases actually cause this to happen
		// if the element doesn't have the scroll set, see if it's possible to
		// set the scroll
		el[scroll] = 1;
		has = (el[scroll] > 0);
		el[scroll] = 0;
		return has;
	},

	isOverAxis: function(x, reference, size) {
		//Determines when x coordinate is over "b" element axis
		return (x > reference) && (x < (reference + size));
	},

	isOver: function(y, x, top, left, height, width) {
		//Determines when x, y coordinates is over "b" element
		return $.ui.isOverAxis(y, top, height) && $.ui.isOverAxis(x, left, width);
	},

	keyCode: {
		BACKSPACE: 8,
		CAPS_LOCK: 20,
		COMMA: 188,
		CONTROL: 17,
		DELETE: 46,
		DOWN: 40,
		END: 35,
		ENTER: 13,
		ESCAPE: 27,
		HOME: 36,
		INSERT: 45,
		LEFT: 37,
		NUMPAD_ADD: 107,
		NUMPAD_DECIMAL: 110,
		NUMPAD_DIVIDE: 111,
		NUMPAD_ENTER: 108,
		NUMPAD_MULTIPLY: 106,
		NUMPAD_SUBTRACT: 109,
		PAGE_DOWN: 34,
		PAGE_UP: 33,
		PERIOD: 190,
		RIGHT: 39,
		SHIFT: 16,
		SPACE: 32,
		TAB: 9,
		UP: 38
	}
};

// WAI-ARIA normalization
if (isFF2) {
	var attr = $.attr,
		removeAttr = $.fn.removeAttr,
		ariaNS = "http://www.w3.org/2005/07/aaa",
		ariaState = /^aria-/,
		ariaRole = /^wairole:/;

	$.attr = function(elem, name, value) {
		var set = value !== undefined;

		return (name == 'role'
			? (set
				? attr.call(this, elem, name, "wairole:" + value)
				: (attr.apply(this, arguments) || "").replace(ariaRole, ""))
			: (ariaState.test(name)
				? (set
					? elem.setAttributeNS(ariaNS,
						name.replace(ariaState, "aaa:"), value)
					: attr.call(this, elem, name.replace(ariaState, "aaa:")))
				: attr.apply(this, arguments)));
	};

	$.fn.removeAttr = function(name) {
		return (ariaState.test(name)
			? this.each(function() {
				this.removeAttributeNS(ariaNS, name.replace(ariaState, ""));
			}) : removeAttr.call(this, name));
	};
}

//jQuery plugins
$.fn.extend({
	remove: function() {
		// Safari has a native remove event which actually removes DOM elements,
		// so we have to use triggerHandler instead of trigger (#3037).
		$("*", this).add(this).each(function() {
			$(this).triggerHandler("remove");
		});
		return _remove.apply(this, arguments );
	},

	enableSelection: function() {
		return this
			.attr('unselectable', 'off')
			.css('MozUserSelect', '')
			.unbind('selectstart.ui');
	},

	disableSelection: function() {
		return this
			.attr('unselectable', 'on')
			.css('MozUserSelect', 'none')
			.bind('selectstart.ui', function() { return false; });
	},

	scrollParent: function() {
		var scrollParent;
		if(($.browser.msie && (/(static|relative)/).test(this.css('position'))) || (/absolute/).test(this.css('position'))) {
			scrollParent = this.parents().filter(function() {
				return (/(relative|absolute|fixed)/).test($.curCSS(this,'position',1)) && (/(auto|scroll)/).test($.curCSS(this,'overflow',1)+$.curCSS(this,'overflow-y',1)+$.curCSS(this,'overflow-x',1));
			}).eq(0);
		} else {
			scrollParent = this.parents().filter(function() {
				return (/(auto|scroll)/).test($.curCSS(this,'overflow',1)+$.curCSS(this,'overflow-y',1)+$.curCSS(this,'overflow-x',1));
			}).eq(0);
		}

		return (/fixed/).test(this.css('position')) || !scrollParent.length ? $(document) : scrollParent;
	}
});


//Additional selectors
$.extend($.expr[':'], {
	data: function(elem, i, match) {
		return !!$.data(elem, match[3]);
	},

	// TODO: add support for object, area
	tabbable: function(elem) {
		var nodeName = elem.nodeName.toLowerCase();
		function isVisible(element) {
			return !($(element).is(':hidden') || $(element).parents(':hidden').length);
		}

		return (
			// in tab order
			elem.tabIndex >= 0 &&

			( // filter node types that participate in the tab order

				// anchor tag
				('a' == nodeName && elem.href) ||

				// enabled form element
				(/input|select|textarea|button/.test(nodeName) &&
					'hidden' != elem.type && !elem.disabled)
			) &&

			// visible on page
			isVisible(elem)
		);
	}
});


// $.widget is a factory to create jQuery plugins
// taking some boilerplate code out of the plugin code
function getter(namespace, plugin, method, args) {
	function getMethods(type) {
		var methods = $[namespace][plugin][type] || [];
		return (typeof methods == 'string' ? methods.split(/,?\s+/) : methods);
	}

	var methods = getMethods('getter');
	if (args.length == 1 && typeof args[0] == 'string') {
		methods = methods.concat(getMethods('getterSetter'));
	}
	return ($.inArray(method, methods) != -1);
}

$.widget = function(name, prototype) {
	var namespace = name.split(".")[0];
	name = name.split(".")[1];

	// create plugin method
	$.fn[name] = function(options) {
		var isMethodCall = (typeof options == 'string'),
			args = Array.prototype.slice.call(arguments, 1);

		// prevent calls to internal methods
		if (isMethodCall && options.substring(0, 1) == '_') {
			return this;
		}

		// handle getter methods
		if (isMethodCall && getter(namespace, name, options, args)) {
			var instance = $.data(this[0], name);
			return (instance ? instance[options].apply(instance, args)
				: undefined);
		}

		// handle initialization and non-getter methods
		return this.each(function() {
			var instance = $.data(this, name);

			// constructor
			(!instance && !isMethodCall &&
				$.data(this, name, new $[namespace][name](this, options)));

			// method call
			(instance && isMethodCall && $.isFunction(instance[options]) &&
				instance[options].apply(instance, args));
		});
	};

	// create widget constructor
	$[namespace] = $[namespace] || {};
	$[namespace][name] = function(element, options) {
		var self = this;

		this.namespace = namespace;
		this.widgetName = name;
		this.widgetEventPrefix = $[namespace][name].eventPrefix || name;
		this.widgetBaseClass = namespace + '-' + name;

		this.options = $.extend({},
			$.widget.defaults,
			$[namespace][name].defaults,
			$.metadata && $.metadata.get(element)[name],
			options);

		this.element = $(element)
			.bind('setData.' + name, function(event, key, value) {
				if (event.target == element) {
					return self._setData(key, value);
				}
			})
			.bind('getData.' + name, function(event, key) {
				if (event.target == element) {
					return self._getData(key);
				}
			})
			.bind('remove', function() {
				return self.destroy();
			});

		this._init();
	};

	// add widget prototype
	$[namespace][name].prototype = $.extend({}, $.widget.prototype, prototype);

	// TODO: merge getter and getterSetter properties from widget prototype
	// and plugin prototype
	$[namespace][name].getterSetter = 'option';
};

$.widget.prototype = {
	_init: function() {},
	destroy: function() {
		this.element.removeData(this.widgetName)
			.removeClass(this.widgetBaseClass + '-disabled' + ' ' + this.namespace + '-state-disabled')
			.removeAttr('aria-disabled');
	},

	option: function(key, value) {
		var options = key,
			self = this;

		if (typeof key == "string") {
			if (value === undefined) {
				return this._getData(key);
			}
			options = {};
			options[key] = value;
		}

		$.each(options, function(key, value) {
			self._setData(key, value);
		});
	},
	_getData: function(key) {
		return this.options[key];
	},
	_setData: function(key, value) {
		this.options[key] = value;

		if (key == 'disabled') {
			this.element
				[value ? 'addClass' : 'removeClass'](
					this.widgetBaseClass + '-disabled' + ' ' +
					this.namespace + '-state-disabled')
				.attr("aria-disabled", value);
		}
	},

	enable: function() {
		this._setData('disabled', false);
	},
	disable: function() {
		this._setData('disabled', true);
	},

	_trigger: function(type, event, data) {
		var callback = this.options[type],
			eventName = (type == this.widgetEventPrefix
				? type : this.widgetEventPrefix + type);

		event = $.Event(event);
		event.type = eventName;

		this.element.trigger(event, data);

		return !($.isFunction(callback) && callback.call(this.element[0], event, data) === false
			|| event.isDefaultPrevented());
	}
};

$.widget.defaults = {
	disabled: false
};


/** Mouse Interaction Plugin **/

$.ui.mouse = {
	_mouseInit: function() {
		var self = this;

		this.element
			.bind('mousedown.'+this.widgetName, function(event) {
				return self._mouseDown(event);
			})
			.bind('click.'+this.widgetName, function(event) {
				if(self._preventClickEvent) {
					self._preventClickEvent = false;
					return false;
				}
			});

		// Prevent text selection in IE
		if ($.browser.msie) {
			this._mouseUnselectable = this.element.attr('unselectable');
			this.element.attr('unselectable', 'on');
		}

		this.started = false;
	},

	// TODO: make sure destroying one instance of mouse doesn't mess with
	// other instances of mouse
	_mouseDestroy: function() {
		this.element.unbind('.'+this.widgetName);

		// Restore text selection in IE
		($.browser.msie
			&& this.element.attr('unselectable', this._mouseUnselectable));
	},

	_mouseDown: function(event) {
		// we may have missed mouseup (out of window)
		(this._mouseStarted && this._mouseUp(event));

		this._mouseDownEvent = event;

		var self = this,
			btnIsLeft = (event.which == 1),
			elIsCancel = (typeof this.options.cancel == "string" ? $(event.target).parents().add(event.target).filter(this.options.cancel).length : false);
		if (!btnIsLeft || elIsCancel || !this._mouseCapture(event)) {
			return true;
		}

		this.mouseDelayMet = !this.options.delay;
		if (!this.mouseDelayMet) {
			this._mouseDelayTimer = setTimeout(function() {
				self.mouseDelayMet = true;
			}, this.options.delay);
		}

		if (this._mouseDistanceMet(event) && this._mouseDelayMet(event)) {
			this._mouseStarted = (this._mouseStart(event) !== false);
			if (!this._mouseStarted) {
				event.preventDefault();
				return true;
			}
		}

		// these delegates are required to keep context
		this._mouseMoveDelegate = function(event) {
			return self._mouseMove(event);
		};
		this._mouseUpDelegate = function(event) {
			return self._mouseUp(event);
		};
		$(document)
			.bind('mousemove.'+this.widgetName, this._mouseMoveDelegate)
			.bind('mouseup.'+this.widgetName, this._mouseUpDelegate);

		// preventDefault() is used to prevent the selection of text here -
		// however, in Safari, this causes select boxes not to be selectable
		// anymore, so this fix is needed
		($.browser.safari || event.preventDefault());
		
		return true;
	},

	_mouseMove: function(event) {
		// IE mouseup check - mouseup happened when mouse was out of window
		if ($.browser.msie && !event.button) {
			return this._mouseUp(event);
		}

		if (this._mouseStarted) {
			this._mouseDrag(event);
			return event.preventDefault();
		}

		if (this._mouseDistanceMet(event) && this._mouseDelayMet(event)) {
			this._mouseStarted =
				(this._mouseStart(this._mouseDownEvent, event) !== false);
			(this._mouseStarted ? this._mouseDrag(event) : this._mouseUp(event));
		}

		return !this._mouseStarted;
	},

	_mouseUp: function(event) {
		$(document)
			.unbind('mousemove.'+this.widgetName, this._mouseMoveDelegate)
			.unbind('mouseup.'+this.widgetName, this._mouseUpDelegate);

		if (this._mouseStarted) {
			this._mouseStarted = false;
			this._preventClickEvent = true;
			this._mouseStop(event);
		}

		return false;
	},

	_mouseDistanceMet: function(event) {
		return (Math.max(
				Math.abs(this._mouseDownEvent.pageX - event.pageX),
				Math.abs(this._mouseDownEvent.pageY - event.pageY)
			) >= this.options.distance
		);
	},

	_mouseDelayMet: function(event) {
		return this.mouseDelayMet;
	},

	// These are placeholder methods, to be overriden by extending plugin
	_mouseStart: function(event) {},
	_mouseDrag: function(event) {},
	_mouseStop: function(event) {},
	_mouseCapture: function(event) { return true; }
};

$.ui.mouse.defaults = {
	cancel: null,
	distance: 1,
	delay: 0
};

})(jQuery);


/* - jquery.dynatree.min.js - */
// jquery.dynatree.js build 0.4.2
// Revision: 216, date: 2009-04-19 08:08:47
// Copyright (c) 2008-09  Martin Wendt (http://dynatree.googlecode.com/)
// Licensed under the MIT License.

var _canLog=true;function _log(mode,msg){if(!_canLog)
return;var args=Array.prototype.slice.apply(arguments,[1]);var dt=new Date();var tag=dt.getHours()+":"+dt.getMinutes()+":"+dt.getSeconds()+"."+dt.getMilliseconds();args[0]=tag+" - "+args[0];try{switch(mode){case"info":window.console.info.apply(window.console,args);break;case"warn":window.console.warn.apply(window.console,args);break;default:window.console.log.apply(window.console,args);}}catch(e){if(!window.console)
_canLog=false;}}
function logMsg(msg){Array.prototype.unshift.apply(arguments,["debug"]);_log.apply(this,arguments);}
var DTNodeStatus_Error=-1;var DTNodeStatus_Loading=1;var DTNodeStatus_Ok=0;;(function($){var Class={create:function(){return function(){this.initialize.apply(this,arguments);}}}
var DynaTreeNode=Class.create();DynaTreeNode.prototype={initialize:function(parent,tree,data){this.parent=parent;this.tree=tree;if(typeof data=="string")
data={title:data};if(data.key==undefined)
data.key="_"+tree._nodeCount++;this.data=$.extend({},$.ui.dynatree.nodedatadefaults,data);this.div=null;this.span=null;this.childList=null;this.isRead=false;this.hasSubSel=false;if(tree.initMode=="cookie"){if(tree.initActiveKey==this.data.key)
tree.activeNode=this;if(tree.initFocusKey==this.data.key)
tree.focusNode=this;this.bExpanded=($.inArray(this.data.key,tree.initExpandedKeys)>=0);this.bSelected=($.inArray(this.data.key,tree.initSelectedKeys)>=0);}else{if(data.activate)
tree.activeNode=this;if(data.focus)
tree.focusNode=this;this.bExpanded=(data.expand==true);this.bSelected=(data.select==true);}
if(this.bExpanded)
tree.expandedNodes.push(this);if(this.bSelected)
tree.selectedNodes.push(this);},toString:function(){return"dtnode<"+this.data.key+">: '"+this.data.title+"'";},toDict:function(recursive,callback){var dict=$.extend({},this.data);dict.activate=(this.tree.activeNode===this);dict.focus=(this.tree.focusNode===this);dict.expand=this.bExpanded;dict.select=this.bSelected;if(callback)
callback(dict);if(recursive&&this.childList){dict.children=[];for(var i=0;i<this.childList.length;i++)
dict.children.push(this.childList[i].toDict(true,callback));}else{delete dict.children;}
return dict;},_getInnerHtml:function(){var opts=this.tree.options;var cache=this.tree.cache;var rootParent=opts.rootVisible?null:this.tree.tnRoot;var bHideFirstExpander=(opts.rootVisible&&opts.minExpandLevel>0)||opts.minExpandLevel>1;var bHideFirstConnector=opts.rootVisible||opts.minExpandLevel>0;var res="";var p=this.parent;while(p){if(bHideFirstConnector&&(p==rootParent))
break;res=(p.isLastSibling()?cache.tagEmpty:cache.tagVline)+res;p=p.parent;}
if(bHideFirstExpander&&this.parent==rootParent){}else if(this.childList||this.data.isLazy){res+=cache.tagExpander;}else{res+=cache.tagConnector;}
if(opts.checkbox&&this.data.hideCheckbox!=true&&!this.data.isStatusNode){res+=cache.tagCheckbox;}
if(this.data.icon){res+="<img src='"+opts.imagePath+this.data.icon+"' alt='' />";}else if(this.data.icon==false){}else{res+=cache.tagNodeIcon;}
var tooltip=(this.data&&typeof this.data.tooltip=="string")?" title='"+this.data.tooltip+"'":"";res+="<a href='#'"+tooltip+">"+this.data.title+"</a>";return res;},render:function(bDeep,bHidden){if(!this.div){this.span=document.createElement("span");this.span.dtnode=this;if(this.data.key)
this.span.id=this.tree.options.idPrefix+this.data.key;this.div=document.createElement("div");this.div.appendChild(this.span);if(this.parent)
this.parent.div.appendChild(this.div);if(this.parent==null&&!this.tree.options.rootVisible)
this.span.style.display="none";}
this.span.innerHTML=this._getInnerHtml();this.div.style.display=(this.parent==null||this.parent.bExpanded?"":"none");var opts=this.tree.options;var cn=opts.classNames;var isLastSib=this.isLastSibling();var cnList=[];cnList.push((this.data.isFolder)?cn.folder:cn.document);if(this.bExpanded)
cnList.push(cn.expanded);if(this.data.isLazy&&!this.isRead)
cnList.push(cn.lazy);if(isLastSib)
cnList.push(cn.lastsib);if(this.bSelected)
cnList.push(cn.selected);if(this.hasSubSel)
cnList.push(cn.partsel);if(this.tree.activeNode===this)
cnList.push(cn.active);if(this.data.addClass)
cnList.push(this.data.addClass);cnList.push(cn.combinedExpanderPrefix
+(this.bExpanded?"e":"c")
+(this.data.isLazy&&!this.isRead?"d":"")
+(isLastSib?"l":""));cnList.push(cn.combinedIconPrefix
+(this.bExpanded?"e":"c")
+(this.data.isFolder?"f":""));this.span.className=cnList.join(" ");if(bDeep&&this.childList&&(bHidden||this.bExpanded)){for(var i=0;i<this.childList.length;i++){this.childList[i].render(bDeep,bHidden)}}},hasChildren:function(){return this.childList!=null;},isLastSibling:function(){var p=this.parent;if(!p)return true;return p.childList[p.childList.length-1]===this;},prevSibling:function(){if(!this.parent)return null;var ac=this.parent.childList;for(var i=1;i<ac.length;i++)
if(ac[i]===this)
return ac[i-1];return null;},nextSibling:function(){if(!this.parent)return null;var ac=this.parent.childList;for(var i=0;i<ac.length-1;i++)
if(ac[i]===this)
return ac[i+1];return null;},_setStatusNode:function(data){var firstChild=(this.childList?this.childList[0]:null);if(!data){if(firstChild){this.div.removeChild(firstChild.div);if(this.childList.length==1)
this.childList=null;else
this.childList.shift();}}else if(firstChild){data.isStatusNode=true;firstChild.data=data;firstChild.render(false,false);}else{data.isStatusNode=true;firstChild=this._addNode(data);}},setLazyNodeStatus:function(lts){switch(lts){case DTNodeStatus_Ok:this._setStatusNode(null);this.isRead=true;this.render(false,false);if(this.tree.options.autoFocus){if(this===this.tree.tnRoot&&!this.tree.options.rootVisible&&this.childList){this.childList[0].focus();}else{this.focus();}}
break;case DTNodeStatus_Loading:this._setStatusNode({title:this.tree.options.strings.loading,addClass:this.tree.options.classNames.nodeWait});break;case DTNodeStatus_Error:this._setStatusNode({title:this.tree.options.strings.loadError,addClass:this.tree.options.classNames.nodeError});break;default:throw"Bad LazyNodeStatus: '"+lts+"'.";}},_parentList:function(includeRoot,includeSelf){var l=[];var dtn=includeSelf?this:this.parent;while(dtn){if(includeRoot||dtn.parent)
l.unshift(dtn);dtn=dtn.parent;};return l;},getLevel:function(){var level=0;var dtn=this.parent;while(dtn){level++;dtn=dtn.parent;};return level;},isVisible:function(){var parents=this._parentList(true,false);for(var i=0;i<parents.length;i++)
if(!parents[i].bExpanded)return false;return true;},makeVisible:function(){var parents=this._parentList(true,false);for(var i=0;i<parents.length;i++)
parents[i]._expand(true);},focus:function(){this.makeVisible();try{$(this.span).find(">a").focus();}catch(e){}},isActive:function(){return(this.tree.activeNode===this);},activate:function(){var opts=this.tree.options;if(this.data.isStatusNode)
return;if(opts.onQueryActivate&&opts.onQueryActivate.call(this.span,true,this)==false)
return;if(this.tree.activeNode){if(this.tree.activeNode===this)
return;this.tree.activeNode.deactivate();}
if(opts.activeVisible)
this.makeVisible();this.tree.activeNode=this;if(opts.persist)
$.cookie(opts.cookieId+"-active",this.data.key,opts.cookie);$(this.span).addClass(opts.classNames.active);if(opts.onActivate)
opts.onActivate.call(this.span,this);},deactivate:function(){if(this.tree.activeNode===this){var opts=this.tree.options;if(opts.onQueryActivate&&opts.onQueryActivate.call(this.span,false,this)==false)
return;$(this.span).removeClass(opts.classNames.active);if(opts.persist){$.cookie(opts.cookieId+"-active","",opts.cookie);}
this.tree.activeNode=null;if(opts.onDeactivate)
opts.onDeactivate.call(this.span,this);}},_userActivate:function(){var activate=true;var expand=false;if(this.data.isFolder){switch(this.tree.options.clickFolderMode){case 2:activate=false;expand=true;break;case 3:activate=expand=true;break;}}
if(this.parent==null&&this.tree.options.minExpandLevel>0){expand=false;}
if(expand){this.toggleExpand();this.focus();}
if(activate){this.activate();}},_setSubSel:function(hasSubSel){if(hasSubSel){this.hasSubSel=true;$(this.span).addClass(this.tree.options.classNames.partsel);}else{this.hasSubSel=false;$(this.span).removeClass(this.tree.options.classNames.partsel);}},_fixSelectionState:function(){if(this.bSelected){this.visit(function(dtnode){dtnode.parent._setSubSel(true);dtnode._select(true,false,false);});var p=this.parent;while(p){p._setSubSel(true);var allChildsSelected=true;for(var i=0;i<p.childList.length;i++){var n=p.childList[i];if(!n.bSelected&&!n.data.isStatusNode){allChildsSelected=false;break;}}
if(allChildsSelected)
p._select(true,false,false);p=p.parent;}}else{this._setSubSel(false);this.visit(function(dtnode){dtnode._setSubSel(false);dtnode._select(false,false,false);});var p=this.parent;while(p){p._select(false,false,false);var isPartSel=false;for(var i=0;i<p.childList.length;i++){if(p.childList[i].bSelected||p.childList[i].hasSubSel){isPartSel=true;break;}}
p._setSubSel(isPartSel);p=p.parent;}}},_select:function(sel,fireEvents,deep){var opts=this.tree.options;if(this.data.isStatusNode)
return;if(this.bSelected==sel){return;}
if(fireEvents&&opts.onQuerySelect&&opts.onQuerySelect.call(this.span,sel,this)==false)
return;if(opts.selectMode==1&&this.tree.selectedNodes.length&&sel)
this.tree.selectedNodes[0]._select(false,false,false);this.bSelected=sel;this.tree._changeNodeList("select",this,sel);if(sel){$(this.span).addClass(opts.classNames.selected);if(deep&&opts.selectMode==3)
this._fixSelectionState();if(fireEvents&&opts.onSelect)
opts.onSelect.call(this.span,true,this);}else{$(this.span).removeClass(opts.classNames.selected);if(deep&&opts.selectMode==3)
this._fixSelectionState();if(fireEvents&&opts.onSelect)
opts.onSelect.call(this.span,false,this);}},isSelected:function(){return this.bSelected;},select:function(sel){return this._select(sel!=false,true,true);},toggleSelect:function(){return this.select(!this.bSelected);},_expand:function(bExpand){if(this.bExpanded==bExpand){return;}
var opts=this.tree.options;if(!bExpand&&this.getLevel()<opts.minExpandLevel){this.tree.logDebug("dtnode._expand(%o) forced expand - %o",bExpand,this);return;}
if(opts.onQueryExpand&&opts.onQueryExpand.call(this.span,bExpand,this)==false)
return;this.bExpanded=bExpand;this.tree._changeNodeList("expand",this,bExpand);this.render(false);if(this.bExpanded&&this.parent&&opts.autoCollapse){var parents=this._parentList(false,true);for(var i=0;i<parents.length;i++)
parents[i].collapseSiblings();}
if(opts.activeVisible&&this.tree.activeNode&&!this.tree.activeNode.isVisible()){this.tree.activeNode.deactivate();}
if(bExpand&&this.data.isLazy&&!this.isRead){try{this.tree.logDebug("_expand: start lazy - %o",this);this.setLazyNodeStatus(DTNodeStatus_Loading);if(true==opts.onLazyRead.call(this.span,this)){this.setLazyNodeStatus(DTNodeStatus_Ok);this.tree.logDebug("_expand: lazy succeeded - %o",this);}}catch(e){this.setLazyNodeStatus(DTNodeStatus_Error);}
return;}
if(opts.fx){var duration=opts.fx.duration||200;$(">DIV",this.div).animate(opts.fx,duration);}else{var $d=$(">DIV",this.div);$d.toggle();}
if(opts.onExpand)
opts.onExpand.call(this.span,bExpand,this);},expand:function(flag){if(!this.childList&&!this.data.isLazy&&flag)
return;if(this.parent==null&&this.tree.options.minExpandLevel>0&&!flag)
return;this._expand(flag);},toggleExpand:function(){this.expand(!this.bExpanded);},collapseSiblings:function(){if(this.parent==null)
return;var ac=this.parent.childList;for(var i=0;i<ac.length;i++){if(ac[i]!==this&&ac[i].bExpanded)
ac[i]._expand(false);}},onClick:function(event){if($(event.target).hasClass(this.tree.options.classNames.expander)){this.toggleExpand();}else if($(event.target).hasClass(this.tree.options.classNames.checkbox)){this.toggleSelect();}else{this._userActivate();this.span.getElementsByTagName("a")[0].focus();}
return false;},onDblClick:function(event){},onKeydown:function(event){var handled=true;switch(event.which){case 107:case 187:if(!this.bExpanded)this.toggleExpand();break;case 109:case 189:if(this.bExpanded)this.toggleExpand();break;case 32:this._userActivate();break;case 8:if(this.parent)
this.parent.focus();break;case 37:if(this.bExpanded){this.toggleExpand();this.focus();}else if(this.parent&&(this.tree.options.rootVisible||this.parent.parent)){this.parent.focus();}
break;case 39:if(!this.bExpanded&&(this.childList||this.data.isLazy)){this.toggleExpand();this.focus();}else if(this.childList){this.childList[0].focus();}
break;case 38:var sib=this.prevSibling();while(sib&&sib.bExpanded)
sib=sib.childList[sib.childList.length-1];if(!sib&&this.parent&&(this.tree.options.rootVisible||this.parent.parent))
sib=this.parent;if(sib)sib.focus();break;case 40:var sib;if(this.bExpanded){sib=this.childList[0];}else{var parents=this._parentList(false,true);for(var i=parents.length-1;i>=0;i--){sib=parents[i].nextSibling();if(sib)break;}}
if(sib)sib.focus();break;default:handled=false;}
return!handled;},onKeypress:function(event){},onFocus:function(event){var opts=this.tree.options;if(event.type=="blur"||event.type=="focusout"){if(opts.onBlur)
opts.onBlur.call(this.span,this);if(this.tree.tnFocused)
$(this.tree.tnFocused.span).removeClass(opts.classNames.focused);this.tree.tnFocused=null;if(opts.persist){$.cookie(opts.cookieId+"-focus",null,$.extend({},opts.cookie));}}else if(event.type=="focus"||event.type=="focusin"){if(this.tree.tnFocused&&this.tree.tnFocused!==this){this.tree.logDebug("dtnode.onFocus: out of sync: curFocus: %o",this.tree.tnFocused);$(this.tree.tnFocused.span).removeClass(opts.classNames.focused);}
this.tree.tnFocused=this;if(opts.onFocus)
opts.onFocus.call(this.span,this);$(this.tree.tnFocused.span).addClass(opts.classNames.focused);if(opts.persist)
$.cookie(opts.cookieId+"-focus",this.data.key,opts.cookie);}},_postInit:function(){if(opts.onPostInit)
opts.onPostInit.call(this.span,this);},visit:function(fn,data,includeSelf){var n=0;if(includeSelf==true){if(fn(this,data)==false)
return 1;n++;}
if(this.childList)
for(var i=0;i<this.childList.length;i++)
n+=this.childList[i].visit(fn,data,true);return n;},remove:function(){if(this===this.tree.root)
return false;return this.parent.removeChild(this);},removeChild:function(tn){var ac=this.childList;if(ac.length==1){if(tn!==ac[0])
throw"removeChild: invalid child";return this.removeChildren();}
if(tn===this.tree.activeNode)
tn.deactivate();if(tn.bSelected)
this.tree._changeNodeList("select",tn,false);if(tn.bExpanded)
this.tree._changeNodeList("expand",tn,false);tn.removeChildren(true);this.div.removeChild(tn.div);for(var i=0;i<ac.length;i++){if(ac[i]===tn){this.childList.splice(i,1);delete tn;break;}}},removeChildren:function(recursive){var tree=this.tree;var ac=this.childList;if(ac){for(var i=0;i<ac.length;i++){var tn=ac[i];if(tn===tree.activeNode)
tn.deactivate();if(tn.bSelected)
this.tree._changeNodeList("select",tn,false);if(tn.bExpanded)
this.tree._changeNodeList("expand",tn,false);tn.removeChildren(true);this.div.removeChild(tn.div);delete tn;}
this.childList=null;if(!recursive){this._expand(false);this.isRead=false;this.render(false,false);}}},_addChildNode:function(dtnode){var tree=this.tree;var opts=tree.options;if(this.childList==null){this.childList=[];}else{$(this.childList[this.childList.length-1].span).removeClass(opts.classNames.lastsib);}
this.childList.push(dtnode);dtnode.parent=this;if(dtnode.data.expand||opts.minExpandLevel>=dtnode.getLevel())
this.bExpanded=true;if(!dtnode.data.isStatusNode&&opts.selectMode==3&&!tree.isInitializing())
dtnode._fixSelectionState();if(tree.bEnableUpdate)
this.render(true,true);return dtnode;},_addNode:function(data){return this._addChildNode(new DynaTreeNode(this,this.tree,data));},append:function(obj){if(!obj||obj.length==0)
return;if(!obj.length)
obj=[obj];var prevFlag=this.tree.enableUpdate(false);var tnFirst=null;for(var i=0;i<obj.length;i++){var data=obj[i];var dtnode=this._addNode(data);if(!tnFirst)tnFirst=dtnode;if(data.children)
dtnode.append(data.children);}
this.tree.enableUpdate(prevFlag);return tnFirst;},appendAjax:function(ajaxOptions){this.setLazyNodeStatus(DTNodeStatus_Loading);var self=this;var orgSuccess=ajaxOptions.success;var orgError=ajaxOptions.error;var options=$.extend({},this.tree.options.ajaxDefaults,ajaxOptions,{success:function(data,textStatus){self.append(data);self.setLazyNodeStatus(DTNodeStatus_Ok);if(orgSuccess)
orgSuccess.call(options,self);},error:function(XMLHttpRequest,textStatus,errorThrown){self.setLazyNodeStatus(DTNodeStatus_Error);if(orgError)
orgError.call(options,self,XMLHttpRequest,textStatus,errorThrown);}});$.ajax(options);},lastentry:undefined}
var DynaTree=Class.create();DynaTree.version="$Version: 0.4.2$";DynaTree.prototype={initialize:function(divContainer,options){this.options=options;this.bEnableUpdate=true;this._nodeCount=0;this.initMode="data";this.activeNode=null;this.selectedNodes=[];this.expandedNodes=[];if(this.options.persist){this.initActiveKey=$.cookie(this.options.cookieId+"-active");if(cookie||this.initActiveKey!=null)
this.initMode="cookie";this.initFocusKey=$.cookie(this.options.cookieId+"-focus");var cookie=$.cookie(this.options.cookieId+"-expand");if(cookie!=null)
this.initMode="cookie";this.initExpandedKeys=cookie?cookie.split(","):[];cookie=$.cookie(this.options.cookieId+"-select");this.initSelectedKeys=cookie?cookie.split(","):[];}
this.logDebug("initMode: %o, active: %o, focus: %o, expanded: %o, selected: %o",this.initMode,this.initActiveKey,this.initFocusKey,this.initExpandedKeys,this.initSelectedKeys);this.cache={tagEmpty:"<span class='"+options.classNames.empty+"'></span>",tagVline:"<span class='"+options.classNames.vline+"'></span>",tagExpander:"<span class='"+options.classNames.expander+"'></span>",tagConnector:"<span class='"+options.classNames.connector+"'></span>",tagNodeIcon:"<span class='"+options.classNames.nodeIcon+"'></span>",tagCheckbox:"<span class='"+options.classNames.checkbox+"'></span>",lastentry:undefined};this.divTree=divContainer;this.tnRoot=new DynaTreeNode(null,this,{title:this.options.title,key:"root"});this.tnRoot.data.isFolder=true;this.tnRoot.render(false,false);this.divRoot=this.tnRoot.div;this.divRoot.className=this.options.classNames.container;this.divTree.appendChild(this.divRoot);},toString:function(){return"DynaTree '"+this.options.title+"'";},toDict:function(){return this.tnRoot.toDict(true);},logDebug:function(msg){if(this.options.debugLevel>=2){Array.prototype.unshift.apply(arguments,["debug"]);_log.apply(this,arguments);}},logInfo:function(msg){if(this.options.debugLevel>=1){Array.prototype.unshift.apply(arguments,["info"]);_log.apply(this,arguments);}},logWarning:function(msg){Array.prototype.unshift.apply(arguments,["warn"]);_log.apply(this,arguments);},isInitializing:function(){return(this.initMode=="data"||this.initMode=="cookie"||this.initMode=="postInit");},_changeNodeList:function(mode,node,bAdd){if(!node)
return false;var cookieName=this.options.cookieId+"-"+mode;var nodeList=(mode=="expand")?this.expandedNodes:this.selectedNodes;var idx=$.inArray(node,nodeList);if(bAdd){if(idx>=0)
return false;nodeList.push(node);}else{if(idx<0)
return false;nodeList.splice(idx,1);}
if(this.options.persist){var keyList=$.map(nodeList,function(e,i){return e.data.key});$.cookie(cookieName,keyList.join(","),this.options.cookie);}else{}},redraw:function(){this.logDebug("dynatree.redraw()...");this.tnRoot.render(true,true);this.logDebug("dynatree.redraw() done.");},getRoot:function(){return this.tnRoot;},getNodeByKey:function(key){var el=document.getElementById(this.options.idPrefix+key);return(el&&el.dtnode)?el.dtnode:null;},getActiveNode:function(){return this.activeNode;},getSelectedNodes:function(stopOnParents){if(stopOnParents==true){var nodeList=[];this.tnRoot.visit(function(dtnode){if(dtnode.bSelected){nodeList.push(dtnode);return false;}});return nodeList;}else{return this.selectedNodes;}},activateKey:function(key){var dtnode=this.getNodeByKey(key);if(!dtnode){this.activeNode=null;return null;}
dtnode.focus();dtnode.activate();return dtnode;},selectKey:function(key,select){var dtnode=this.getNodeByKey(key);if(!dtnode)
return null;dtnode.select(select);return dtnode;},enableUpdate:function(bEnable){if(this.bEnableUpdate==bEnable)
return bEnable;this.bEnableUpdate=bEnable;if(bEnable)
this.redraw();return!bEnable;},visit:function(fn,data,includeRoot){return this.tnRoot.visit(fn,data,includeRoot);},_createFromTag:function(parentTreeNode,$ulParent){var self=this;$ulParent.find(">li").each(function(){var $li=$(this);var $liSpan=$li.find(">span:first");var title;if($liSpan.length){title=$liSpan.html();}else{title=$li.html();var iPos=title.search(/<ul/i);if(iPos>=0)
title=$.trim(title.substring(0,iPos));else
title=$.trim(title);}
var data={title:title,isFolder:$li.hasClass("folder"),isLazy:$li.hasClass("lazy"),expand:$li.hasClass("expanded"),select:$li.hasClass("selected"),activate:$li.hasClass("active"),focus:$li.hasClass("focused")};if($li.attr("title"))
data.tooltip=$li.attr("title");if($li.attr("id"))
data.key=$li.attr("id");if($li.attr("data")){var dataAttr=$.trim($li.attr("data"));if(dataAttr){if(dataAttr.charAt(0)!="{")
dataAttr="{"+dataAttr+"}"
try{$.extend(data,eval("("+dataAttr+")"));}catch(e){throw("Error parsing node data: "+e+"\ndata:\n'"+dataAttr+"'");}}}
childNode=parentTreeNode._addNode(data);var $ul=$li.find(">ul:first");if($ul.length){self._createFromTag(childNode,$ul);}});},lastentry:undefined};$.widget("ui.dynatree",{init:function(){return this._init();},_init:function(){logMsg("Dynatree._init(): version='%s', debugLevel=%o.",DynaTree.version,this.options.debugLevel);this.options.event+=".dynatree";var $this=this.element;var opts=this.options;if(!opts.imagePath){$("script").each(function(){if(this.src.search(/.*dynatree[^/]*\.js$/i)>=0){if(this.src.indexOf("/")>=0)
opts.imagePath=this.src.slice(0,this.src.lastIndexOf("/"))+"/skin/";else
opts.imagePath="skin/";logMsg("Guessing imagePath from '%s': '%s'",this.src,opts.imagePath);return false;}});}
var divContainer=$this.get(0);if(opts.children||(opts.initAjax&&opts.initAjax.url)||opts.initId)
$(divContainer).empty();this.tree=new DynaTree(divContainer,opts);var root=this.tree.getRoot();var prevFlag=this.tree.enableUpdate(false);this.tree.logDebug("Start init tree structure...");if(opts.children){root.append(opts.children);}else if(opts.initAjax&&opts.initAjax.url){root.appendAjax(opts.initAjax);}else if(opts.initId){this.tree._createFromTag(root,$("#"+opts.initId));}else{var $ul=$this.find(">ul").hide();this.tree._createFromTag(root,$ul);$ul.remove();}
this.tree.enableUpdate(prevFlag);this.tree.logDebug("Init tree structure... done.");this.bind();this.tree.initMode="postInit";nodeList=this.tree.selectedNodes.slice();this.tree.selectedNodes=[];for(var i=0;i<nodeList.length;i++){var dtnode=nodeList[i];this.tree.logDebug("Re-select on init: %o",dtnode);dtnode.bSelected=false;dtnode.select(true);}
if(this.tree.focusNode){this.tree.logDebug("Focus on init: %o",this.tree.focusNode);this.tree.focusNode.focus();}
if(this.tree.activeNode){var dtnode=this.tree.activeNode;this.tree.activeNode=null;this.tree.logDebug("Activate on init: %o",dtnode);dtnode._userActivate();}
this.tree.initMode="running";},bind:function(){var $this=this.element;var o=this.options;this.unbind();function __getNodeFromElement(el){var iMax=4;do{if(el.dtnode)return el.dtnode;el=el.parentNode;}while(iMax--);return null;}
$this.bind("click.dynatree dblclick.dynatree keypress.dynatree keydown.dynatree",function(event){var dtnode=__getNodeFromElement(event.target);if(!dtnode)
return false;dtnode.tree.logDebug("bind(%o): dtnode: %o",event,dtnode);switch(event.type){case"click":return(o.onClick&&o.onClick(dtnode,event)===false)?false:dtnode.onClick(event);case"dblclick":return(o.onDblClick&&o.onDblClick(dtnode,event)===false)?false:dtnode.onDblClick(event);case"keydown":return(o.onKeydown&&o.onKeydown(dtnode,event)===false)?false:dtnode.onKeydown(event);case"keypress":return(o.onKeypress&&o.onKeypress(dtnode,event)===false)?false:dtnode.onKeypress(event);};});function __focusHandler(event){event=arguments[0]=$.event.fix(event||window.event);var dtnode=__getNodeFromElement(event.target);return dtnode?dtnode.onFocus(event):false;}
var div=this.tree.divTree;if(div.addEventListener){div.addEventListener("focus",__focusHandler,true);div.addEventListener("blur",__focusHandler,true);}else{div.onfocusin=div.onfocusout=__focusHandler;}},unbind:function(){this.element.unbind(".dynatree");},enable:function(){this.bind();this.setData("disabled",false);},disable:function(){this.unbind();this.setData("disabled",true);},getTree:function(){return this.tree;},getRoot:function(){return this.tree.getRoot();},getActiveNode:function(){return this.tree.getActiveNode();},getSelectedNodes:function(){return this.tree.getSelectedNodes();},lastentry:undefined});$.ui.dynatree.getter="getTree getRoot getActiveNode getSelectedNodes";$.ui.dynatree.defaults={title:"Dynatree root",rootVisible:false,minExpandLevel:1,imagePath:null,children:null,initId:null,initAjax:null,autoFocus:true,keyboard:true,persist:false,autoCollapse:false,clickFolderMode:3,activeVisible:true,checkbox:false,selectMode:2,fx:null,onClick:null,onDblClick:null,onKeydown:null,onKeypress:null,onFocus:null,onBlur:null,onQueryActivate:null,onQuerySelect:null,onQueryExpand:null,onActivate:null,onDeactivate:null,onSelect:null,onExpand:null,onLazyRead:null,ajaxDefaults:{cache:false,dataType:"json"},strings:{loading:"Loading&#8230;",loadError:"Load error!"},idPrefix:"ui-dynatree-id-",cookieId:"ui-dynatree-cookie",cookie:{expires:null},classNames:{container:"ui-dynatree-container",folder:"ui-dynatree-folder",document:"ui-dynatree-document",empty:"ui-dynatree-empty",vline:"ui-dynatree-vline",expander:"ui-dynatree-expander",connector:"ui-dynatree-connector",checkbox:"ui-dynatree-checkbox",nodeIcon:"ui-dynatree-icon",nodeError:"ui-dynatree-statusnode-error",nodeWait:"ui-dynatree-statusnode-wait",hidden:"ui-dynatree-hidden",combinedExpanderPrefix:"ui-dynatree-exp-",combinedIconPrefix:"ui-dynatree-ico-",active:"ui-dynatree-active",selected:"ui-dynatree-selected",expanded:"ui-dynatree-expanded",lazy:"ui-dynatree-lazy",focused:"ui-dynatree-focused",partsel:"ui-dynatree-partsel",lastsib:"ui-dynatree-lastsib"},debugLevel:1,lastentry:undefined};$.ui.dynatree.nodedatadefaults={title:null,key:null,isFolder:false,isLazy:false,tooltip:null,icon:null,addClass:null,activate:false,focus:false,expand:false,select:false,children:null,lastentry:undefined};})(jQuery);

/* - tree.js - */
/*jslint white: true, onevar: true, undef: true, nomen: true, eqeqeq: true, plusplus: true, bitwise: true, regexp: true, strict: true, newcap: true */
/*global jq */
"use strict";

function inline_tree_init() {
    if (self.inline_tree_initialised === true) {
        return;
    }
    self.inline_tree_initialised = true;

    // Javascript function for really adding a selected category to an object
    function addItems(objects, id, func) {
        jq.map(objects, function (o) {
            jq.post(o.ajax_url, {
                add: id,
                field: o.field
            }, function (data) {
                return func(data, o.list, o.base_id);
            });
        });
    }

    // Javascript function for really removing an unselected category from an
    // object
    function removeItems(objects, id, func) {
        jq.map(objects, function (object) {
            jq.post(object.ajax_url, {
                remove: id,
                field: object.field
            }, function (data) {
                return func(data, object.list, object.base_id);
            });
        });
    }

    // Category management, can be overwritten
    function getCategories() {
        return self._objects;
    }
    function addCategory(category) {
        self._objects = jq.merge(self._objects, jq.makeArray(category));
    }
    function resetCategories() {
        self._objects = jq.makeArray();
    }


    /* For each inline tree widget we find on the page */
    jq('.inline_tree').each(function (item) {

        this.addCategory = addCategory;
        this.getCategories = getCategories;
        this.resetCategories = resetCategories;
        this.resetCategories();
        var base_id = this.id.replace('.', '\\.').replace(':', '\\:');
        var fx = this.fx;
        if (!fx) {
            fx = {
                height: "toggle",
                duration: 200
            };
        }
        var inline_tree_this = this;
        var data_field = jq(this);
        var id_prefix = base_id + '-inline-';
        function jq_(suffix) {
            // find an object with the current base id and the specified suffix.
            return jq(("#" + base_id + '_' + suffix));
        }
        var fieldName = jq_('fieldName').val();

        /* add event handlers to the remove parts */
        function loadRemoveButtons(list, base_id) {
            /* When one clicks on the remove button, submit a request
             * to delete the category from the object. After this finished
             * successfully, remove the category from the view
             */
            list.children().children('img').filter(function () {
                var className = this.className;
                return className.substring(className.length - 'remove'.length) === 'remove' && !jq(this).data('click_added');
            }).each(function () {
                jq(this).click(function () {
                    var item_to_remove = this;
                    var li = jq(this).parent()[0];
                    var liid = li.id.substring("liid_".length + base_id.replace('\\.', '.').replace('\\:', ':').length);
                    if (!jq.map(inline_tree_this.getCategories(), function (object) {
                        return object.field;
                    }).filter(function () {
                        return 'subcategory' === this;
                    })) {
/*                    }).contains(fieldName)) { */
                        inline_tree_this.addCategory({
                            ajax_url: jq_('ajax_url').val(),
                            field: fieldName,
                            list: data_field,
                            base_id : base_id
                        });
                    }
                    removeItems(inline_tree_this.getCategories(), liid, function (data, list, base_id) {
                        jq('#liid_' + base_id + liid).remove();
                        jq_('inlinetree').dynatree('getTree').selectKey(liid, false);
                    });
                });
                jq(this).data('click_added', 1);
            });
        }

        /* Build the tree */
        loadRemoveButtons(data_field, base_id);
        function resetActivatorButtons(func) {
            return function () {
                var activator = this;
                jq(".tree").each(function () {
                    if (this === activator) {
                    }
                    else {
                        jq(this).hide();
                    }
                });
                func();
            };
        }
        jq_("activator").toggle(resetActivatorButtons(function () {
            jq_("inlinetree").dynatree({
                persist: false,
                initAjax: {
                    url: jq_('vocabulary_url').val() + '/json',
                    data: {'_': '1'},
                    success: function (reload, isError) {
                        jq('#' + base_id + ' li').each(function () {
                            var id = this.id.substring(5 + base_id.replace('\\.', '.').replace('\\:', ':').length);
                            if (id) {
                                var key = jq_('inlinetree').dynatree('getTree').selectKey(id, true);
                                if (key !== null) {
                                    key.makeVisible();
                                }
                            }
                        });
                        self['initialised_' + base_id] = true;
                    }
                },
                onSelect: function (flag, dtnode) {
                    if (self['initialised_' + base_id] !== true) {
                        return;
                    }
                    if (flag) {
                        var id = dtnode.data.key;
                        addItems(inline_tree_this.getCategories(), id, function (data, list, base_id) {
                            jq(list.children()[0]).after('<li id="liid_' +
                            base_id.replace('\\.', '.').replace('\\:', ':') +
                            id +
                            '"><img src="delete_icon.gif" title="Click here to delete" class="remove ' +
                            base_id.replace('\\.', '.').replace('\\:', ':') +
                            '_remove" />' +
                            data +
                            '</li>');
                            loadRemoveButtons(list, base_id);
                        });
                    }
                    else {
                        removeItems(inline_tree_this.getCategories(), dtnode.data.key, function (data, list, base_id) {
                            jq('#liid_' + base_id + dtnode.data.key).remove();
                        });
                    }
                },
                idPrefix: id_prefix,
                fx: fx,
                debugLevel: 0,
                checkbox: true,
                strings: {
                    loading: jq(".tree_wait").text(),
                    loadError: jq(".tree_error").text()
                }
            });
            inline_tree_this.resetCategories();
            inline_tree_this.addCategory({
                ajax_url: jq_('ajax_url').val(),
                field: fieldName,
                list: data_field,
                base_id : base_id
            });
            jq_('inlinetree').show();
        }), resetActivatorButtons(function () {
            inline_tree_this.resetCategories();
            jq_('inlinetree').hide();
        }));
    });
}

function portlet_tree_init() {
    if (self.tree_portlet_initialised === true) {
        return;
    }
    self.tree_portlet_initialised = true;

    jq('.tree_portlet_category').each(function (item) {
        var base_id = this.id;
        var fx = this.fx;
        if (!fx) {
            fx = {
                height: "toggle",
                duration: 200
            };
        }
        var data_field = jq(this);
        function jq_(suffix) {
            // find an object with the current base id and the specified suffix.
            return jq("#" + base_id + '_' + suffix);
        }
        function toggleHighlight(element) {
            var category = element.parents('.tree')[0].id.split('_')[0];
            jq('.categorizerForm .category.' + category).filter(function () {
                return jq(this).parent().children('input:checked').length;
            }).each(function () {
                jq(this).parent().toggleClass('error');
            });
        }
        function makeDraggable(selector) {
            jq(selector).each(function () {
                this.toggleHighlight = function () {
                    jq(selector).each(function () {
                        toggleHighlight(jq(this));
                    });
                };
            });
            jq(selector).draggable({
                'revert': true,
                start: function (event, ui) {
                    toggleHighlight(ui.helper);
                },
                stop: function (event, ui) {
                    toggleHighlight(ui.helper);
                }
            });
        }
        jq_("tree").dynatree({
            persist: false,
            onExpand: function (node) {
                makeDraggable(this);
            },
            initAjax: {
                url: jq_('vocabulary_url').val() + '/json',
                success: function (reload, isError) {
                    makeDraggable('#' + base_id + '_tree .ui-dynatree-container a');
                }
            },
            fx: fx,
            debugLevel: 0,
            strings: {
                loading: jq(".tree_wait").text(),
                loadError: jq(".tree_error").text()
            }
        });
    });
}

function tree_init() {
    // each select input item that belongs to this widget contains the
    // state of the widget. We look for that input item to get the state, and
    // all configuration for the dynamic elements. the base id for each
    // element, for example. Interaction with plone is done via the select box
    // only!
    if (self.tree_initialised === true) {
        return;
    }
    self.tree_initialised = true;
    jq('.tree_values').each(function (item) {
        var base_id = this.id;
        var fx = this.fx;
        if (!fx) {
            fx = {
                height: "toggle",
                duration: 200
            };
        }
        // for some reason the select element is not
        // wrapped by jquery, we do it here
        var data_field = jq(this);
        function jq_(suffix) {
            // find an object with the current base id and the specified suffix.
            return jq("#" + base_id + '_' + suffix);
        }
        function initTree(event) {
            // update the trees. This method is the preferred way to update the tree contents
            // One tree shall only show the unselected
            // methods, the other only the selected
            // We build one filter here, that can be
            // used for both xmlhttprequests
            var filters = "&key_limiter:list=";
            data_field.children().each(function (i) {
                filters += '&key_limiter:list=' + this.value;
            });
            filters += '&full_text_filter=' + jq_('filter').val();
            // Both trees are initialized similary.
            // The information for retrieving the valid
            // options is stored in the html,
            // the parameters are dynamically set up
            // here. the can_have tree shows the
            // possible items, thus the item filter is
            // set to reverse.
            // the onActivate event is fired when one
            // clicks on an element.
            // The event handler updates only the select
            // input element, and then triggers
            // a change event on the select input
            // element. This in turns calls updateTree
            // which updates the tree.
            if (jq_('can_have').dynatree('getRoot')) {
                jq_('can_have').dynatree('getRoot').removeChildren();
                jq_('has').dynatree('getRoot').removeChildren();
            }
            jq_("can_have").dynatree({
                onActivate: function (dtnode) {
                    data_field.append(new Option(dtnode.data.title, dtnode.data.key, true));
                    dtnode.visit(function (node, data) {
                        jq('#' + base_id + ' option[value=' + node.data.key + ']').remove();
                    }, false);
                    data_field.change();
                },
                persist: false,
                initAjax: {
                    url: jq_('vocabulary_url').val() + '/json?1=1' + filters + '&invert_key_limiter=True'
                },
                fx: fx,
                debugLevel: 0,
                strings: {
                    loading: jq(".tree_wait").text(),
                    loadError: jq(".tree_error").text()
                }
            });
            jq_("has").dynatree({
                onActivate: function (dtnode) {
                    dtnode.toDict(true, function (dict) {
                        jq('#' + base_id + ' option[value=' + dict.key + ']').remove();
                    });
                    data_field.change();
                },
                persist: false,
                initAjax: {
                    url: jq_('vocabulary_url').val() + '/json?1=1' + filters
                },
                fx: fx,
                debugLevel: 0,
                strings: {
                    loading: jq(".tree_wait").text(),
                    loadError: jq(".tree_error").text()
                }
            });
        }
        function updateTree(event) {
            var filters = "&key_limiter:list=";
            data_field.children().each(function (i) {
                filters += '&key_limiter:list=' + this.value;
            });
            filters += '&full_text_filter=' + jq_('filter').val();

            function _updateTree(item, url) {
                jQuery.getJSON(url, function (data) {
                    item.dynatree('getRoot').removeChildren();
                    item.dynatree('getRoot').append(data);
                });
            }
            _updateTree(jq_("has"), jq_('vocabulary_url').val() + '/json?1=1' + filters);
            _updateTree(jq_("can_have"), jq_('vocabulary_url').val() + '/json?1=1' + filters + '&invert_key_limiter=True');
        }
        data_field.change(updateTree);
        initTree();
        // Each tree item has a filter that acts without
        // submit button. It waits 500ms before doing
        // the actual filtering
        var treesearch_timerid = 'None';
        jq_('filter').bind('keypress', function (e) {
            if (treesearch_timerid !== 'None') {
                clearTimeout(treesearch_timerid);
            }
            treesearch_timerid = setTimeout(updateTree, 500);
        });
    });
}


/* - ++resource++jquery.ui/ui/ui.droppable.js - */
/*
 * jQuery UI Droppable 1.6rc5
 *
 * Copyright (c) 2009 AUTHORS.txt (http://ui.jquery.com/about)
 * Dual licensed under the MIT (MIT-LICENSE.txt)
 * and GPL (GPL-LICENSE.txt) licenses.
 *
 * http://docs.jquery.com/UI/Droppables
 *
 * Depends:
 *	ui.core.js
 *	ui.draggable.js
 */
(function($) {

$.widget("ui.droppable", {

	_init: function() {

		var o = this.options, accept = o.accept;
		this.isover = 0; this.isout = 1;

		this.options.accept = this.options.accept && $.isFunction(this.options.accept) ? this.options.accept : function(d) {
			return d.is(accept);
		};

		//Store the droppable's proportions
		this.proportions = { width: this.element[0].offsetWidth, height: this.element[0].offsetHeight };

		// Add the reference and positions to the manager
		$.ui.ddmanager.droppables[this.options.scope] = $.ui.ddmanager.droppables[this.options.scope] || [];
		$.ui.ddmanager.droppables[this.options.scope].push(this);

		(this.options.cssNamespace && this.element.addClass(this.options.cssNamespace+"-droppable"));

	},

	destroy: function() {
		var drop = $.ui.ddmanager.droppables[this.options.scope];
		for ( var i = 0; i < drop.length; i++ )
			if ( drop[i] == this )
				drop.splice(i, 1);

		this.element
			.removeClass(this.options.cssNamespace+"-droppable "+this.options.cssNamespace+"-droppable-disabled")
			.removeData("droppable")
			.unbind(".droppable");
	},

	_setData: function(key, value) {

		if(key == 'accept') {
			this.options.accept = value && $.isFunction(value) ? value : function(d) {
				return d.is(accept);
			};
		} else {
			$.widget.prototype._setData.apply(this, arguments);
		}

	},

	_activate: function(event) {

		var draggable = $.ui.ddmanager.current;
		$.ui.plugin.call(this, 'activate', [event, this.ui(draggable)]);
		(draggable && this._trigger('activate', event, this.ui(draggable)));

	},

	_deactivate: function(event) {

		var draggable = $.ui.ddmanager.current;
		$.ui.plugin.call(this, 'deactivate', [event, this.ui(draggable)]);
		(draggable && this._trigger('deactivate', event, this.ui(draggable)));

	},

	_over: function(event) {

		var draggable = $.ui.ddmanager.current;
		if (!draggable || (draggable.currentItem || draggable.element)[0] == this.element[0]) return; // Bail if draggable and droppable are same element

		if (this.options.accept.call(this.element,(draggable.currentItem || draggable.element))) {
			$.ui.plugin.call(this, 'over', [event, this.ui(draggable)]);
			this._trigger('over', event, this.ui(draggable));
		}

	},

	_out: function(event) {

		var draggable = $.ui.ddmanager.current;
		if (!draggable || (draggable.currentItem || draggable.element)[0] == this.element[0]) return; // Bail if draggable and droppable are same element

		if (this.options.accept.call(this.element,(draggable.currentItem || draggable.element))) {
			$.ui.plugin.call(this, 'out', [event, this.ui(draggable)]);
			this._trigger('out', event, this.ui(draggable));
		}

	},

	_drop: function(event,custom) {

		var draggable = custom || $.ui.ddmanager.current;
		if (!draggable || (draggable.currentItem || draggable.element)[0] == this.element[0]) return false; // Bail if draggable and droppable are same element

		var childrenIntersection = false;
		this.element.find(":data(droppable)").not("."+draggable.options.cssNamespace+"-draggable-dragging").each(function() {
			var inst = $.data(this, 'droppable');
			if(inst.options.greedy && $.ui.intersect(draggable, $.extend(inst, { offset: inst.element.offset() }), inst.options.tolerance)) {
				childrenIntersection = true; return false;
			}
		});
		if(childrenIntersection) return false;

		if(this.options.accept.call(this.element,(draggable.currentItem || draggable.element))) {
			$.ui.plugin.call(this, 'drop', [event, this.ui(draggable)]);
			this._trigger('drop', event, this.ui(draggable));
			return this.element;
		}

		return false;

	},

	plugins: {},

	ui: function(c) {
		return {
			draggable: (c.currentItem || c.element),
			helper: c.helper,
			position: c.position,
			absolutePosition: c.positionAbs,
			options: this.options,
			element: this.element
		};
	}

});

$.extend($.ui.droppable, {
	version: "1.6rc5",
	eventPrefix: 'drop',
	defaults: {
		accept: '*',
		activeClass: null,
		cssNamespace: 'ui',
		greedy: false,
		hoverClass: null,
		scope: 'default',
		tolerance: 'intersect'
	}
});

$.ui.intersect = function(draggable, droppable, toleranceMode) {

	if (!droppable.offset) return false;

	var x1 = (draggable.positionAbs || draggable.position.absolute).left, x2 = x1 + draggable.helperProportions.width,
		y1 = (draggable.positionAbs || draggable.position.absolute).top, y2 = y1 + draggable.helperProportions.height;
	var l = droppable.offset.left, r = l + droppable.proportions.width,
		t = droppable.offset.top, b = t + droppable.proportions.height;

	switch (toleranceMode) {
		case 'fit':
			return (l < x1 && x2 < r
				&& t < y1 && y2 < b);
			break;
		case 'intersect':
			return (l < x1 + (draggable.helperProportions.width / 2) // Right Half
				&& x2 - (draggable.helperProportions.width / 2) < r // Left Half
				&& t < y1 + (draggable.helperProportions.height / 2) // Bottom Half
				&& y2 - (draggable.helperProportions.height / 2) < b ); // Top Half
			break;
		case 'pointer':
			var draggableLeft = ((draggable.positionAbs || draggable.position.absolute).left + (draggable.clickOffset || draggable.offset.click).left),
				draggableTop = ((draggable.positionAbs || draggable.position.absolute).top + (draggable.clickOffset || draggable.offset.click).top),
				isOver = $.ui.isOver(draggableTop, draggableLeft, t, l, droppable.proportions.height, droppable.proportions.width);
			return isOver;
			break;
		case 'touch':
			return (
					(y1 >= t && y1 <= b) ||	// Top edge touching
					(y2 >= t && y2 <= b) ||	// Bottom edge touching
					(y1 < t && y2 > b)		// Surrounded vertically
				) && (
					(x1 >= l && x1 <= r) ||	// Left edge touching
					(x2 >= l && x2 <= r) ||	// Right edge touching
					(x1 < l && x2 > r)		// Surrounded horizontally
				);
			break;
		default:
			return false;
			break;
		}

};

/*
	This manager tracks offsets of draggables and droppables
*/
$.ui.ddmanager = {
	current: null,
	droppables: { 'default': [] },
	prepareOffsets: function(t, event) {

		var m = $.ui.ddmanager.droppables[t.options.scope];
		var type = event ? event.type : null; // workaround for #2317
		var list = (t.currentItem || t.element).find(":data(droppable)").andSelf();

		droppablesLoop: for (var i = 0; i < m.length; i++) {

			if(m[i].options.disabled || (t && !m[i].options.accept.call(m[i].element,(t.currentItem || t.element)))) continue;	//No disabled and non-accepted
			for (var j=0; j < list.length; j++) { if(list[j] == m[i].element[0]) { m[i].proportions.height = 0; continue droppablesLoop; } }; //Filter out elements in the current dragged item
			m[i].visible = m[i].element.css("display") != "none"; if(!m[i].visible) continue; 									//If the element is not visible, continue

			m[i].offset = m[i].element.offset();
			m[i].proportions = { width: m[i].element[0].offsetWidth, height: m[i].element[0].offsetHeight };

			if(type == "dragstart" || type == "sortactivate") m[i]._activate.call(m[i], event); 										//Activate the droppable if used directly from draggables

		}

	},
	drop: function(draggable, event) {

		var dropped = false;
		$.each($.ui.ddmanager.droppables[draggable.options.scope], function() {

			if(!this.options) return;
			if (!this.options.disabled && this.visible && $.ui.intersect(draggable, this, this.options.tolerance))
				dropped = this._drop.call(this, event);

			if (!this.options.disabled && this.visible && this.options.accept.call(this.element,(draggable.currentItem || draggable.element))) {
				this.isout = 1; this.isover = 0;
				this._deactivate.call(this, event);
			}

		});
		return dropped;

	},
	drag: function(draggable, event) {

		//If you have a highly dynamic page, you might try this option. It renders positions every time you move the mouse.
		if(draggable.options.refreshPositions) $.ui.ddmanager.prepareOffsets(draggable, event);

		//Run through all droppables and check their positions based on specific tolerance options

		$.each($.ui.ddmanager.droppables[draggable.options.scope], function() {

			if(this.options.disabled || this.greedyChild || !this.visible) return;
			var intersects = $.ui.intersect(draggable, this, this.options.tolerance);

			var c = !intersects && this.isover == 1 ? 'isout' : (intersects && this.isover == 0 ? 'isover' : null);
			if(!c) return;

			var parentInstance;
			if (this.options.greedy) {
				var parent = this.element.parents(':data(droppable):eq(0)');
				if (parent.length) {
					parentInstance = $.data(parent[0], 'droppable');
					parentInstance.greedyChild = (c == 'isover' ? 1 : 0);
				}
			}

			// we just moved into a greedy child
			if (parentInstance && c == 'isover') {
				parentInstance['isover'] = 0;
				parentInstance['isout'] = 1;
				parentInstance._out.call(parentInstance, event);
			}

			this[c] = 1; this[c == 'isout' ? 'isover' : 'isout'] = 0;
			this[c == "isover" ? "_over" : "_out"].call(this, event);

			// we just moved out of a greedy child
			if (parentInstance && c == 'isout') {
				parentInstance['isout'] = 0;
				parentInstance['isover'] = 1;
				parentInstance._over.call(parentInstance, event);
			}
		});

	}
};

/*
 * Droppable Extensions
 */

$.ui.plugin.add("droppable", "activeClass", {
	activate: function(event, ui) {
		$(this).addClass(ui.options.activeClass);
	},
	deactivate: function(event, ui) {
		$(this).removeClass(ui.options.activeClass);
	},
	drop: function(event, ui) {
		$(this).removeClass(ui.options.activeClass);
	}
});

$.ui.plugin.add("droppable", "hoverClass", {
	over: function(event, ui) {
		$(this).addClass(ui.options.hoverClass);
	},
	out: function(event, ui) {
		$(this).removeClass(ui.options.hoverClass);
	},
	drop: function(event, ui) {
		$(this).removeClass(ui.options.hoverClass);
	}
});

})(jQuery);


/* - ++resource++jquery.ui/ui/ui.draggable.js - */
/*
 * jQuery UI Draggable 1.6rc5
 *
 * Copyright (c) 2009 AUTHORS.txt (http://ui.jquery.com/about)
 * Dual licensed under the MIT (MIT-LICENSE.txt)
 * and GPL (GPL-LICENSE.txt) licenses.
 *
 * http://docs.jquery.com/UI/Draggables
 *
 * Depends:
 *	ui.core.js
 */
(function($) {

$.widget("ui.draggable", $.extend({}, $.ui.mouse, {

	_init: function() {

		if (this.options.helper == 'original' && !(/^(?:r|a|f)/).test(this.element.css("position")))
			this.element[0].style.position = 'relative';

		(this.options.cssNamespace && this.element.addClass(this.options.cssNamespace+"-draggable"));
		(this.options.disabled && this.element.addClass(this.options.cssNamespace+'-draggable-disabled'));

		this._mouseInit();

	},

	destroy: function() {
		if(!this.element.data('draggable')) return;
		this.element.removeData("draggable").unbind(".draggable").removeClass(this.options.cssNamespace+'-draggable '+this.options.cssNamespace+'-draggable-dragging '+this.options.cssNamespace+'-draggable-disabled');
		this._mouseDestroy();
	},

	_mouseCapture: function(event) {

		var o = this.options;

		if (this.helper || o.disabled || $(event.target).is('.'+this.options.cssNamespace+'-resizable-handle'))
			return false;

		//Quit if we're not on a valid handle
		this.handle = this._getHandle(event);
		if (!this.handle)
			return false;

		return true;

	},

	_mouseStart: function(event) {

		var o = this.options;

		//Create and append the visible helper
		this.helper = this._createHelper(event);

		//Cache the helper size
		this._cacheHelperProportions();

		//If ddmanager is used for droppables, set the global draggable
		if($.ui.ddmanager)
			$.ui.ddmanager.current = this;

		/*
		 * - Position generation -
		 * This block generates everything position related - it's the core of draggables.
		 */

		//Cache the margins of the original element
		this._cacheMargins();

		//Store the helper's css position
		this.cssPosition = this.helper.css("position");
		this.scrollParent = this.helper.scrollParent();

		//The element's absolute position on the page minus margins
		this.offset = this.element.offset();
		this.offset = {
			top: this.offset.top - this.margins.top,
			left: this.offset.left - this.margins.left
		};

		$.extend(this.offset, {
			click: { //Where the click happened, relative to the element
				left: event.pageX - this.offset.left,
				top: event.pageY - this.offset.top
			},
			parent: this._getParentOffset(),
			relative: this._getRelativeOffset() //This is a relative to absolute position minus the actual position calculation - only used for relative positioned helper
		});

		//Generate the original position
		this.originalPosition = this._generatePosition(event);
		this.originalPageX = event.pageX;
		this.originalPageY = event.pageY;

		//Adjust the mouse offset relative to the helper if 'cursorAt' is supplied
		if(o.cursorAt)
			this._adjustOffsetFromHelper(o.cursorAt);

		//Set a containment if given in the options
		if(o.containment)
			this._setContainment();

		//Call plugins and callbacks
		this._trigger("start", event);

		//Recache the helper size
		this._cacheHelperProportions();

		//Prepare the droppable offsets
		if ($.ui.ddmanager && !o.dropBehaviour)
			$.ui.ddmanager.prepareOffsets(this, event);

		this.helper.addClass(o.cssNamespace+"-draggable-dragging");
		this._mouseDrag(event, true); //Execute the drag once - this causes the helper not to be visible before getting its correct position
		return true;
	},

	_mouseDrag: function(event, noPropagation) {

		//Compute the helpers position
		this.position = this._generatePosition(event);
		this.positionAbs = this._convertPositionTo("absolute");

		//Call plugins and callbacks and use the resulting position if something is returned
		if (!noPropagation) {
			var ui = this._uiHash();
			this._trigger('drag', event, ui);
			this.position = ui.position;
		}

		if(!this.options.axis || this.options.axis != "y") this.helper[0].style.left = this.position.left+'px';
		if(!this.options.axis || this.options.axis != "x") this.helper[0].style.top = this.position.top+'px';
		if($.ui.ddmanager) $.ui.ddmanager.drag(this, event);

		return false;
	},

	_mouseStop: function(event) {

		//If we are using droppables, inform the manager about the drop
		var dropped = false;
		if ($.ui.ddmanager && !this.options.dropBehaviour)
			dropped = $.ui.ddmanager.drop(this, event);
		
		//if a drop comes from outside (a sortable)
		if(this.dropped) {
			dropped = this.dropped;
			this.dropped = false;
		}

		if((this.options.revert == "invalid" && !dropped) || (this.options.revert == "valid" && dropped) || this.options.revert === true || ($.isFunction(this.options.revert) && this.options.revert.call(this.element, dropped))) {
			var self = this;
			$(this.helper).animate(this.originalPosition, parseInt(this.options.revertDuration, 10), function() {
				self._trigger("stop", event);
				self._clear();
			});
		} else {
			this._trigger("stop", event);
			this._clear();
		}

		return false;
	},

	_getHandle: function(event) {

		var handle = !this.options.handle || !$(this.options.handle, this.element).length ? true : false;
		$(this.options.handle, this.element)
			.find("*")
			.andSelf()
			.each(function() {
				if(this == event.target) handle = true;
			});

		return handle;

	},

	_createHelper: function(event) {

		var o = this.options;
		var helper = $.isFunction(o.helper) ? $(o.helper.apply(this.element[0], [event])) : (o.helper == 'clone' ? this.element.clone() : this.element);

		if(!helper.parents('body').length)
			helper.appendTo((o.appendTo == 'parent' ? this.element[0].parentNode : o.appendTo));

		if(helper[0] != this.element[0] && !(/(fixed|absolute)/).test(helper.css("position")))
			helper.css("position", "absolute");

		return helper;

	},

	_adjustOffsetFromHelper: function(obj) {
		if(obj.left != undefined) this.offset.click.left = obj.left + this.margins.left;
		if(obj.right != undefined) this.offset.click.left = this.helperProportions.width - obj.right + this.margins.left;
		if(obj.top != undefined) this.offset.click.top = obj.top + this.margins.top;
		if(obj.bottom != undefined) this.offset.click.top = this.helperProportions.height - obj.bottom + this.margins.top;
	},

	_getParentOffset: function() {

		//Get the offsetParent and cache its position
		this.offsetParent = this.helper.offsetParent();
		var po = this.offsetParent.offset();
		
		// This is a special case where we need to modify a offset calculated on start, since the following happened:
		// 1. The position of the helper is absolute, so it's position is calculated based on the next positioned parent
		// 2. The actual offset parent is a child of the scroll parent, and the scroll parent isn't the document, which means that
		//    the scroll is included in the initial calculation of the offset of the parent, and never recalculated upon drag
		if(this.cssPosition == 'absolute' && this.scrollParent[0] != document && $.ui.contains(this.scrollParent[0], this.offsetParent[0])) {
			po.left += this.scrollParent.scrollLeft();
			po.top += this.scrollParent.scrollTop();
		}

		if((this.offsetParent[0] == document.body && $.browser.mozilla)	//Ugly FF3 fix
		|| (this.offsetParent[0].tagName && this.offsetParent[0].tagName.toLowerCase() == 'html' && $.browser.msie)) //Ugly IE fix
			po = { top: 0, left: 0 };

		return {
			top: po.top + (parseInt(this.offsetParent.css("borderTopWidth"),10) || 0),
			left: po.left + (parseInt(this.offsetParent.css("borderLeftWidth"),10) || 0)
		};

	},

	_getRelativeOffset: function() {

		if(this.cssPosition == "relative") {
			var p = this.element.position();
			return {
				top: p.top - (parseInt(this.helper.css("top"),10) || 0) + this.scrollParent.scrollTop(),
				left: p.left - (parseInt(this.helper.css("left"),10) || 0) + this.scrollParent.scrollLeft()
			};
		} else {
			return { top: 0, left: 0 };
		}

	},

	_cacheMargins: function() {
		this.margins = {
			left: (parseInt(this.element.css("marginLeft"),10) || 0),
			top: (parseInt(this.element.css("marginTop"),10) || 0)
		};
	},

	_cacheHelperProportions: function() {
		this.helperProportions = {
			width: this.helper.outerWidth(),
			height: this.helper.outerHeight()
		};
	},

	_setContainment: function() {

		var o = this.options;
		if(o.containment == 'parent') o.containment = this.helper[0].parentNode;
		if(o.containment == 'document' || o.containment == 'window') this.containment = [
			0 - this.offset.relative.left - this.offset.parent.left,
			0 - this.offset.relative.top - this.offset.parent.top,
			$(o.containment == 'document' ? document : window).width() - this.helperProportions.width - this.margins.left,
			($(o.containment == 'document' ? document : window).height() || document.body.parentNode.scrollHeight) - this.helperProportions.height - this.margins.top
		];

		if(!(/^(document|window|parent)$/).test(o.containment)) {
			var ce = $(o.containment)[0];
			var co = $(o.containment).offset();
			var over = ($(ce).css("overflow") != 'hidden');

			this.containment = [
				co.left + (parseInt($(ce).css("borderLeftWidth"),10) || 0) - this.margins.left,
				co.top + (parseInt($(ce).css("borderTopWidth"),10) || 0) - this.margins.top,
				co.left+(over ? Math.max(ce.scrollWidth,ce.offsetWidth) : ce.offsetWidth) - (parseInt($(ce).css("borderLeftWidth"),10) || 0) - this.helperProportions.width - this.margins.left,
				co.top+(over ? Math.max(ce.scrollHeight,ce.offsetHeight) : ce.offsetHeight) - (parseInt($(ce).css("borderTopWidth"),10) || 0) - this.helperProportions.height - this.margins.top
			];
		}

	},

	_convertPositionTo: function(d, pos) {

		if(!pos) pos = this.position;
		var mod = d == "absolute" ? 1 : -1;
		var o = this.options, scroll = this.cssPosition == 'absolute' && !(this.scrollParent[0] != document && $.ui.contains(this.scrollParent[0], this.offsetParent[0])) ? this.offsetParent : this.scrollParent, scrollIsRootNode = (/(html|body)/i).test(scroll[0].tagName);

		return {
			top: (
				pos.top																	// The absolute mouse position
				+ this.offset.relative.top * mod										// Only for relative positioned nodes: Relative offset from element to offset parent
				+ this.offset.parent.top * mod											// The offsetParent's offset without borders (offset + border)
				- ( this.cssPosition == 'fixed' ? -this.scrollParent.scrollTop() : ( scrollIsRootNode ? 0 : scroll.scrollTop() ) ) * mod
			),
			left: (
				pos.left																// The absolute mouse position
				+ this.offset.relative.left * mod										// Only for relative positioned nodes: Relative offset from element to offset parent
				+ this.offset.parent.left * mod											// The offsetParent's offset without borders (offset + border)
				- ( this.cssPosition == 'fixed' ? -this.scrollParent.scrollLeft() : scrollIsRootNode ? 0 : scroll.scrollLeft() ) * mod
			)
		};
		
	},

	_generatePosition: function(event) {

		var o = this.options, scroll = this.cssPosition == 'absolute' && !(this.scrollParent[0] != document && $.ui.contains(this.scrollParent[0], this.offsetParent[0])) ? this.offsetParent : this.scrollParent, scrollIsRootNode = (/(html|body)/i).test(scroll[0].tagName);

		// This is another very weird special case that only happens for relative elements:
		// 1. If the css position is relative
		// 2. and the scroll parent is the document or similar to the offset parent
		// we have to refresh the relative offset during the scroll so there are no jumps
		if(this.cssPosition == 'relative' && !(this.scrollParent[0] != document && this.scrollParent[0] != this.offsetParent[0])) {
			this.offset.relative = this._getRelativeOffset();
		}
		
		var pageX = event.pageX;
		var pageY = event.pageY;

		/*
		 * - Position constraining -
		 * Constrain the position to a mix of grid, containment.
		 */
		 
		if(this.originalPosition) { //If we are not dragging yet, we won't check for options

			if(this.containment) {
				if(event.pageX - this.offset.click.left < this.containment[0]) pageX = this.containment[0] + this.offset.click.left;
				if(event.pageY - this.offset.click.top < this.containment[1]) pageY = this.containment[1] + this.offset.click.top;
				if(event.pageX - this.offset.click.left > this.containment[2]) pageX = this.containment[2] + this.offset.click.left;
				if(event.pageY - this.offset.click.top > this.containment[3]) pageY = this.containment[3] + this.offset.click.top;
			}
			
			if(o.grid) {
				var top = this.originalPageY + Math.round((pageY - this.originalPageY) / o.grid[1]) * o.grid[1];
				pageY = this.containment ? (!(top - this.offset.click.top < this.containment[1] || top - this.offset.click.top > this.containment[3]) ? top : (!(top - this.offset.click.top < this.containment[1]) ? top - o.grid[1] : top + o.grid[1])) : top;

				var left = this.originalPageX + Math.round((pageX - this.originalPageX) / o.grid[0]) * o.grid[0];
				pageX = this.containment ? (!(left - this.offset.click.left < this.containment[0] || left - this.offset.click.left > this.containment[2]) ? left : (!(left - this.offset.click.left < this.containment[0]) ? left - o.grid[0] : left + o.grid[0])) : left;
			}

		}

		return {
			top: (
				pageY																// The absolute mouse position
				- this.offset.click.top													// Click offset (relative to the element)
				- this.offset.relative.top												// Only for relative positioned nodes: Relative offset from element to offset parent
				- this.offset.parent.top												// The offsetParent's offset without borders (offset + border)
				+ ( this.cssPosition == 'fixed' ? -this.scrollParent.scrollTop() : ( scrollIsRootNode ? 0 : scroll.scrollTop() ) )
			),
			left: (
				pageX																// The absolute mouse position
				- this.offset.click.left												// Click offset (relative to the element)
				- this.offset.relative.left												// Only for relative positioned nodes: Relative offset from element to offset parent
				- this.offset.parent.left												// The offsetParent's offset without borders (offset + border)
				+ ( this.cssPosition == 'fixed' ? -this.scrollParent.scrollLeft() : scrollIsRootNode ? 0 : scroll.scrollLeft() )
			)
		};

	},

	_clear: function() {
		this.helper.removeClass(this.options.cssNamespace+"-draggable-dragging");
		if(this.helper[0] != this.element[0] && !this.cancelHelperRemoval) this.helper.remove();
		//if($.ui.ddmanager) $.ui.ddmanager.current = null;
		this.helper = null;
		this.cancelHelperRemoval = false;
	},

	// From now on bulk stuff - mainly helpers

	_trigger: function(type, event, ui) {
		ui = ui || this._uiHash();
		$.ui.plugin.call(this, type, [event, ui]);
		if(type == "drag") this.positionAbs = this._convertPositionTo("absolute"); //The absolute position has to be recalculated after plugins
		return $.widget.prototype._trigger.call(this, type, event, ui);
	},

	plugins: {},

	_uiHash: function(event) {
		return {
			helper: this.helper,
			position: this.position,
			absolutePosition: this.positionAbs,
			options: this.options
		};
	}

}));

$.extend($.ui.draggable, {
	version: "1.6rc5",
	eventPrefix: "drag",
	defaults: {
		appendTo: "parent",
		axis: false,
		cancel: ":input,option",
		connectToSortable: false,
		containment: false,
		cssNamespace: "ui",
		cursor: "default",
		cursorAt: null,
		delay: 0,
		distance: 1,
		grid: false,
		handle: false,
		helper: "original",
		iframeFix: false,
		opacity: null,
		refreshPositions: false,
		revert: false,
		revertDuration: 500,
		scope: "default",
		scroll: true,
		scrollSensitivity: 20,
		scrollSpeed: 20,
		snap: false,
		snapMode: "both",
		snapTolerance: 20,
		stack: false,
		zIndex: null
	}
});

$.ui.plugin.add("draggable", "connectToSortable", {
	start: function(event, ui) {

		var inst = $(this).data("draggable");
		inst.sortables = [];
		$(ui.options.connectToSortable).each(function() {
			// 'this' points to a string, and should therefore resolved as query, but instead, if the string is assigned to a variable, it loops through the strings properties,
			// so we have to append '' to make it anonymous again
			$(this+'').each(function() {
				if($.data(this, 'sortable')) {
					var sortable = $.data(this, 'sortable');
					inst.sortables.push({
						instance: sortable,
						shouldRevert: sortable.options.revert
					});
					sortable._refreshItems();	//Do a one-time refresh at start to refresh the containerCache
					sortable._trigger("activate", event, inst);
				}
			});
		});

	},
	stop: function(event, ui) {

		//If we are still over the sortable, we fake the stop event of the sortable, but also remove helper
		var inst = $(this).data("draggable");

		$.each(inst.sortables, function() {
			if(this.instance.isOver) {
				
				this.instance.isOver = 0;
				
				inst.cancelHelperRemoval = true; //Don't remove the helper in the draggable instance
				this.instance.cancelHelperRemoval = false; //Remove it in the sortable instance (so sortable plugins like revert still work)
				
				//The sortable revert is supported, and we have to set a temporary dropped variable on the draggable to support revert: 'valid/invalid'
				if(this.shouldRevert) this.instance.options.revert = true;
				
				//Trigger the stop of the sortable
				this.instance._mouseStop(event);

				//Also propagate receive event, since the sortable is actually receiving a element
				this.instance.element.triggerHandler("sortreceive", [event, $.extend(this.instance._uiHash(), { sender: inst.element })], this.instance.options["receive"]);

				this.instance.options.helper = this.instance.options._helper;

				//If the helper has been the original item, restore properties in the sortable
				if(inst.options.helper == 'original')
					this.instance.currentItem.css({ top: 'auto', left: 'auto' });

			} else {
				this.instance.cancelHelperRemoval = false; //Remove the helper in the sortable instance
				this.instance._trigger("deactivate", event, inst);
			}

		});

	},
	drag: function(event, ui) {

		var inst = $(this).data("draggable"), self = this;

		var checkPos = function(o) {
			var dyClick = this.offset.click.top, dxClick = this.offset.click.left;
			var helperTop = this.positionAbs.top, helperLeft = this.positionAbs.left;
			var itemHeight = o.height, itemWidth = o.width;
			var itemTop = o.top, itemLeft = o.left;

			return $.ui.isOver(helperTop + dyClick, helperLeft + dxClick, itemTop, itemLeft, itemHeight, itemWidth);
		};

		$.each(inst.sortables, function(i) {

			if(checkPos.call(inst, this.instance.containerCache)) {

				//If it intersects, we use a little isOver variable and set it once, so our move-in stuff gets fired only once
				if(!this.instance.isOver) {
					this.instance.isOver = 1;
					//Now we fake the start of dragging for the sortable instance,
					//by cloning the list group item, appending it to the sortable and using it as inst.currentItem
					//We can then fire the start event of the sortable with our passed browser event, and our own helper (so it doesn't create a new one)
					this.instance.currentItem = $(self).clone().appendTo(this.instance.element).data("sortable-item", true);
					this.instance.options._helper = this.instance.options.helper; //Store helper option to later restore it
					this.instance.options.helper = function() { return ui.helper[0]; };

					event.target = this.instance.currentItem[0];
					this.instance._mouseCapture(event, true);
					this.instance._mouseStart(event, true, true);

					//Because the browser event is way off the new appended portlet, we modify a couple of variables to reflect the changes
					this.instance.offset.click.top = inst.offset.click.top;
					this.instance.offset.click.left = inst.offset.click.left;
					this.instance.offset.parent.left -= inst.offset.parent.left - this.instance.offset.parent.left;
					this.instance.offset.parent.top -= inst.offset.parent.top - this.instance.offset.parent.top;

					inst._trigger("toSortable", event);
					inst.dropped = this.instance.element; //draggable revert needs that
					this.instance.fromOutside = true; //Little hack so receive/update callbacks work

				}

				//Provided we did all the previous steps, we can fire the drag event of the sortable on every draggable drag, when it intersects with the sortable
				if(this.instance.currentItem) this.instance._mouseDrag(event);

			} else {

				//If it doesn't intersect with the sortable, and it intersected before,
				//we fake the drag stop of the sortable, but make sure it doesn't remove the helper by using cancelHelperRemoval
				if(this.instance.isOver) {
					this.instance.isOver = 0;
					this.instance.cancelHelperRemoval = true;
					this.instance.options.revert = false; //No revert here
					this.instance._mouseStop(event, true);
					this.instance.options.helper = this.instance.options._helper;

					//Now we remove our currentItem, the list group clone again, and the placeholder, and animate the helper back to it's original size
					this.instance.currentItem.remove();
					if(this.instance.placeholder) this.instance.placeholder.remove();

					inst._trigger("fromSortable", event);
					inst.dropped = false; //draggable revert needs that
				}

			};

		});

	}
});

$.ui.plugin.add("draggable", "cursor", {
	start: function(event, ui) {
		var t = $('body');
		if (t.css("cursor")) ui.options._cursor = t.css("cursor");
		t.css("cursor", ui.options.cursor);
	},
	stop: function(event, ui) {
		if (ui.options._cursor) $('body').css("cursor", ui.options._cursor);
	}
});

$.ui.plugin.add("draggable", "iframeFix", {
	start: function(event, ui) {
		$(ui.options.iframeFix === true ? "iframe" : ui.options.iframeFix).each(function() {
			$('<div class="ui-draggable-iframeFix" style="background: #fff;"></div>')
			.css({
				width: this.offsetWidth+"px", height: this.offsetHeight+"px",
				position: "absolute", opacity: "0.001", zIndex: 1000
			})
			.css($(this).offset())
			.appendTo("body");
		});
	},
	stop: function(event, ui) {
		$("div.ui-draggable-iframeFix").each(function() { this.parentNode.removeChild(this); }); //Remove frame helpers
	}
});

$.ui.plugin.add("draggable", "opacity", {
	start: function(event, ui) {
		var t = $(ui.helper);
		if(t.css("opacity")) ui.options._opacity = t.css("opacity");
		t.css('opacity', ui.options.opacity);
	},
	stop: function(event, ui) {
		if(ui.options._opacity) $(ui.helper).css('opacity', ui.options._opacity);
	}
});

$.ui.plugin.add("draggable", "scroll", {
	start: function(event, ui) {
		var o = ui.options;
		var i = $(this).data("draggable");

		if(i.scrollParent[0] != document && i.scrollParent[0].tagName != 'HTML') i.overflowOffset = i.scrollParent.offset();

	},
	drag: function(event, ui) {

		var o = ui.options, scrolled = false;
		var i = $(this).data("draggable");

		if(i.scrollParent[0] != document && i.scrollParent[0].tagName != 'HTML') {

			if((i.overflowOffset.top + i.scrollParent[0].offsetHeight) - event.pageY < o.scrollSensitivity)
				i.scrollParent[0].scrollTop = scrolled = i.scrollParent[0].scrollTop + o.scrollSpeed;
			else if(event.pageY - i.overflowOffset.top < o.scrollSensitivity)
				i.scrollParent[0].scrollTop = scrolled = i.scrollParent[0].scrollTop - o.scrollSpeed;

			if((i.overflowOffset.left + i.scrollParent[0].offsetWidth) - event.pageX < o.scrollSensitivity)
				i.scrollParent[0].scrollLeft = scrolled = i.scrollParent[0].scrollLeft + o.scrollSpeed;
			else if(event.pageX - i.overflowOffset.left < o.scrollSensitivity)
				i.scrollParent[0].scrollLeft = scrolled = i.scrollParent[0].scrollLeft - o.scrollSpeed;

		} else {

			if(event.pageY - $(document).scrollTop() < o.scrollSensitivity)
				scrolled = $(document).scrollTop($(document).scrollTop() - o.scrollSpeed);
			else if($(window).height() - (event.pageY - $(document).scrollTop()) < o.scrollSensitivity)
				scrolled = $(document).scrollTop($(document).scrollTop() + o.scrollSpeed);

			if(event.pageX - $(document).scrollLeft() < o.scrollSensitivity)
				scrolled = $(document).scrollLeft($(document).scrollLeft() - o.scrollSpeed);
			else if($(window).width() - (event.pageX - $(document).scrollLeft()) < o.scrollSensitivity)
				scrolled = $(document).scrollLeft($(document).scrollLeft() + o.scrollSpeed);

		}

		if(scrolled !== false && $.ui.ddmanager && !o.dropBehaviour)
			$.ui.ddmanager.prepareOffsets(i, event);

	}
});

$.ui.plugin.add("draggable", "snap", {
	start: function(event, ui) {

		var inst = $(this).data("draggable");
		inst.snapElements = [];

		$(ui.options.snap.constructor != String ? ( ui.options.snap.items || ':data(draggable)' ) : ui.options.snap).each(function() {
			var $t = $(this); var $o = $t.offset();
			if(this != inst.element[0]) inst.snapElements.push({
				item: this,
				width: $t.outerWidth(), height: $t.outerHeight(),
				top: $o.top, left: $o.left
			});
		});

	},
	drag: function(event, ui) {

		var inst = $(this).data("draggable");
		var d = ui.options.snapTolerance;

		var x1 = ui.absolutePosition.left, x2 = x1 + inst.helperProportions.width,
			y1 = ui.absolutePosition.top, y2 = y1 + inst.helperProportions.height;

		for (var i = inst.snapElements.length - 1; i >= 0; i--){

			var l = inst.snapElements[i].left, r = l + inst.snapElements[i].width,
				t = inst.snapElements[i].top, b = t + inst.snapElements[i].height;

			//Yes, I know, this is insane ;)
			if(!((l-d < x1 && x1 < r+d && t-d < y1 && y1 < b+d) || (l-d < x1 && x1 < r+d && t-d < y2 && y2 < b+d) || (l-d < x2 && x2 < r+d && t-d < y1 && y1 < b+d) || (l-d < x2 && x2 < r+d && t-d < y2 && y2 < b+d))) {
				if(inst.snapElements[i].snapping) (inst.options.snap.release && inst.options.snap.release.call(inst.element, event, $.extend(inst._uiHash(), { snapItem: inst.snapElements[i].item })));
				inst.snapElements[i].snapping = false;
				continue;
			}

			if(ui.options.snapMode != 'inner') {
				var ts = Math.abs(t - y2) <= d;
				var bs = Math.abs(b - y1) <= d;
				var ls = Math.abs(l - x2) <= d;
				var rs = Math.abs(r - x1) <= d;
				if(ts) ui.position.top = inst._convertPositionTo("relative", { top: t - inst.helperProportions.height, left: 0 }).top;
				if(bs) ui.position.top = inst._convertPositionTo("relative", { top: b, left: 0 }).top;
				if(ls) ui.position.left = inst._convertPositionTo("relative", { top: 0, left: l - inst.helperProportions.width }).left;
				if(rs) ui.position.left = inst._convertPositionTo("relative", { top: 0, left: r }).left;
			}

			var first = (ts || bs || ls || rs);

			if(ui.options.snapMode != 'outer') {
				var ts = Math.abs(t - y1) <= d;
				var bs = Math.abs(b - y2) <= d;
				var ls = Math.abs(l - x1) <= d;
				var rs = Math.abs(r - x2) <= d;
				if(ts) ui.position.top = inst._convertPositionTo("relative", { top: t, left: 0 }).top;
				if(bs) ui.position.top = inst._convertPositionTo("relative", { top: b - inst.helperProportions.height, left: 0 }).top;
				if(ls) ui.position.left = inst._convertPositionTo("relative", { top: 0, left: l }).left;
				if(rs) ui.position.left = inst._convertPositionTo("relative", { top: 0, left: r - inst.helperProportions.width }).left;
			}

			if(!inst.snapElements[i].snapping && (ts || bs || ls || rs || first))
				(inst.options.snap.snap && inst.options.snap.snap.call(inst.element, event, $.extend(inst._uiHash(), { snapItem: inst.snapElements[i].item })));
			inst.snapElements[i].snapping = (ts || bs || ls || rs || first);

		};

	}
});

$.ui.plugin.add("draggable", "stack", {
	start: function(event, ui) {
		var group = $.makeArray($(ui.options.stack.group)).sort(function(a,b) {
			return (parseInt($(a).css("zIndex"),10) || ui.options.stack.min) - (parseInt($(b).css("zIndex"),10) || ui.options.stack.min);
		});

		$(group).each(function(i) {
			this.style.zIndex = ui.options.stack.min + i;
		});

		this[0].style.zIndex = ui.options.stack.min + group.length;
	}
});

$.ui.plugin.add("draggable", "zIndex", {
	start: function(event, ui) {
		var t = $(ui.helper);
		if(t.css("zIndex")) ui.options._zIndex = t.css("zIndex");
		t.css('zIndex', ui.options.zIndex);
	},
	stop: function(event, ui) {
		if(ui.options._zIndex) $(ui.helper).css('zIndex', ui.options._zIndex);
	}
});

})(jQuery);


/* - jquery-integration.js - */
// http://osha.europa.eu/portal_javascripts/jquery-integration.js?original=1
var jq=jQuery.noConflict();if(typeof cssQuery=='undefined'){
function cssQuery(s,f){return jq.makeArray(jq(s,f))}};

/* - event-registration.js - */
// http://osha.europa.eu/portal_javascripts/event-registration.js?original=1
function addDOMLoadEvent(listener){jQuery(listener)}


/* - register_function.js - */
// http://osha.europa.eu/portal_javascripts/register_function.js?original=1
var bugRiddenCrashPronePieceOfJunk=(navigator.userAgent.indexOf('MSIE 5')!=-1&&navigator.userAgent.indexOf('Mac')!=-1)
var W3CDOM=(!bugRiddenCrashPronePieceOfJunk&&typeof document.getElementsByTagName!='undefined'&&typeof document.createElement!='undefined');var registerEventListener=function(elem,event,func){jq(elem).bind(event,func)}
var unRegisterEventListener=function(elem,event,func){jq(elem).unbind(event,func)}
var registerPloneFunction=jq;
function getContentArea(){var node=jq('#region-content,#content');return node.length?node[0]:null}


/* - plone_javascript_variables.js - */
// http://osha.europa.eu/portal_javascripts/plone_javascript_variables.js?original=1
var portal_url='http://osha.europa.eu';var form_modified_message='Your form has not been saved. All changes you have made will be lost.';var form_resubmit_message='You already clicked the submit button. Do you really want to submit this form again?';var external_links_open_new_window='true';var mark_special_links='true';

/* - nodeutilities.js - */
// http://osha.europa.eu/portal_javascripts/nodeutilities.js?original=1
function wrapNode(node,wrappertype,wrapperclass){jq(node).wrap('<'+wrappertype+'>').parent().addClass(wrapperclass)};
function nodeContained(innernode,outernode){return jq(innernode).parents().filter(function(){return this==outernode}).length>0};
function findContainer(node,func){p=jq(node).parents().filter(func);return p.length?p.get(0):false};
function hasClassName(node,class_name){return jq(node).hasClass(class_name)};
function addClassName(node,class_name){jq(node).addClass(class_name)};
function removeClassName(node,class_name){jq(node).removeClass(class_name)};
function replaceClassName(node,old_class,new_class,ignore_missing){if(ignore_missing||jq(node).hasClass(old_class))
jq(node).removeClass(old_class).addClass(new_class)};
function walkTextNodes(node,func,data){jq(node).find('*').andSelf().contents().each(function(){if(this.nodeType==3) func(this,data)})};
function getInnerTextCompatible(node){return jq(node).text()};
function getInnerTextFast(node){return jq(node).text()};
function sortNodes(nodes,fetch_func,cmp_func){var SortNodeWrapper=function(node){this.value=fetch_func(node);this.cloned_node=node.cloneNode(true)}
SortNodeWrapper.prototype.toString=function(){return this.value.toString?this.value.toString():this.value}
var items=jq(nodes).map(function(){return new SortNodeWrapper(this)});if(cmp_func) items.sort(cmp_func);else items.sort();jq.each(items, function(i){jq(nodes[i]).replace(this.cloned_node)})};
function copyChildNodes(srcNode,dstNode){jq(srcNode).children().clone().appendTo(jq(dstNode))}


/* - cookie_functions.js - */
// http://osha.europa.eu/portal_javascripts/cookie_functions.js?original=1
function createCookie(name,value,days){if(days){var date=new Date();date.setTime(date.getTime()+(days*24*60*60*1000));var expires="; expires="+date.toGMTString()} else{expires=""}
document.cookie=name+"="+escape(value)+expires+"; path=/;"};
function readCookie(name){var nameEQ=name+"=";var ca=document.cookie.split(';');for(var i=0;i<ca.length;i++){var c=ca[i];while(c.charAt(0)==' '){c=c.substring(1,c.length)}
if(c.indexOf(nameEQ)==0){return unescape(c.substring(nameEQ.length,c.length))}}
return null};

/* - livesearch.js - */
// http://osha.europa.eu/portal_javascripts/livesearch.js?original=1
var livesearch=function(){var _2=400;var _7=400;var _0={};var _1="LSHighlight";function _5(f,i){var l=null;var r=null;var c={};var q="livesearch_reply";if(typeof portal_url!="undefined")q=portal_url+"/"+q;var re=f.find('div.LSResult');var s=f.find('div.LSShadow');var p=f.find('input[name=path]');function _12(){re.hide();l=null};function _6(){window.setTimeout('livesearch.hide("'+f.attr('id')+'")',_7)};function _11(d){re.show();s.html(d)};function _14(){if(l==i.value){return}l=i.value;if(r&&r.readyState<4)r.abort();if(i.value.length<2){_12();return}var qu={q:i.value};qu['name']=i.name;if(p.length&&p[0].checked)qu['path']=p.val();qu=jq.param(qu);if(c[qu]){_11(c[qu]);return}r=jq.get(q,qu,function(d){_11(d);c[qu]=d},'text')};function _4(){window.setTimeout('livesearch.search("'+f.attr('id')+'")',_2)};return{hide:_12,hide_delayed:_6,search:_14,search_delayed:_4}};function _3(f){var t=null;var re=f.find('div.LSResult');var s=f.find('div.LSShadow');function _16(){c=s.find('li.LSHighlight').removeClass(_1);p=c.prev('li');if(!p.length)p=s.find('li:last');p.addClass(_1);return false};function _9(){c=s.find('li.LSHighlight').removeClass(_1);n=c.next('li');if(!n.length)n=s.find('li:first');n.addClass(_1);return false};function _8(){s.find('li.LSHighlight').removeClass(_1);re.hide()};function _10(e){window.clearTimeout(t);switch(e.keyCode){case 38:return _16();case 40:return _9();case 27:return _8();case 37:break;case 39:break;default:{t=window.setTimeout('livesearch.search("'+f.attr('id')+'")',_2)}}};function _13(){var t=s.find('li.LSHighlight a').attr('href');if(!t)return;window.location=t;return false};return{handler:_10,submit:_13}};function _15(i){var i='livesearch'+i;var f=jq(this).parents('form:first');var k=_3(f);_0[i]=_5(f,this);f.attr('id',i).css('white-space','nowrap').submit(k.submit);jq(this).attr('autocomplete','off').keydown(k.handler).focus(_0[i].search_delayed).blur(_0[i].hide_delayed)};jq(function(){jq("#searchGadget,input.portlet-search-gadget").each(_15)});return{search:function(id){_0[id].search()},hide:function(id){_0[id].hide()}}}();

/* - select_all.js - */
// http://osha.europa.eu/portal_javascripts/select_all.js?original=1
function toggleSelect(selectbutton,id,initialState,formName){id=id||'ids:list'
var state=selectbutton.isSelected;state=state==null?Boolean(initialState):state;selectbutton.isSelected=!state;jq(selectbutton).attr('src',portal_url+'/select_'+(state?'all':'none')+'_icon.gif');var base=formName?jq(document.forms[formName]):jq(document);base.find(':checkbox[name='+id+']').attr('checked',!state)}


/* - dragdropreorder.js - */
// http://osha.europa.eu/portal_javascripts/dragdropreorder.js?original=1
var ploneDnDReorder={};ploneDnDReorder.dragging=null;ploneDnDReorder.table=null;ploneDnDReorder.rows=null;ploneDnDReorder.doDown=function(e){var dragging=jq(this).parents('.draggable:first');if(!dragging.length) return;ploneDnDReorder.rows.mousemove(ploneDnDReorder.doDrag);ploneDnDReorder.dragging=dragging;dragging._position=ploneDnDReorder.getPos(dragging);dragging.addClass("dragging");return false};ploneDnDReorder.getPos=function(node){var pos=node.parent().children('.draggable').index(node[0]);return pos==-1?null:pos};ploneDnDReorder.doDrag=function(e){var dragging=ploneDnDReorder.dragging;if(!dragging) return;var target=this;if(!target) return;if(jq(target).attr('id')!=dragging.attr('id')){ploneDnDReorder.swapElements(jq(target),dragging)};return false};ploneDnDReorder.swapElements=function(child1,child2){var parent=child1.parent();var items=parent.children('[id]');items.removeClass('even').removeClass('odd');if(child1[0].swapNode){child1[0].swapNode(child2[0])} else{var t=parent[0].insertBefore(document.createTextNode(''),child1[0]);child1.insertBefore(child2);child2.insertBefore(t);jq(t).remove()};parent.children('[id]:odd').addClass('even');parent.children('[id]:even').addClass('odd')};ploneDnDReorder.doUp=function(e){var dragging=ploneDnDReorder.dragging;if(!dragging) return;dragging.removeClass("dragging");ploneDnDReorder.updatePositionOnServer();dragging._position=null;try{delete dragging._position} catch(e){};dragging=null;ploneDnDReorder.rows.unbind('mousemove',ploneDnDReorder.doDrag);return false};ploneDnDReorder.updatePositionOnServer=function(){var dragging=ploneDnDReorder.dragging;if(!dragging) return;var delta=ploneDnDReorder.getPos(dragging)-dragging._position;if(delta==0){return};var args={item_id:dragging.attr('id').substr('folder-contents-item-'.length)};args['delta:int']=delta;jQuery.post('folder_moveitem',args)};

/* - mark_special_links.js - */
// http://osha.europa.eu/portal_javascripts/mark_special_links.js?original=1
function scanforlinks(){if(typeof external_links_open_new_window=='string')
var elonw=external_links_open_new_window.toLowerCase()=='true';else elonw=false;if(typeof mark_special_links=='string')
var mslinks=mark_special_links.toLowerCase()=='true';else mslinks=false;var url=window.location.protocol+'//'+window.location.host;if(elonw)
jq('a[href^=http]:not(.link-plain):not([href^='+url+'])').attr('target','_blank');if(mslinks){var protocols=/^(mailto|ftp|news|irc|h323|sip|callto|https|feed|webcal)/;var contentarea=jq(getContentArea());contentarea.find('a[href^=http]:not(.link-plain):not([href^='+url+']):not(:has(img))').wrap('<span></span>').parent().addClass('link-external')
contentarea.find('a[href]:not([href^=http]):not(.link-plain):not([href^='+url+']):not(:has(img))').each(function(){if(res=protocols.exec(this.href))
jq(this).wrap('<span></span>').parent().addClass('link-'+res[0])})}};jq(scanforlinks);

/* - collapsiblesections.js - */
// http://osha.europa.eu/portal_javascripts/collapsiblesections.js?original=1
function activateCollapsibles(){jq('dl.collapsible:not([class$=Collapsible])').find('dt.collapsibleHeader:first').click(function(){var c=jq(this).parents('dl.collapsible:first');if(!c)return true;var t=c.hasClass('inline')?'Inline':'Block';c.toggleClass('collapsed'+t+'Collapsible').toggleClass('expanded'+t+'Collapsible')}).end().each(function(){var s=jq(this).hasClass('collapsedOnLoad')?'collapsed':'expanded';var t=jq(this).hasClass('inline')?'Inline':'Block';jq(this).removeClass('collapsedOnLoad').addClass(s+t+'Collapsible')})};jq(activateCollapsibles);

/* - form_tabbing.js - */
// http://osha.europa.eu/portal_javascripts/form_tabbing.js?original=1
var ploneFormTabbing={};ploneFormTabbing._toggleFactory=function(container,tab_ids,panel_ids){return function(e){jq(tab_ids).removeClass('selected');jq(panel_ids).addClass('hidden');var orig_id=this.tagName.toLowerCase()=='a'?'#'+this.id:jq(this).val();var id=orig_id.replace(/^#fieldsetlegend-/,"#fieldset-");jq(orig_id).addClass('selected');jq(id).removeClass('hidden');jq(container).find("input[name=fieldset.current]").val(orig_id);return false}};ploneFormTabbing._buildTabs=function(container,legends){var threshold=6;var tab_ids=[];var panel_ids=[];legends.each(function(i){tab_ids[i]='#'+this.id;panel_ids[i]=tab_ids[i].replace(/^#fieldsetlegend-/,"#fieldset-")});var handler=ploneFormTabbing._toggleFactory(container,tab_ids.join(','),panel_ids.join(','));if(legends.length>threshold){var tabs=document.createElement("select");var tabtype='option';jq(tabs).change(handler).addClass('noUnloadProtection')} else{var tabs=document.createElement("ul");var tabtype='li'}
jq(tabs).addClass('formTabs');legends.each(function(){var tab=document.createElement(tabtype);jq(tab).addClass('formTab');if(legends.length>threshold){jq(tab).text(jq(this).text());tab.id=this.id;tab.value='#'+this.id} else{var a=document.createElement("a");a.id=this.id;a.href="#"+this.id;jq(a).click(handler);var span=document.createElement("span");jq(span).text(jq(this).text());a.appendChild(span);tab.appendChild(a)}
tabs.appendChild(tab);jq(this).remove()});jq(tabs).children(':first').addClass('firstFormTab');jq(tabs).children(':last').addClass('lastFormTab');return tabs};ploneFormTabbing.select=function($which){if(typeof $which=="string")
$which=jq($which.replace(/^#fieldset-/,"#fieldsetlegend-"));if($which[0].tagName.toLowerCase()=='a'){$which.click();return true} else if($which[0].tagName.toLowerCase()=='option'){$which.attr('selected',true);$which.parent().change();return true} else{$which.change();return true}
return false};ploneFormTabbing.initializeDL=function(){var tabs=jq(ploneFormTabbing._buildTabs(this,jq(this).children('dt')));jq(this).before(tabs);jq(this).children('dd').addClass('formPanel');tabs=tabs.find('li.formTab a,option.formTab');if(tabs.length)
ploneFormTabbing.select(tabs.filter(':first'))};ploneFormTabbing.initializeForm=function(){var fieldsets=jq(this).children('fieldset');if(!fieldsets.length) return;var tabs=ploneFormTabbing._buildTabs(this,fieldsets.children('legend'));jq(this).prepend(tabs);fieldsets.addClass("formPanel");jq(this).find('input[name=fieldset.current]').addClass('noUnloadProtection');var tab_inited=false;jq(this).find('.formPanel:has(div.field.error)').each(function(){var id=this.id.replace(/^fieldset-/,"#fieldsetlegend-");var tab=jq(id);tab.addClass("notify");if(tab.length&&!tab_inited)
tab_inited=ploneFormTabbing.select(tab)});jq(this).find('.formPanel:has(div.field span.fieldRequired)').each(function(){var id=this.id.replace(/^fieldset-/,"#fieldsetlegend-");jq(id).addClass('required')});if(!tab_inited){jq('input[name=fieldset.current][value^=#]').each(function(){tab_inited=ploneFormTabbing.select(jq(this).val())})}
if(!tab_inited){var tabs=jq("form.enableFormTabbing li.formTab a,"+"form.enableFormTabbing option.formTab,"+"div.enableFormTabbing li.formTab a,"+"div.enableFormTabbing option.formTab");if(tabs.length)
ploneFormTabbing.select(tabs.filter(':first'))}
jq("#archetypes-schemata-links").addClass('hiddenStructure');jq("div.formControls input[name=form.button.previous],"+"div.formControls input[name=form.button.next]").remove()};jq(function(){jq("form.enableFormTabbing,div.enableFormTabbing").each(ploneFormTabbing.initializeForm);jq("dl.enableFormTabbing").each(ploneFormTabbing.initializeDL);if(window.location.hash&&jq(".enableFormTabbing fieldset"+window.location.hash).length){ploneFormTabbing.select(window.location.hash)}});

/* - input-label.js - */
// http://osha.europa.eu/portal_javascripts/input-label.js?original=1
var ploneInputLabel={focus: function(){var t=jq(this);if(t.hasClass('inputLabelActive')&&t.val()==t.attr('title'))
t.val('').removeClass('inputLabelActive');if(t.hasClass('inputLabelPassword'))
ploneInputLabel._setInputType(t.removeClass('inputLabelPassword'),'password').focus().bind('blur.ploneInputLabel',ploneInputLabel.blur)},blur: function(){var t=jq(this);if(t.is(':password[value=""]')){t=ploneInputLabel._setInputType(this,'text').addClass('inputLabelPassword').bind('focus.ploneInputLabel',ploneInputLabel.focus);if(e.originalEvent&&e.originalEvent.explicitOriginalTarget)
jq(e.originalEvent.explicitOriginalTarget).trigger('focus!')}
if(!t.val())
t.addClass('inputLabelActive').val(t.attr('title'))},submit: function(){jq('input[title].inputLabelActive').trigger('focus.ploneInputLabel')},_setInputType: function(elem,ntype){var otype=new RegExp('type="?'+jq(elem).attr('type')+'"?')
var nelem=jq(jq('<div></div>').append(jq(elem).clone()).html().replace(otype,'').replace(/\/?>/,'type="'+ntype+'" />'));jq(elem).replaceWith(nelem);return nelem}};jq(function(){jq('form:has(input[title].inputLabel)').submit(ploneInputLabel.submit);jq('input[title].inputLabel').bind('focus.ploneInputLabel',ploneInputLabel.focus).bind('blur.ploneInputLabel',ploneInputLabel.blur).trigger('blur.ploneInputLabel')});

/* - highlightsearchterms.js - */
// http://osha.europa.eu/portal_javascripts/highlightsearchterms.js?original=1
function highlightTermInNode(node,word){var contents=node.nodeValue;if(jq(node).parent().hasClass("highlightedSearchTerm")) return;var highlight=function(content){return jq('<span class="highlightedSearchTerm">'+content+'</span>')}
while(contents&&(index=contents.toLowerCase().indexOf(word))>-1){jq(node).before(document.createTextNode(contents.substr(0,index))).before(highlight(contents.substr(index,word.length))).before(document.createTextNode(contents.substr(index+word.length)));var next=node.previousSibling;jq(node).remove();node=next;contents=node.nodeValue}}
function highlightSearchTerms(terms,startnode){if(!terms||!startnode) return;jq.each(terms, function(i,term){term=term.toLowerCase();if(!term||/(not|and|or)/.test(term)) return;jq(startnode).find('*').andSelf().contents().each(function(){if(this.nodeType==3) highlightTermInNode(this,term)})})}
function getSearchTermsFromURI(uri){var query;if(typeof decodeURI!='undefined'){query=decodeURI(uri)} else if(typeof unescape!='undefined'){query=unescape(uri)} else{}
var result=new Array();if(window.decodeReferrer){var referrerSearch=decodeReferrer();if(null!=referrerSearch&&referrerSearch.length>0){result=referrerSearch}}
var qfinder=new RegExp("(searchterm|SearchableText)=([^&]*)","gi");var qq=qfinder.exec(query);if(qq&&qq[2]){var terms=qq[2].replace(/\+/g,' ').split(' ');result.push.apply(result,jq.grep(terms, function(a){return a!=""}));return result}
return result.length==0?false:result}
jq(function(){var terms=getSearchTermsFromURI(window.location.search);highlightSearchTerms(terms,getContentArea())});

/* - se-highlight.js - */
// http://osha.europa.eu/portal_javascripts/se-highlight.js?original=1
var searchEngines=[['^http://([^.]+\\.)?google.*','q='],['^http://search\\.yahoo.*','p='],['^http://search\\.msn.*','q='],['^http://search\\.aol.*','userQuery='],['^http://(www\\.)?altavista.*','q='],['^http://(www\\.)?feedster.*','q='],['^http://search\\.lycos.*','query='],['^http://(www\\.)?alltheweb.*','q='],['^http://(www\\.)?ask\\.com.*','q=']]
function decodeReferrer(ref){if(null==ref&&document.referrer){ref=document.referrer}
if(!ref) return null;var match=new RegExp('');var seQuery='';for(var i=0;i<searchEngines.length;i++){if(!match.compile){match=new RegExp(searchEngines[i][0],'i')} else{match.compile(searchEngines[i][0],'i')}
if(ref.match(match)){if(!match.compile){match=new RegExp('^.*[?&]'+searchEngines[i][1]+'([^&]+)&?.*$','i')} else{match.compile('^.*[?&]'+searchEngines[i][1]+'([^&]+)&?.*$')}
seQuery=ref.replace(match,'$1');if(seQuery){seQuery=decodeURIComponent(seQuery);seQuery=seQuery.replace(/\'|"/, '');return seQuery.split(/[\s,\+\.]+/)}}}
return null}


/* - first_input_focus.js - */
// http://osha.europa.eu/portal_javascripts/first_input_focus.js?original=1
jq(function(){if(jq("form div.error :input:first").focus().length) return;jq("form.enableAutoFocus :input:not(.formTabs):visible:first").focus()});

/* - accessibility.js - */
// http://osha.europa.eu/portal_javascripts/accessibility.js?original=1
function setBaseFontSize(f,r){var b=jq('body');if(r){b.removeClass('smallText').removeClass('largeText');createCookie("fontsize",f,365)}b.addClass(f)};jq(function(){var f=readCookie("fontsize");if(f)setBaseFontSize(f,0)});

/* - styleswitcher.js - */
// http://osha.europa.eu/portal_javascripts/styleswitcher.js?original=1
function setActiveStyleSheet(title,reset){jq('link[rel*=style][title]').attr('disabled',true).find('[title='+title+']').attr('disabled',false);if(reset) createCookie("wstyle",title,365)};jq(function(){var style=readCookie("wstyle");if(style!=null) setActiveStyleSheet(style,0)});

/* - ++resource++jquery.bigtarget.1.0.1.js - */
// http://osha.europa.eu/portal_javascripts/++resource++jquery.bigtarget.1.0.1.js?original=1
(function($){$.fn.bigTarget=function(options){debug(this);var opts=$.extend({},$.fn.bigTarget.defaults,options);return this.each(function(){var $a=$(this);var href=$a.attr('href');var title=$a.attr('title');var o=$.meta?$.extend({},opts,$a.data()):opts;$a.parents(o.clickZone).hover(function(){$h=$(this);$h.addClass(o.hoverClass);if(typeof o.title!='undefined'&&o.title===true&&title!=''){$h.attr('title',title)}}, function(){$h.removeClass(o.hoverClass);if(typeof o.title!='undefined'&&o.title===true&&title!=''){$h.removeAttr('title')}}).click(function(){if(getSelectedText()==""){if($a.is('[rel*=external]')){window.open(href);return false}
else{window.location=href}}})})};
function debug($obj){if(window.console&&window.console.log)
window.console.log('bigTarget selection count: '+$obj.size())};
function getSelectedText(){if(window.getSelection){return window.getSelection().toString()}
else if(document.getSelection){return document.getSelection()}
else if(document.selection){return document.selection.createRange().text}};$.fn.bigTarget.defaults={hoverClass:'hover',clickZone:'li:eq(0)',title:true}})(jQuery);

/* - toc.js - */
// http://osha.europa.eu/portal_javascripts/toc.js?original=1
jq(function(){var dest=jq('dl.toc dd.portletItem');var content=getContentArea();if(!content||!dest.length) return;dest.empty();var location=window.location.href;if(window.location.hash)
location=location.substring(0,location.lastIndexOf(window.location.hash));var stack=[];jq(content).find('*').filter(function(){return/^h[1234]$/.test(this.tagName.toLowerCase())}).not('.documentFirstHeading').each(function(i){var level=this.nodeName.charAt(1)-1;while(stack.length<level){var ol=jq('<ol>');if(stack.length){var li=jq(stack[stack.length-1]).children('li:last');if(!li.length)
li=jq('<li>').appendTo(jq(stack[stack.length-1]));li.append(ol)}
stack.push(ol)}
while(stack.length>level) stack.pop();jq(this).before(jq('<a name="section-'+i+'" />'));jq('<li>').append(jq('<a />').attr('href',location+'#section-'+i).text(jq(this).text())).appendTo(jq(stack[stack.length-1]))});if(stack.length){jq('dl.toc').show();oltoc=jq(stack[0]);numdigits=oltoc.children().length.toString().length;oltoc.addClass("TOC"+numdigits+"Digit");dest.append(oltoc);var $target=jq(window.location.hash);$target=$target.length&&$target||jq('[name='+window.location.hash.slice(1)+']');var targetOffset=$target.offset().top;jq('html,body').animate({scrollTop:targetOffset},0)}});

