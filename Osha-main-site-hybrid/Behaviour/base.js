/*-------------------------------------------------------------------- 
 * JQuery Plugin: "EqualHeights"
 * by:	Scott Jehl, Todd Parker, Maggie Costello Wachs (http://www.filamentgroup.com)
 *
 * Copyright (c) 2008 Filament Group
 * Licensed under GPL (http://www.opensource.org/licenses/gpl-license.php)
 *
 * Description: Compares the heights or widths of the top-level children of a provided element 
 		and sets their min-height to the tallest height (or width to widest width). Sets in em units 
 		by default if pxToEm() method is available.
 * Dependencies: jQuery library, pxToEm method	(article: 
		http://www.filamentgroup.com/lab/retaining_scalable_interfaces_with_pixel_to_em_conversion/)							  
 * Usage Example: $(element).equalHeights();
  		Optional: to set min-height in px, pass a true argument: $(element).equalHeights(true);
 * Version: 2.0, 08.01.2008
--------------------------------------------------------------------*/

(function($){
$.fn.equalHeights = function(px) {
	$(this).each(function(){
		var currentTallest = 0;
		$(this).children().each(function(i){
			if ($(this).height() > currentTallest) { currentTallest = $(this).height(); }
		});
		// for ie6, set height since min-height isn't supported
		if ($.browser.msie && $.browser.version == 6.0) { $(this).children().css({'height': currentTallest}); }
		$(this).children().css({'min-height': currentTallest}); 
	});
	return this;
};

jQuery(document).ready(function() {
	$('#content').equalHeights();
});

jQuery(document).ready(function() {
    navcarousel = jQuery(".navcarousel").jcarousel();
});

jQuery(document).ready(function() {
	$('.partnerCloud').masonry({ columnWidth: 1 });
});


jQuery(document).ready(function() {
    var dX, dY;
    var trackm = function(ev) {
        dX = ev.pageX;
        dY = ev.pageY;
        if (dY < 150) {
            $('body').addClass('header-in');        
        } else {
            $('body').removeClass('header-in');                
        }
    };
    $('body').bind("mousemove",trackm);
    $('body').addClass('nav-closed').removeClass('nav-open');


});
/** Markup Pattern Library.
 *
 * Copyright 2009-2010 W. Akkerman
 */

/*jslint browser: true, undef: true, eqeqeq: true, regexp: true */

var mapal = {
    widthClasses: {},

    // Utility methods
    registerWidthClass: function(cls, minimum, maximum) {
        mapal.widthClasses[cls] = { minimum: minimum,
                                    maximum: maximum };
    },

    _renumberAttribute: function(el, attr, i) {
        var $el = $(el),
            buf = $el.attr(attr);
        if (buf) {
            $el.attr(attr, buf.replace(/[0-9]+/, i));
        }
    },

    renumber: function($container, selector) {
        var $entries = $container.find(selector ? selector : "fieldset,tr,dd"),
            entry, i;

        for (i=0; i<$entries.length; i++) {
            entry = $entries.get(i);
            mapal._renumberAttribute(entry, "id", i);
            $("label, :input", entry).each(function() {
                mapal._renumberAttribute(this, "for", i);
                mapal._renumberAttribute(this, "id", i);
                mapal._renumberAttribute(this, "name", i);
            });
        }
    },


    // Give the first input element with the autofocus class the focus
    initAutofocus: function(root) {
        var $elements = $(":input.autofocus", root),
            i;

        for (i=0; i < $elements.length; i+=1) {
            if (!$elements.eq(i).val()) {
                $elements.get(i).focus();
                break;
            }
        }
        if (i===$elements.length) {
            $elements.eq(0).focus();
        }
    },

    // Check if all dependencies as specified in `command` for
    // an element are satisfied.
    verifyDependencies: function($slave, command) {
        var result=[],
            $form = $slave.closest("body"),
            $input, i, value, parts; 

        for (i=0; i<command.on.length; i++) {
            parts=command.on[i];

            $input = $form.find(":input[name="+parts[0]+"]");
            if (!$input.length) {
                result.push(false);
                continue;
            }

            if ($input.attr("type")==="radio" || $input.attr("type")==="checkbox") {
                value = $input.filter(":checked").val();
            } else {
                value = $input.val();
            }

            if ((parts.length===1 || parts[1]==="on") && !value) {
                result.push(false);
                continue;
            } else if (parts[1]==="off" && value) {
                result.push(false);
                continue;
            } else if (parts.length>2) {
                if (parts[1]==="equals" && parts[2]!==value) {
                    result.push(false);
                    continue;
                } else if (parts[1]==="notEquals" && parts[2]===value) {
                    result.push(false);
                    continue;
                }
            } 
            result.push(true);
        }

        if (command.type==="or") {
            for (i=0; i<result.length; i++) {
                if (result[i]) {
                    return true;
                }
            }
            return false;
        } else {
            for (i=0; i<result.length; i++) {
                if (!result[i]) {
                    return false;
                }
            }
            return true;
        }
    },


    // Return the list of all input elements on which the given element has
    // a declared dependency via `dependsOn` classes.
    getDependMasters: function($slave, command) {
        var $result = $(),
            $form = $slave.closest("body"),
            i, parts;

        for (i=0; i<command.on.length; i++) {
            parts=command.on[i];
            if (!parts) {
                continue;
            }

            $result=$result.add($form.find(":input[name="+parts[0]+"]"));
        }

        return $result;
    },


    // Setup dependency-tracking behaviour.
    initDepends: function(root) {
        $("*[class*='dependsOn-']", root).each(function() {
            var slave = this,
                $slave = $(this),
                classes = $slave.attr("class").split(" "),
                command = {"on" : [],
                           "action" : "show",
                           "type": "and"
                           };
            var i, a, parts, state;

            for (i=0; i<classes.length; i++) {
                parts=classes[i].split("-");
                if (parts[0].indexOf("depends")===0) {
                    a=parts[0].substr(7).toLowerCase();
                    if (a==="on") {
                        if (parts.length>4) {
                            parts=parts.slice(0,3).concat(parts.slice(3).join("-"));
                        }
                        command.on.push(parts.slice(1));
                    } else {
                        command[a]=parts[1];
                    }
                }
            }

            state=mapal.verifyDependencies($slave, command);

            if (command.action==="show") {
                if (state) {
                    $slave.show();
                } else {
                    $slave.hide();
                }
            } else if (command.action==="enable") {
                if (state) {
                    slave.disabled=null;
                    $slave.removeClass("disabled");
                } else {
                    slave.disabled="disabled";
                    $slave.addClass("disabled");
                }
            }

            mapal.getDependMasters($slave, command).bind("change.depends", function() {
                state=mapal.verifyDependencies($slave, command);
                if (command.action==="show") {
                    if (state) {
                        $slave.slideDown();
                    } else {
                        $slave.slideUp();
                    }
                } else if (command.action==="enable" ) {
                    if (state) {
                        slave.disabled=null;
                        $slave.removeClass("disabled");
                    } else {
                        slave.disabled="disabled";
                        $slave.addClass("disabled");
                    }
                }
            });
        });
    },


    // Support for superimposing labels on input elements
    initSuperImpose: function(root) {
        $("label.superImpose", root).each(function() {
            var $label = $(this),
                forInput = $label.attr("for").replace(/([.\[\]])/g, "\\$1"),
                $myInput = forInput ? $(":input#"+forInput) : $(":input", this);

            if (!$myInput.length) {
                return;
            }

            $label
                .css("display", $myInput.val() ? "block" : "none")
                .click(function() {
                    $myInput.focus();
                });

            setTimeout(function() {
                $label.css("display", $myInput.val()==="" ? "block" : "none");
                }, 250);

            $myInput
                .bind("blur", function() {
                    $label.css("display", $myInput.val()==="" ? "block" : "none");
                })
                .bind("focus", function() {
                    $label.css("display", "none");
                });
        });
    },


    // Apply some standard markup transformations
    initTransforms: function(root) {
        $(".jsOnly", root).show();

        $("legend", root).each(function() {
            $(this).replaceWith('<p class="legend">'+$(this).html()+'</p>');
        });
    },


    // Manage open/close/hasChild classes for a ul-based menu tree
    initMenu: function(root) {
        $("ul.menu").each(function() {
            var $menu = $(this),
                timer,
                closeMenu, openMenu,
                mouseOverHandler, mouseOutHandler;


            root.globalIntent = null;
            root.globalIntentState = 0;
            root.currentLI = null;
            var sensitivity = 1;
            var interval = 50;
            
            var cX, cY, pX, pY;
            var track = function(ev) {
                cX = ev.pageX;
                cY = ev.pageY;
            };
            $("body").bind("mousemove",track);            
            
            // A private function for comparing current and previous mouse position
            compare = function(ev) {
                root.globalIntent = clearTimeout(root.globalIntent);
                // compare mouse positions to see if they've crossed the threshold
                if ( ( Math.abs(pX-cX) + Math.abs(pY-cY) ) < sensitivity  && (cY<150)) {
                    // set hoverIntent state to true (so mouseOut can be called)
                    root.globalIntentState = 1;
                    // if vorheriger aktiv, return false;
                    return openMenu(root.currentLI);
                } else {
                    // set previous coordinates for next time
                    pX = cX; pY = cY;
                    // use self-calling timeout, guarantees intervals are spaced out properly (avoids JavaScript timer bugs)
                    root.globalIntent = setTimeout( function(){compare(ev);} , interval );
                }
            };

            openMenu = function($li) {
                if (timer) {
                    
                    clearTimeout(timer);
                    timer = null;
                }

                if (!$li.hasClass("open")) {
                    $li.siblings("li.open").each(function() { closeMenu($menu);});
                    $li.addClass("open").removeClass("closed");

                    /* alex added */
                    h = $li.find('ul').innerHeight()+150;
                    $('div#content').animate({marginTop:h},{queue:false,duration:500});          
                    $('body').addClass('nav-open').removeClass('nav-closed');
                    root.globalIntentState = 0;
                    /* end alex added */
                }
            };

            closeMenu = function($li) {
                $li.find("li.open").andSelf().removeClass("open").addClass("closed");
                /* alex added */
                $('div#content').animate({marginTop:'150px'},{queue:false,duration:500});
                $('body').addClass('nav-closed').removeClass('nav-open');
                root.globalIntentState = 0;
                /* end alex added */
                
            };

            mouseOverHandler = function(e) {
                var ev = jQuery.extend({},e);
                var ob = this;
                var $li = $(this);
                pX = ev.pageX; pY = ev.pageY;
                root.currentLI = $li;
                root.globalIntent = setTimeout( function(){compare(ev);} , interval );
            };

            mouseOutHandler = function(e) {
                var $li = $(this);
                var p = (e.type == "mouseover" ? e.fromElement : e.toElement) || e.relatedTarget;
                while ( p && p != this ) { try { p = p.parentNode; } catch(e) { p = this; } }
                if ( p == this ) { return false; }
                if (timer) {
                    clearTimeout(timer);
                    timer=null;
                }
                timer = setTimeout(function() { closeMenu($li); }, 1000);
            };

            $("ul.menu li", root)
                .addClass("closed")
                .filter(":has(ul)").addClass("hasChildren")
                .bind("mouseover.mapal", mouseOverHandler)
                .bind("mouseout.mapal", mouseOutHandler);         
        });
    },

    // Utility method to facilitate AJAX content loading
    loadSnippet: function(url, selector, target, callback) {
        var $factory = $("<div/>"),
            $target = $("#"+target);

        if ($target.length===0) {
            $target = $("<div/>")
                .css("opacity", 0)
                .appendTo(document.body);
        }

        function htmlLoaded(data, textStatus, response) {
            if (response.status < 200 || response.status >= 400) {
                return;
            }

            $target.replaceWith(
                    $factory.find("#"+selector)
                        .attr("id", target)
                        .css("opacity", 0));
            $target = $("#"+target);

            mapal.initContent($target);
            callback($target);
        }

        $target.animate({opacity: 0}, "slow", function() { 
            url = url + " #" + selector;
            $factory.load(url, htmlLoaded);
        });
    },

    // Enable DOM-injection from anchors
    initDomInjection: function () {
        $("a[rel^=#]").live("click", function (e) {
            var $a = $(this),
                parts = $a.attr("href").split("#", 2),
                target = $a.attr("rel").slice(1);

            mapal.loadSnippet(parts[0], parts[1], target, function($target) {
                $target.animate({opacity: 1}, "fast");
            });

            e.preventDefault();
        });
    },

    // Event handler for forms in a panel
    panelFormHandler: function(data, status, xhr, $form) {
        // regexp taken from jQuery 1.4.1
        var rscript = /<script(.|\s)*?\/script>/gi,
            $trigger = $(this.context),
            href = this.context.tagName.toLowerCase()==="a" ? $trigger.attr("href") : $trigger.attr("name"),
            action = $form.attr("action"),
            $panel = $("#panel"),
            ct = xhr.getResponseHeader("content-type"),
            isJSON = ct.indexOf("application/json") >= 0,
            $tree, target;

        // Error or validation error
        if (isJSON || xhr.status !== 202) {
            if (isJSON) {
                var reply = $.parseJSON(xhr.responseText);
                $trigger.trigger("ajaxFormResult", reply);
                if (reply.action==="reload") {
                    location.reload();
                } else if (reply.action==="close" || !reply.action) {
                    $panel.overlay().close();
                    $panel.remove();
                }
                return;
            } else {
                $trigger.trigger("ajaxFormResult");
            }
            $panel.overlay().close();
            $panel.remove();
            return;
        }

        if (action.indexOf("#")>0) {
            target = action.split("#", 2)[1];
        } else {
            target = href.split("#", 2)[1];
        }

        $tree = $("<div/>").append(data.replace(rscript, ""));
        $tree = $tree.find("#"+target).attr("id", "panel-content");
        mapal.initContent(target);
        $("#panel-content").replaceWith($tree);
        $panel.find("form").ajaxForm({context: this.context,
                                      success: mapal.panelFormHandler});
    },

    // Load (part of a) page and open it in a modal panel
    initPanels: function() {
        $("a.openPanel[href*=#], button.openPanel[name*=#]").live("click", function (e) {
            var $trigger = $(this),
                href = this.tagName.toLowerCase()==="a" ? $trigger.attr("href") : $trigger.attr("name"),
                parts = href.split("#", 2),
                $panel = $("#panel");

            if ($panel.length===0) {
                $panel = $("<div/>")
                    .attr("id", "panel")
                    .appendTo(document.body);
                $("<div/>")
                    .attr("id", "panel-content")
                    .appendTo($panel);
            }

            mapal.loadSnippet(parts[0], parts[1], "panel-content", function($target) {
                var api;

                $target.css("opacity", 1).addClass("panel");
                $("#panel form").ajaxForm({context: $trigger.get(0),
                                           success: mapal.panelFormHandler});
                api = $panel.overlay({api: true,
                                      closeOnClick: false,
                                      expose: {color: "#333", loadSpeed: 200, opacity: 0.9}});
                api.load();
            });

            e.preventDefault();
        });
    },

    // Utility method to update the width classes on the body
    updateWidthClasses: function() {
        var width = $(window).width(),
            $body = $("body"),
            limits;

        for (var cls in mapal.widthClasses) {
            if (mapal.widthClasses.hasOwnProperty(cls)) {
                limits=mapal.widthClasses[cls];
                if ((limits.minimum===null || limits.minimum<=width) && (limits.maximum===null || width<=limits.maximum)) {
                    $body.addClass(cls);
                } else {
                    $body.removeClass(cls);
                }
            }
        }
    },


    initWidthClasses: function() {
        mapal.updateWidthClasses();
        $(window).bind("resize.mapal", mapal.updateWidthClasses);
    },


    // Setup a DOM tree.
    initContent: function(root) {
        mapal.initAutofocus(root);
        mapal.initDepends(root);
        mapal.initSuperImpose(root);
        mapal.initTransforms(root);
        mapal.initMenu(root);
        $(root).trigger("newContent", root);
    },

    // Setup global behaviour
    init: function() {
        mapal.initWidthClasses();
        mapal.initDomInjection();
        mapal.initPanels();
    }
};


$(document).ready(function() {
    mapal.registerWidthClass("narrow", 0, 780);
    mapal.registerWidthClass("medium", 0, 1060);
    mapal.registerWidthClass("wide", 1060, null);
    mapal.init();
    mapal.initContent(document.body);
    $(document).trigger("setupFinished", document);
});
})(jQuery);

