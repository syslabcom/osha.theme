/* 
vPIP version 1.13i Beta 
    * vPIP changed constructDiv to using the link parentNode innerHTML to construct it's hVlog DIV 
    
* Next:
*   * 
	 
Installation and usage page starts at:  http://vpip.org/videos-playing-in-place/

vPIP generates code from the hVlog format:
   <div class="hVlog">
      <a href="{url to videoblog file}" rel="enclosure" title="{title}" {type="video/{mime type}}" {class="hVlogTarget"} onclick=?vPIPPlay(this, {...})?> 
	  	<img src="{url to image file}" />
	</a>...
    <a href="{url to videoblog file}" rel="enclosure" title="{title}" {type="video/{mime type}}" onclick=?vPIPPlay(this, {...})?> 
	  	{Text description of movie type}
	</a>...
	<p>{Text on videoblog}</p>
   </div>
Note:  <a has the "onclick=..." to run vPIP:
      <a href="{url to videoblog file}" rel="enclosure" title="{title}" {type="video/{mime type}} 
	       onclick=onclick="vPIPShow({'width={width number including controller}, height={height number including controller},controller={true/false}, revert={true/false}...'})"> 

Acknowledgements
----------------
vPIP was originaly inspired in August, 2005 on seeing videos that popped into the location on 
Steve Garfields, http://stevegarfield.blogs.com/, vlog site.  The current version is partially 
based on input from Andreas Haugstrup, http://www.solitude.dk/ ,  and his script, video-link.js, 
and input from Josh Kinberg, http://fireant.tv/ .  Encouragement, testing and usage comes from 
the members of the videoblogging yahoo group, http://groups.yahoo.com/group/videoblogging/ .

March 2006

 * License (X11 License)
 * ===================================================================
 *  Copyright 2006-2007  Enric Teller  (email: enric@vpip.org)
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy 
 * of this software and associated documentation files (the "Software"), to 
 * deal in the Software without restriction, including without limitation the 
 * rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
 * sell copies of the Software, and to permit persons to whom the Software is 
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in 
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 * OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.

 * Except as contained in this notice, the name of the author or copyright 
 * holders shall not be used in advertising or otherwise to promote the sale, 
 * use or other dealings in this Software without prior written authorization 
 * from the author or copyright holders.
 * 
 * ===================================================================
 *
 *  
ThickBox
--------
	
 Thickbox - One box to rule them all.
 By Cody Lindley (http://www.codylindley.com)
 Under an Attribution, Share Alike License
 Thickbox is built on top of the very light weight jquery library.

*/

/*
 * Replace the link with an embed of the media file (video or audio) 
 * 
 * @param oLink
 * 			The link that called vPIPPlay
 * @param sParam
 * 			The embed parameters
 * @param sFlashVars
 * 			Variables passed to flash video player (either included -- cineViewer.swf -- or specified)
 * @param sThickBox
 * 			ThickBox parameters
 * @param sJump
 * 			Time location to jump in movie
 * 
 */
function vPIPPlay(_oLink, _sParams, _sFlashVars, _sThickBox, _sJump, _byDebug) {
	
	if (vpipPlayerRef == undefined || vpipPlayerRef == null) {
		var vpipPlayer = new vPIPPlayer(_oLink, _sParams, _sFlashVars, _sThickBox, _sJump, _byDebug);
		//Allow vpipPlayer to be accessed from external functions
		vpipPlayerRef = vpipPlayer;
	}
	else {
		// Get the existing vPIPPlayer that can hold multiple vPIP containers.
		var vpipPlayer = vpipPlayerRef;
		vpipPlayer.setStartup(_oLink, _sParams, _sFlashVars, _sThickBox, _sJump, _byDebug);
	}
	
	if (vpipPlayer.init()){
		vpipPlayer.show();
		
		return false;
	}
	else {
		if (vpipPlayer.oLink.href.toLowerCase().indexOf("http://") > -1)
			window.open(vpipPlayer.oLink.href, "_self");
		
		return true;	
	}
}

/* aDIV's array holds the DIVs that have been activated.
 * structure:
	[0]... divs
		[0] oDiv
		[1] DIVid
		[2] OrigHTML
		[3]... links
			[0] Open/Close
			[1] HREF
			[2] Width
			[3] Height
			[4] Autostart
			[5] Controller
			[6] Name
			[7] KioskMode
			[8] Target
			[9] Loop
			[10] Quality
			[11] BGColor
			[12] FlashMedia
			[13] Scale
			[14] AddControlHeight
		 	[15] Revert
		 	[16] ShowCloseBtn
		 	[17] LinkID
*/
//Constants for aDIV Array positions for accessing array elements
vPIPPlayer.DIVPOS = 0; 
vPIPPlayer.DIVIDPOS = 1;
vPIPPlayer.ORIGHTMLPOS = 2;
vPIPPlayer.LINKSARRAYPOS = 3;

//Link Array position constants
vPIPPlayer.OPENPOS = 0;
vPIPPlayer.HREFPOS = 1;
vPIPPlayer.WIDTHPOS = 2;
vPIPPlayer.HEIGHTPOS = 3;
vPIPPlayer.FLASHWIDTH = 320; 		     //Internal Flash Player width
vPIPPlayer.FLASHHEIGHT  = 240; 		     //Internal Flash Player height
vPIPPlayer.FLASHCONTROLBARHEIGHT  = 20;  //Height of the internal Flash Player control bar
vPIPPlayer.QTCONTROLBARHEIGHT  = 16;     //Height of the quicktime control bar
vPIPPlayer.WMCONTROLBARHEIGHT  = 16;     //Height of the windows media control bar
vPIPPlayer.AUTOSTARTPOS = 4;
vPIPPlayer.CONTROLLERPOS = 5;
vPIPPlayer.NAMEPOS = 6;
vPIPPlayer.KIOSKMODEPOS = 7;
vPIPPlayer.TARGETPOS = 8;
vPIPPlayer.LOOPPOS = 9;
vPIPPlayer.QUALITYPOS = 10;
vPIPPlayer.BGCOLORPOS = 11;
vPIPPlayer.FLASHMEDIAPOS = 12;
vPIPPlayer.SCALEPOS = 13;
vPIPPlayer.ADDCONTROLHEIGHTPOS = 14;
vPIPPlayer.REVERTPOS = 15;
vPIPPlayer.SHOWCLOSEBTNPOS = 16;
vPIPPlayer.LINKIDPOS = 17;

//Movie embed default constants
vPIPPlayer.WIDTH = 320; 			//Movie width
vPIPPlayer.HEIGHT  = 240; 			//Movie height with controller (if enabled)
vPIPPlayer.AUTOSTART = "true"; 		//Whether the movie automaticaly plays on initiation
vPIPPlayer.CONTROLLER = "true";		//Whether the movie controller is active
vPIPPlayer.NAME = "" 				//Name and ID of movie
vPIPPlayer.KIOSKMODE = "false" 		//Quicktime kioskmode parameter
vPIPPlayer.TARGET = "embed" 		//Quicktime target parameter
vPIPPlayer.LOOP = "false" 			//Quicktime loop parameter
vPIPPlayer.QUALITY = "high" 		//Flash quality parameter
vPIPPlayer.BGCOLOR = "#FFFFFF";		//Flash background color parameter
vPIPPlayer.FLASHMEDIA = "false"		//Whether the movie is a Flash Media.  If true, the internal Flash video player is used.
vPIPPlayer.SCALE = "noScale"		//The scaling method for the embedded flash video player
vPIPPlayer.ADDCONTROLHEIGHT = "true"; //Whether to add the height of the control to the embed
vPIPPlayer.REVERT = "true"; 		//Whether to revert to original elements in DIV container when another movie is selected
vPIPPlayer.SHOWCLOSEBTN = "true";	// Whether the Close button appears above the movie

//Internal Flash video Player
vPIPPlayer.FLASHMEDIAPLAYER = "cineViewer-002a.swf";

//The Safari build where releasing an embedded movie works.
vPIPPlayer.WORKINGSAFARIBUILD = 420;

//Whether the vPIPPlayer has been opened to embed
vPIPPlayer.prototype.isOpen = false;

vPIPPlayer.glDivs;                 // Global divs array

//Global reference to vPIPPlayer object
var vpipPlayerRef;

//The item (text, image, etc.) that displays to activate closing the ThickBox instance.
var vPIPThickBoxCloseItem = "close";

function vPIPPlayer(_oLink, _sParams, _sFlashVars, _sThickBox, _sJump, _byDebug) {

	this.setStartup(_oLink, _sParams, _sFlashVars, _sThickBox, _sJump, _byDebug);
	
	this.aDIVs = new Array();
	//Current link array position
	this.iInitiator = 0;

	aParams = _sParams.split(",");
	iIDPos = aParams.findFirst(/id=/i);
	if (iIDPos != null) 
	{
		sID = aParams[iIDPos];
		var iPos = sID.indexOf("=");
		if (iPos > -1)
		{
			sID = sID.substr(iPos+1);
		}		}
	else
		sID = null;
	// Get path to vPIP.js
	this.vPIPpath = vPIP_getPath(sID);
			
}

vPIPPlayer.prototype.setStartup = function(_oLink, _sParams, _sFlashVars, _sThickBox, _sJump, _byDebug) {
	// Record parameters in vPIPPlayer properties
	this.oLink = _oLink;
	this.sParams = _sParams;
	this.sFlashVars = _sFlashVars;
	this.sThickBox = _sThickBox;
	this.sJump = _sJump;
	//Wether in Debug mode
	if (_byDebug != undefined)
		this.byDebug = _byDebug
	else if (this.byDebug == undefined)
		this.byDebug = false
	
	if (this.byDebug)
	{
		if (this.sFlashVars.length == 0)
			this.sFlashVars += "byDebug=true";
		else
			this.sFlashVars += "&byDebug=false";
		
	}
}

vPIPPlayer.prototype.init = function() {
		
	//Get the DIV container of the link to 
	this.oDiv = vPIP_getContainer("hVlog", this.oLink);
	
	/*= this.oLink.parentNode;
	while (this.oDiv != undefined && this.oDiv != null && 
			this.oDiv.nodeName.toLowerCase() != "div" &&
			(vPIPPlayer.findAttribute(this.oDiv, "class") == null || 
			vPIPPlayer.findAttribute(this.oDiv, "class").toLowerCase() != "hvlog")) {
		this.oDiv = this.oDiv.parentNode;
	}*/
	
	//If anchor link is missing container div, create it.
	if (this.oDiv == undefined || this.oDiv == null || 
		this.oDiv.nodeName.toLowerCase() != "div" || 
		vPIPPlayer.findAttribute(this.oDiv, "class") == null ||
		vPIPPlayer.findAttribute(this.oDiv, "class").toLowerCase() != "hvlog") {
		
		this.oDiv = this.constructDiv(this.oLink);
		
		if (this.oDiv != undefined && this.oDiv != null && 
			this.oDiv.nodeName.toLowerCase() == "div" && 
			vPIPPlayer.findAttribute(this.oDiv, "class") != null &&
			vPIPPlayer.findAttribute(this.oDiv, "class").toLowerCase() == "hvlog") {
			
			this.oLink.parentNode.replaceChild(this.oDiv, this.oLink);
			this.oLink = this.oDiv.firstChild;
		}
	}
	
	if (this.oDiv == undefined || this.oDiv == null || 
		this.oDiv.nodeName.toLowerCase() != "div" || 
		vPIPPlayer.findAttribute(this.oDiv, "class") == null ||
		vPIPPlayer.findAttribute(this.oDiv, "class").toLowerCase() != "hvlog")
		
		this.byDivExists = false;
	else
		this.byDivExists = true;
	
	if (this.byDivExists) {
		var byDivFound = false;
		
		//If viewing notication object exists, create local object
		//  (**to be implemented**)
		//if (typeof _vPIP_NotifyViewing == "function") {
		//	vpip_NotifyViewing = new _vPIP_NotifyViewing();
		//}
		
		// Locate the current DIV in the aDIVs array of DIVs
		this.iNextPos = this.findDIV(this.oDiv);
		// If DIV not found set to create a new entry in the aDIVs array of DIVs
		if (this.iNextPos == -1) 
			this.iNextPos = this.aDIVs.length;
		else
			byDivFound = true;
		
		// The ID value of the LINK	
		this.sLinkid = "";
		
		this.sHREF = vPIPPlayer.toAlphaNum(this.oLink.href, "~");
		if (! byDivFound) {	
			this.oDiv.setAttribute("id", "vPIP" + this.iNextPos);
			this.sOnClick = vPIPPlayer.toAlphaNum(this.oLink.onclick.toString());
			this.sLinkid = "vPIPMovie" + this.iInitiator;
			this.oLink.setAttribute("id", this.sLinkid);
			
			this.aDIVs[this.iNextPos] = new Array(3);
			this.aDIVs[this.iNextPos][vPIPPlayer.DIVPOS] = this.oDiv;
			this.aDIVs[this.iNextPos][vPIPPlayer.DIVIDPOS] = "vPIP" + this.iNextPos;
			
			this.aDIVs[this.iNextPos][3] = new Array(vPIPPlayer.LINKIDPOS+1);
			this.aDIVs[this.iNextPos][3][vPIPPlayer.OPENPOS] = false;
			this.aDIVs[this.iNextPos][3][vPIPPlayer.HREFPOS] = this.sHREF;
			this.aDIVs[this.iNextPos][3][vPIPPlayer.LINKIDPOS] = parseInt(this.sLinkid.substring(9));;
			
			this.iInitiator++;
		}
		else {
		
			this.byLinkFound = false;
			this.iNextLinkPos = -1;
			
			this.sLinkid = this.oLink.id;
			
			if (this.sLinkid != undefined && this.sLinkid != null && this.sLinkid.length > 9) {
				this.iLinkid = parseInt(this.sLinkid.substring(9));
				this.iNextLinkPos = this.findLinkInDiv(this.aDIVs[this.iNextPos], this.iLinkid);
				if (this.iNextLinkPos < 3) 
					this.iNextLinkPos = 3;
				else 
					this.byLinkFound = true;
			}
			else {
				this.iNextLinkPos = this.aDIVs[this.iNextPos].length;
				if (this.iNextLinkPos < 3) 
					this.iNextLinkPos = 3;
				this.sLinkid = "vPIPMovie" + this.iInitiator;
             	this.oLink.setAttribute("id", this.sLinkid);
             	
   				this.iInitiator++;
			}
			
			if (! this.byLinkFound) {
				this.aDIVs[this.iNextPos][this.iNextLinkPos] = new Array(vPIPPlayer.LINKIDPOS+1);
				this.aDIVs[this.iNextPos][this.iNextLinkPos][vPIPPlayer.OPENPOS] = false;
				this.aDIVs[this.iNextPos][this.iNextLinkPos][vPIPPlayer.HREFPOS] = this.sHREF;
				this.aDIVs[this.iNextPos][this.iNextLinkPos][vPIPPlayer.LINKIDPOS] = parseInt(this.sLinkid.substring(9));;
			}
			
		}
		
	}
	
	return true;
	
}

vPIPPlayer.prototype.show = function() {
	
	//Initialize the embed parameters
	this.iWidth = vPIPPlayer.WIDTH;					//Movie width
	this.iHeight  = vPIPPlayer.HEIGHT; 				//Movie height with controller (if enabled)
	this.byAutostart = vPIPPlayer.AUTOSTART; 		//Whether the movie automaticaly plays on initiation
	this.byController = vPIPPlayer.CONTROLLER; 		//Whether the movie controller is active
	this.sName = vPIPPlayer.NAME; 					//Name and ID of movie
	this.sKioskMode = vPIPPlayer.KIOSKMODE; 		//Quicktime kioskmode parameter
	this.sTarget = vPIPPlayer.TARGET; 				//Quicktime target parameter
	this.sLoop = vPIPPlayer.Loop; 					//Quicktime loop parameter
	this.sQuality = vPIPPlayer.QUALITY; 			//Flash quality parameter
	this.sBGColor = vPIPPlayer.BGCOLOR; 			//Flash background color parameter
	this.byFlashMedia = vPIPPlayer.FLASHMEDIA;		//Whether the movie is a Flash Media.  If true, the internal Flash video player is used.
	this.sScale = vPIPPlayer.SCALE;					//Scaling method for the embedded flash player
	this.byAddControlHeight = vPIPPlayer.ADDCONTROLHEIGHT; //Whether to add the height of the control to the embed
	this.byRevert = vPIPPlayer.REVERT; 				//Whether to revert to original elements in DIV container when another movie is selected
    
    // Whether the Close button appears above the movie
    this.byShowCloseBtn = vPIPPlayer.SHOWCLOSEBTN;	
    
    // General purpose variable for holding an array or string position.
	var iPos;   
	
	if (this.byDivExists) {
		if (this.oLink != undefined && this.oLink != null && this.oLink.nodeName.toLowerCase() == "a") {
		
			this.iCurrDIVid = parseInt(this.oDiv.id.substring(4));
			this.iCurrLinkid = parseInt(this.oLink.id.substring(9));
			this.iCurrLink = this.findLinkID(this.aDIVs[this.iCurrDIVid], this.iCurrLinkid);
	
			this.sHREF = this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.HREFPOS];
			
			if (this.sHREF == undefined || this.sHREF == null)
				this.sHREF = this.oLink.href;
			
			if (this.sHREF != undefined && this.sHREF != null) {
	
				var movieType = vPIPPlayer.isMovieFile(this.oLink);
				this.sMimeType = movieType.sMimeType;
				this.sType = movieType.sType;
				this.sMediaFormat = movieType.sMediaFormat;
				this.sFileExt = movieType.sFileExt;
				
				//Set default Flash parameters
				if (this.sMediaFormat == "flash") {
					this.iWidth = vPIPPlayer.FLASHWIDTH;
					if (this.byAddControlHeight == "true")
					{
						this.iHeight = vPIPPlayer.FLASHHEIGHT + vPIPPlayer.FLASHCONTROLBARHEIGHT;
					}
					else 
					{
						this.iHeight = vPIPPlayer.FLASHHEIGHT;
					}
					if (this.sFileExt == ".flv")
						this.byFlashMedia = "true";
				}
				
				// Get movie parameters
				var byInitArray = true;
				//If movie operation settings already loaded
				if (this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.WIDTHPOS] != undefined) {
				  this.iWidth = this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.WIDTHPOS];
				  this.iHeight = this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.HEIGHTPOS];
				  this.byAutostart = this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.AUTOSTARTPOS];
				  this.byController = this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.CONTROLLERPOS];
				  this.sName = this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.NAMEPOS];
				  this.sKioskMode = this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.KIOSKMODEPOS];
				  this.sTarget = this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.TARGETPOS];
				  this.sLoop = this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.LOOPPOS];
				  this.sQuality = this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.QUALITYPOS];
				  this.sBGColor = this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.BGCOLORPOS];
				  this.byFlashMedia = this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.FLASHMEDIAPOS];
				  this.sScale = this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.SCALEPOS];
				  this.byAddControlHeight = this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.ADDCONTROLHEIGHTPOS];
				  this.byRevert = this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.REVERTPOS];
				  this.byShowCloseBtn = this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.SHOWCLOSEBTNPOS];
				  byInitArray = false;
				}
				// Load user movie operation settings
				else {
					if (this.sParams != undefined && this.sParams != null) {
						var aParams = this.sParams.split(",");
						var aMatch;
						for (var i=0; i < aParams.length; i++) {
							if (aMatch = aParams[i].match(/(\bwidth\b\s*=\s*)(\d*)/i)) {
							  this.iWidth = aMatch[2];
							}
							else if (aMatch = aParams[i].match(/(\bheight\b\s*=\s*)(\d*)/i)) {
							  this.iHeight = aMatch[2];
							}
							else if (aMatch = aParams[i].match(/(\bautostart\b\s*=\s*)(\w*)/i)) {
							  this.byAutostart = (aMatch[2].toLowerCase() === "true");
							}
							else if (aMatch = aParams[i].match(/(\bcontroller\b\s*=\s*)(\w*)/i)) {
							  this.byController = (aMatch[2].toLowerCase() === "true");
							}
							else if (aMatch = aParams[i].match(/(\bname\b\s*=\s*)(\w*)/i)) {
								this.sName = aMatch[2];
							}
							else if (aMatch = aParams[i].match(/(\bkioskmode\b\s*=\s*)(\w*)/i)) {
							  this.sKioskMode = aMatch[2];
							}
							else if (aMatch = aParams[i].match(/(\btarget\b\s*=\s*)(\w*)/i)) {
							  this.sTarget = aMatch[2];
							}
							else if (aMatch = aParams[i].match(/(\bloop\b\s*=\s*)(\w*)/i)) {
							  this.sLoop = aMatch[2];
							}
							else if (aMatch = aParams[i].match(/(\bquality\b\s*=\s*)(\w*)/i)) {
							  this.sQuality = aMatch[2];
							}
							else if (aMatch = aParams[i].match(/(\bbgcolor\b\s*=\s*)(\w*)/i)) {
							  this.sBGColor = aMatch[2];
							}
							else if (aMatch = aParams[i].match(/(\bflv\b\s*=\s*)(\w*)/i)) {
							  this.byFlashMedia = aMatch[2];
							}
							else if (aMatch = aParams[i].match(/(\bscale\b\s*=\s*)(\w*)/i)) {
							  this.sScale = aMatch[2];
							}
							else if (aMatch = aParams[i].match(/(\baddcontrolheight\b\s*=\s*)(\w*)/i)) {
							  this.byAddControlHeight = aMatch[2];
							}
							else if (aMatch = aParams[i].match(/(\brevert\b\s*=\s*)(\w*)/i)) {
							  this.byRevert = (aMatch[2].toLowerCase() === "true");
							}
							else if (aMatch = aParams[i].match(/(\bshowclose\b\s*=\s*)(\w*)/i)) {
							  this.byShowCloseBtn = (aMatch[2].toLowerCase() === "true");
							}
						}
						//Add control bar height to display height
						if (this.sType == "video" || this.sType == "application") 
						{
							if (this.byAddControlHeight == "true")
							{
								if (this.sMediaFormat == "quicktime") 
								{
									this.iHeight = (Number(this.iHeight) + vPIPPlayer.QTCONTROLBARHEIGHT).toString();
								}
								else if (this.sMediaFormat == "windowsmedia") 
								{
									this.iHeight = (Number(this.iHeight) + vPIPPlayer.WMCONTROLBARHEIGHT).toString();
								}
								else if (this.sMediaFormat == "flash") 
								{
									this.iHeight = (Number(this.iHeight) + vPIPPlayer.FLASHCONTROLBARHEIGHT).toString();
								}
							}
						}
					}
				}
	
				//If this DIV is already open from a link, close it
				this.closeThisDiv(this.aDIVs, this.iCurrDIVid);
				
				var sInnerHTML = this.oDiv.innerHTML;
				//Add the 2nd dimension
				this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.OPENPOS] = false;  // default to embed not opened.
				//If no id Name specified for embed, assign the link's number
				if (this.sName == undefined || this.sName == null || this.sName == "") {
					this.sName = "Embed" + this.iCurrLinkid;
				}
				
				// If array already initialized, don't init.
				if (byInitArray) {
					this.aDIVs[this.iCurrDIVid][vPIPPlayer.ORIGHTMLPOS] = sInnerHTML;
					
					this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.WIDTHPOS] = 			this.iWidth;
					this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.HEIGHTPOS] = 		this.iHeight;
					this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.AUTOSTARTPOS] = 		this.byAutostart;
					this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.CONTROLLERPOS] = 	this.byController;
					this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.NAMEPOS] = 			this.sName;
					this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.KIOSKMODEPOS] = 		this.sKioskMode;
					this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.TARGETPOS] = 		this.sTarget;
					this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.LOOPPOS] = 			this.sLoop;
					this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.QUALITYPOS] = 		this.sQuality;
					this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.BGCOLORPOS] = 		this.sBGColor;
					this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.FLASHMEDIAPOS] = 	this.byFlashMedia;
					this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.SCALEPOS] = 			this.sScale;
					this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.ADDCONTROLHEIGHTPOS] = this.byAddControlHeight;
					this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.REVERTPOS] = 		this.byRevert;
					this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.SHOWCLOSEBTNPOS] = 	this.byShowCloseBtn;
				}
				
				// Replacement text 
				this.sReplace = "";
				if (this.sType == "video" || this.sType == "application") {
					if (this.sMediaFormat == "quicktime") {
						this.sReplace = "<object class='vPIPEmbed' width='" + this.iWidth + "' height='" + this.iHeight  + "' id='" + this.sName + "' classid='clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B' ";
						if (this.sMimeType == "smil")
						{
							if (this.sTarget.toLowerCase() == "quicktimeplayer")
							{
								this.sReplace += "codebase='http://www.apple.com/qtactivex/qtplugin.cab'> <param name='src' value='" + this.vPIPpath + "InitSMIL.mov'><param name='qtsrc' value='" +  this.sHREF;
								this.sReplace += "'><param name='href' value='" + this.sHREF + "' /><param name='autohref' value='true";
							}
							else
								this.sReplace += "codebase='http://www.apple.com/qtactivex/qtplugin.cab'> <param name='src' value='" + this.vPIPpath + "InitSMIL.mov'><param name='qtsrc' value='" +  this.sHREF;
						}
						else
						{
							if (this.sTarget.toLowerCase() == "quicktimeplayer")
							{
								this.sReplace += "codebase='http://www.apple.com/qtactivex/qtplugin.cab'> <param name='src' value='" + this.vPIPpath + "InitSMIL.mov' >";
								this.sReplace += "<param name='href' value='" + this.sHREF + "' /><param name='autohref' value='true";
							}
							else
								this.sReplace += "codebase='http://www.apple.com/qtactivex/qtplugin.cab'> <param name='src' value='" + this.sHREF;
						}
						this.sReplace += "'><param name='autoplay' value='" + this.byAutostart + "'><param name='scale' value='tofit' />";
						if (this.sTarget.toLowerCase() == "quicktimeplayer")
							this.sReplace += "<param name='target' value='quicktimeplayer'><param name='loop' value='" + this.sLoop + "'>";
						else
							this.sReplace += "<param name='loop' value='" + this.sLoop + "'>";
						this.sReplace += "<param name='kioskmode' value='" + this.sKioskMode + "'><param name='controller' value='";
						if (this.sMimeType == "smil")
							if (this.sTarget.toLowerCase() == "quicktimeplayer")
							{
								this.sReplace += this.byController + "'><embed src='" + this.vPIPpath + "InitSMIL.mov' width='"+ this.iWidth + "' height='" + this.iHeight;
								this.sReplace += "' href='" + this.sHREF + "' autohref='true";
							}
							else
								this.sReplace += this.byController + "'><embed src='" + this.vPIPpath + "InitSMIL.mov' qtsrc='" + this.sHREF + "' width='"+ this.iWidth + "' height='" + this.iHeight;
						else
						{
							if (this.sTarget.toLowerCase() == "quicktimeplayer")
							{
								this.sReplace += this.byController + "'><embed src='" + this.vPIPpath + "InitSMIL.mov' width='"+ this.iWidth + "' height='" + this.iHeight;
								this.sReplace += "' href='" + this.sHREF + "' autohref='true";
							}
							else
								this.sReplace += this.byController + "'><embed src='" + this.sHREF + "' width='"+ this.iWidth + "' height='" + this.iHeight;
						}
						this.sReplace += "' name='" + this.sName + "' autoplay='" + this.byAutostart + "' controller='" + this.byController; 
						if (this.sTarget.toLowerCase() == "quicktimeplayer")
							this.sReplace += "' target='quicktimeplayer'  loop='" + this.sLoop;
						else
							this.sReplace += "' loop='" + this.sLoop;
						this.sReplace += "' kioskmode='" + this.sKioskMode + "' scale='tofit' pluginspage='http://www.apple.com/quicktime/download/'></embed></object>";
					}
					else if (this.sMediaFormat == "windowsmedia") {
							
						this.sReplace = "<OBJECT class='vPIPEmbed' CLASSID='CLSID:22d6f312-b0f6-11d0-94ab-0080c74c7e95'  ";
						this.sReplace += "codebase='http://activex.microsoft.com/activex/controls/mplayer/en/nsmp2inf.cab#Version=5,1,52,701' ";
						this.sReplace += "standby='Loading Microsoft Windows Media Player components...' type='application/x-oleobject'  ";
						this.sReplace += "width='" + this.iWidth + "' height='" + this.iHeight + "' id='" + this.sName + "' >";
						this.sReplace += "<PARAM NAME='fileName' VALUE='" + this.sHREF + "' ><PARAM NAME='autoStart' VALUE='" + this.byAutostart;
						this.sReplace += "'><PARAM NAME='showControls' VALUE='" + this.byController + "'>";
						this.sReplace += "<EMBED type='application/x-mplayer2' pluginspage='http://www.microsoft.com/Windows/MediaPlayer/' id='";
						this.sReplace += this.sName + "' name='" + this.sName + "' showcontrols='" + this.byController + "' width='" + this.iWidth + "' height='"; 
						this.sReplace += this.iHeight + "' src='" + this.sHREF + "' autostart='" + this.byAutostart + "'></EMBED></OBJECT>";
					}
					else if (this.sMediaFormat == "flash") {
						this.sReplace = "<OBJECT class=\"vPIPEmbed\" classid=\"clsid:D27CDB6E-AE6D-11cf-96B8-444553540000\" ";
						this.sReplace += "codebase=\"http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,40,0\" ";
						this.sReplace += "WIDTH=\"" + this.iWidth + "\" HEIGHT=\"" + this.iHeight + "\" id=\"" + this.sName + "\" >";
						this.sReplace += "<PARAM NAME=\"movie\" VALUE=\"";
						//Use a Flash video viewer to play the designated Flash Media
						if (this.byFlashMedia == "true") {
							 //  Set Flash type and location
						    this.sFlashMediaPlayer = this.vPIPpath + vPIPPlayer.FLASHMEDIAPLAYER;

							//Construct sJump for flashvars send
							var sJumpFlashVars= "";
							if (this.sJump != null && this.sJump.length > 0) {
								var aParams = this.sJump.split(",");
								var aMatch;
								for (var i=0; i < aParams.length; i++) {
									if (aMatch = aParams[i].match(/(\w*)(\s*=\s*)(.*)/)) 
										sJumpFlashVars += "&" + aMatch[1] + "=" + aMatch[3];
								}
							}
							
							this.sReplace += this.sFlashMediaPlayer + "\"> <PARAM NAME=\"quality\" VALUE=\"" + this.sQuality + "\" > <PARAM NAME=\"bgcolor\" VALUE=\"" + this.sBGColor + "\"> ";
							this.sReplace += "<param name=\"scale\" value=\"" + this.sScale + "\" ><param name=\"salign\" value=\"TL\" ><param name=\"allowfullscreen\" value=\"true\" >";
							this.sReplace += "<PARAM NAME=\"FlashVars\" VALUE=\"file=" + this.sHREF + "&cvhome=" + this.vPIPpath + "&width=" + this.iWidth + "&height=" + this.iHeight;
							this.sReplace += "&autostart=" + this.byAutostart;
							if (this.sFlashVars != undefined && this.sFlashVars != null && this.sFlashVars.length > 0)
								this.sReplace += "&" + this.sFlashVars;
							this.sReplace += sJumpFlashVars + "\" > <EMBED src=\"" + this.sFlashMediaPlayer + "\" quality=\"" + this.sQuality + "\" bgcolor=\"" + this.sBGColor + "\" width=\"" + this.iWidth + "\" height=\"" + this.iHeight + "\" ";
							this.sReplace += "  scale=\"" + this.sScale + "\" salign=\"TL\" allowfullscreen=\"true\" FlashVars=\"file=" + this.sHREF + "&cvhome=" + this.vPIPpath + "&width=" + this.iWidth + "&height=" + this.iHeight + "&autostart=" + this.byAutostart;
							if (this.sFlashVars != undefined && this.sFlashVars != null && this.sFlashVars.length > 0) {
								this.sReplace += "&" + this.sFlashVars;
							}
							this.sReplace += sJumpFlashVars + "\" NAME=\"" + this.sName + "\" ALIGN=\"\" TYPE=\"application/x-shockwave-flash\" PLUGINSPAGE=\"http://www.macromedia.com/go/getflashplayer\"> ";
						}
						else {
							this.sReplace += this.sHREF + "\"> <PARAM NAME=\"quality\" VALUE=\"" + this.sQuality + "\" > <PARAM NAME=\"bgcolor\" VALUE=\"" + this.sBGColor + "\"> ";
							if (this.sFlashVars != undefined && this.sFlashVars != null && this.sFlashVars.length > 0)
								this.sReplace += "<param name=\"scale\" value=\"" + this.sScale + "\" ><param name=\"salign\" value=\"TL\" ><param name=\"allowfullscreen\" value=\"true\" >";
								this.sReplace += "<PARAM NAME=\"FlashVars\" VALUE=\"" + this.sFlashVars + "\" > "; //Why?: + "&embdWidth=" + this.iWidth + "&embdHeight=" + this.iHeight + "\" > ";
							this.sReplace += "<EMBED src=\"" + this.sHREF + "\" quality=\"" + this.sQuality + "\" bgcolor=\"" + this.sBGColor + "\" width=\"" + this.iWidth + "\" height=\"" + this.iHeight + "\"";
							if (this.sFlashVars != undefined && this.sFlashVars != null && this.sFlashVars.length > 0)
								this.sReplace += "  scale=\"" + this.sScale + "\" salign=\"TL\" allowfullscreen=\"true\" FlashVars=\"" + this.sFlashVars + "\" "; //Why?: + "&embdWidth=" + this.iWidth + "&embdHeight=" + this.iHeight + "\" ";
							this.sReplace += "NAME=\"" + this.sName + "\" ALIGN=\"\" TYPE=\"application/x-shockwave-flash\" PLUGINSPAGE=\"http://www.macromedia.com/go/getflashplayer\"> ";
						}
						this.sReplace += "</EMBED> </OBJECT>";
					}
			         else if (this.sMediaFormat == "ogg") {
			
			          this.sReplace += "<applet code='com.fluendo.player.Cortado.class'  \n";
			          this.sReplace += "   archive='" + this.vPIPpath + "cortado.jar' \n";
			          this.sReplace += "   width='" + this.iWidth + "' height='" + this.iHeight + "'>\n";
			          this.sReplace += " <PARAM NAME='url' VALUE='" + this.sHREF + "' />\n";
			          this.sReplace += " <param name='local' value='false' />\n";
			          this.sReplace += " <PARAM NAME='keepAspect' VALUE='true' />\n";
			          this.sReplace += " <PARAM NAME='video' VALUE='true' />\n";
			          this.sReplace += " <PARAM NAME='audio' VALUE='true' />\n";
			          this.sReplace += " <PARAM NAME='bufferSize' VALUE='200' />\n";
			          this.sReplace += "</applet>\n";
					}
					
					if (this.sReplace.length > 0) {
						if (this.byDebug)
							alert( this.sReplace);
	
						var sUserAgent = navigator.userAgent;
						this.bySafari = sUserAgent.indexOf('Safari') > -1;
						this.byOpera = sUserAgent.indexOf('Opera') > -1;
						this.byIE7 = sUserAgent.indexOf("MSIE 7") > -1;
						this.byIE6 = sUserAgent.indexOf("MSIE 6") > -1;
						this.nSafariBuild = -1;
						if (this.bySafari) {
							this.nSafariBuild = Number(sUserAgent.substring(sUserAgent.indexOf('Safari')+7));
						}
						//Get any Thickbox parameters
						this.byThickBox = false;
						//Setup ThickBox parameters
						if (this.sThickBox != undefined && this.sThickBox != null && this.sThickBox.length > 0) { // See if it works on Safari & IE6 && ! this.bySafari && ! this.byIE6) {
							var aParams = this.sThickBox.split(",");
							var aMatch;
							var sThickBoxActive = "true";
							var sThickBoxCaption = "";
							var sThickBoxBackground = "#E1E1E1";
							for (var i=0; i < aParams.length; i++) {
								if (aMatch = aParams[i].match(/(active\s*=\s*)(\w*)/i)) {
								  sThickBoxActive = aMatch[2];
								}
								else if (aMatch = aParams[i].match(/(caption\s*=\s*)(.*)/i)) {
								  sThickBoxCaption = unescape(aMatch[2]);
								}
								else if (aMatch = aParams[i].match(/(background\s*=\s*)(\d*)/i)) {
								  sThickBoxBackground = aMatch[2];
								}
							}
							if (sThickBoxActive.toLowerCase() == "true")
								this.byThickBox = true;
						}
						
						//Open in Thickbox
						if (this.byThickBox) {
							// Sample of modifying the ThickBox close display to the "X Close" 
							// graphic (uncomment to activate, modify for your own graphic.)
							//vPIPThickBoxCloseItem =	 "<img src='" + this.vPIPpath + "close_hover.gif' />";
							
							this.revert(this.aDIVs);
							this.thickBox_show(sThickBoxCaption, this.sReplace, Number(this.iWidth), Number(this.iHeight), sThickBoxBackground);	
						}
						// Open in page location
						else {
							//Add [X Close] button to revert to original <DIV ...> data.
						    if (this.byShowCloseBtn) {
								this.sReplace = "<div style=\"padding-right: " + (this.iWidth - 49) + "px\" ><a href=\"javascript: vPIPClose(" + this.iCurrDIVid  + ", " + this.iCurrLink + ", '" + this.sMediaFormat + "');\" title=\"Close Movie\" onMouseOver=\"document.vPIPImage" + (this.iCurrDIVid * 10) + this.iCurrLink + ".src='" + this.vPIPpath + "close_hover.gif';\" onMouseOut=\"document.vPIPImage" + (this.iCurrDIVid * 10) + this.iCurrLink + ".src='" + this.vPIPpath + "close_grey.gif';\" style=\" background: transparent;\" ><img src=\"" + this.vPIPpath + "close_grey.gif\" name=\"vPIPImage" + (this.iCurrDIVid * 10) + this.iCurrLink + "\" style=\"border: none;\"  /></a></div>" + this.sReplace;
							}
							
							// Mac Safari version 1.3.2 does not correctly close a replaced media object, so revert is disabled for Safari
							if (! (this.bySafari && this.nSafariBuild < vPIPPlayer.WORKINGSAFARIBUILD)) {
								//Close any <DIVs set to revert
								this.revert(this.aDIVs);
							}
							
							//If "hVlogTarget" class identified,
							//   add HTML outside it.
							this.sReplace = this.addOutsideTarget(sInnerHTML, this.sReplace);
							
							this.oDiv.innerHTML = this.sReplace;
                                                        var sReplaceShow = this.sReplace.replace(/</g, "&lt;");
                                                         sReplaceShow = sReplaceShow.replace(/>/g, "&gt;");
                            if (window.trace)
	                            trace("sReplaceShow: <PRE><CODE>" + sReplaceShow + "</PRE></CODE>");
							this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.OPENPOS] = true;
							this.isOpen = true;
							
						}
						//If opening in external quicktime player, then close embed div in 1/2 second
						if (this.sMediaFormat == "quicktime" && 
							this.sTarget.toLowerCase() == "quicktimeplayer")
						{
							vPIPPlayer.glDivs = this.aDIVs;
							var sCloseDiv = "vPIPPlayer.glDivs[" + this.iCurrDIVid + "][vPIPPlayer.DIVPOS].innerHTML = vPIPPlayer.glDivs[" + this.iCurrDIVid + "][vPIPPlayer.ORIGHTMLPOS];vPIPPlayer.glDivs[" + this.iCurrDIVid + "][" + this.iCurrLink + "][vPIPPlayer.OPENPOS] = false;vPIPPlayer.glDivs=null";
							setTimeout(sCloseDiv, 2000);
						}
						
					}
						
				}
				else {
					if (this.sMimeType != undefined && this.sMimeType != null) {
						setTimeout("Unsuported mime type: \"" + this.sMimeType + "\".", 0);
						if (this.oLink.href.toLowerCase().indexOf("http://") > -1)
							window.open(this.oLink.href, "_self");
						else if (this.sHREF != undefined && this.sHREF != null) 
							window.open(this.sHREF, "_self");
					}
					else  {
						setTimeout("Unsuported file extension: \"" + this.sFileExt + "\".", 0);
						if (this.oLink.href.toLowerCase().indexOf("http://") > -1)
							window.open(this.oLink.href, "_self");
						else if (this.sHREF != undefined && this.sHREF != null) 
							window.open(this.sHREF, "_self");
					}
				}
			}
			else {
				setTimeout("Missing href=\"...\" attribute.", 0);
				if (this.oLink.href.toLowerCase().indexOf("http://") > -1)
					window.open(this.oLink.href, "_self");
				else if (this.sHREF != undefined && this.sHREF != null) 
					window.open(this.sHREF, "_self");
			}
		}
		else {
			setTimeout("video Playing In Place cannot execute because the link is not identified.", 0);
			if (this.sHREF != undefined && this.sHREF != null) 
					window.open(this.sHREF, "_self");
		}
		
	}
	else {
		setTimeout("video Playing In Place cannot execute because the hVlog DIV is not identified.", 0);
		if (this.oLink.href.toLowerCase().indexOf("http://") > -1)
			window.open(this.oLink.href, "_self");
		else if (this.sHREF != undefined && this.sHREF != null) 
			window.open(this.sHREF, "_self");
		
	}
	
	return;
	
}

// Class to pass the movie MimeType, type of file (video, application, ...) and
//    sMediaFormat (quicktime, windowsmedia or flash)
function MovieType(_MimeType, _sType, _sMediaFormat, _sFileExt) {
	this.sMimeType = _MimeType;
	this.sType = _sType;
	this.sMediaFormat = _sMediaFormat;
	this.sFileExt = _sFileExt;
}

vPIPPlayer.isMovieFile = function(oLink) {
	
	var movieType = null;
	
	if (oLink != undefined && oLink != null && oLink.nodeName.toLowerCase() == "a") {
		
		//Handle mimetype					
		var sMimeType = oLink.type;
		if (sMimeType != undefined && sMimeType != null && sMimeType.length > 0) {
			var iPos = sMimeType.search(/\//);
			if (iPos > -1) 
				sMimeType = sMimeType.substring(iPos+1);
			else 
				sMimeType = null;
		}
		
		// Type of media
		var sType = "false";
		var sMediaFormat = "";
		
		// Get the file extension
		var sFileExt;
		var sHREF = vPIPPlayer.toAlphaNum(oLink.href, "~");
		var iURLGET = sHREF.indexOf('?');
		if (iURLGET > -1) {
			var sHREFFile = sHREF.substring(0, iURLGET);
			sFileExt = sHREFFile.substring(sHREFFile.lastIndexOf('.'), iURLGET).toLowerCase();
		}
		else {
			sFileExt = sHREF.substring(sHREF.lastIndexOf('.'), sHREF.length).toLowerCase();
		}
		 
		// Determine the video type to embed
		if (sMimeType != undefined && sMimeType != null && sMimeType.length > 0) {
			switch (sMimeType.toLowerCase()) {
				case "quicktime":
				case "mp4":
				case "x-m4v":
				case "x-mp3":
				case "mp3":
				case "mpeg":
				case "smil":
				case "3gpp":
					sMediaFormat = "quicktime";
					sType = "video";
					break;
				
				case "x-msvideo":
				case "x-ms-wmv":
				case "x-ms-asf":
				case "x-ms-wma":
					sMediaFormat = "windowsmedia";
					sType = "video";
					break;
				
				case "x-shockwave-flash":
				case "x-flv":
					sMediaFormat = "flash";
					sType = "application";
					break;
			 case "ogg":
				 sMediaFormat = "ogg";
				 sType = "application";
				 break;
			}
		}
		else {
			sMimeType = "";
			switch (sFileExt.toLowerCase()) {
				case ".mov":
				case ".mp4":
				case ".m4v":
				case ".mp3":
				case ".3gp":
					sMediaFormat = "quicktime";
					sType = "video";
					break;
					
				case ".smi":
				case ".smil":
					sMediaFormat = "quicktime";
					sType = "video";
					sMimeType = "smil";
					break;
					
				case ".avi":
				case ".wmv":
				case ".asf":
				case ".wma":
					sMediaFormat = "windowsmedia";
					sType = "video";
					break;
					
				case ".swf":
				case ".flv":
					sMediaFormat = "flash";
					sType = "application";
					break;
               case ".ogg":
               case ".ogv":
               case ".oga":
	               sMediaFormat = "ogg";
	               sType = "application";
	               break;
					
			}
		}
		
		movieType = new MovieType(sMimeType, sType, sMediaFormat, sFileExt);
	}
	
	return movieType;
}

vPIPPlayer.prototype.revert = function(aDIVs) {
	for(var j = 0; j < aDIVs.length; j++) {
		for(var k = vPIPPlayer.LINKSARRAYPOS; k < aDIVs[j].length; k++) {
			if (aDIVs[j][k][vPIPPlayer.REVERTPOS]) {
				aDIVs[j][vPIPPlayer.DIVPOS].innerHTML = aDIVs[j][vPIPPlayer.ORIGHTMLPOS];
				aDIVs[j][k][vPIPPlayer.OPENPOS] = false;
			}
		}
	}
	this.isOpen = false;

}

vPIPPlayer.prototype.closeThisDiv = function(aDIVs, iCurrDIVid) {
	for(var k = vPIPPlayer.LINKSARRAYPOS; k < aDIVs[iCurrDIVid].length; k++) {
		if (aDIVs[iCurrDIVid][k][vPIPPlayer.REVERTPOS]) {
			aDIVs[iCurrDIVid][vPIPPlayer.DIVPOS].innerHTML = aDIVs[iCurrDIVid][vPIPPlayer.ORIGHTMLPOS];
			aDIVs[iCurrDIVid][k][vPIPPlayer.OPENPOS] = false;
		}
	}
	this.isOpen = false;

}

vPIPPlayer.prototype.isOpen = function() {
   return this.isOpen;
}

vPIPPlayer.prototype.getInnerHTML = function()
{
	return this.aDIVs[this.iCurrDIVid][vPIPPlayer.ORIGHTMLPOS]
}

vPIPPlayer.prototype.constructDiv = function(oLink) {
	var oDiv = document.createElement("div");
	oDiv.setAttribute("class", "hVlog");
	oDiv.innerHTML = oLink.parentNode.innerHTML;
	
	return oDiv;
	
}

vPIPPlayer.prototype.addOutsideTarget = function(sInnerHTML, sRevert) {
	var iTargetStart = sInnerHTML.toLowerCase().indexOf("hvlogtarget");
	if (iTargetStart > -1) {
		iTargetStart = sInnerHTML.toLowerCase().substring(0, iTargetStart).lastIndexOf("<");
		var iTargetEnd = sInnerHTML.toLowerCase().indexOf("</a", iTargetStart);
		iTargetEnd = sInnerHTML.toLowerCase().indexOf(">", iTargetEnd);
		if (iTargetEnd > -1) {
			var sPrior = sInnerHTML.substring(0, iTargetStart);
			var sAfter = sInnerHTML.substring(iTargetEnd + 1);
			sRevert = sPrior + sRevert + sAfter;
		}
		
	}
	return sRevert;
}

// Close back to the original <div contained data.
function vPIPClose(sDivLoc, sLinkLoc, sMediaFormat) {
	var sUserAgent = navigator.userAgent;
	var byOpera = sUserAgent.indexOf('Opera') > -1;
	var bySafari = sUserAgent.indexOf('Safari') > -1;
	var nSafariBuild = -1;
	if (bySafari) {
		nSafariBuild = Number(sUserAgent.substring(sUserAgent.indexOf('Safari')+7));
	}
	//If Safari build where video file does not release or 
	// Opera with Flash where Netstream doesn't close, reload page.
	if ((bySafari && nSafariBuild < vPIPPlayer.WORKINGSAFARIBUILD) ||
		(sMediaFormat == "flash" && byOpera)) {
		document.location.reload();
	}
	else {
		if (Number(sDivLoc) != NaN && Number(sLinkLoc) != NaN) {
			var iDivLoc = Number(sDivLoc);
			var iLinkLoc = Number(sLinkLoc);
			vpipPlayerRef.aDIVs[iDivLoc][vPIPPlayer.DIVPOS].innerHTML = vpipPlayerRef.aDIVs[iDivLoc][vPIPPlayer.ORIGHTMLPOS];
			vpipPlayerRef.aDIVs[iDivLoc][iLinkLoc][vPIPPlayer.OPENPOS] = false;
			
			// Setup onclick to vPIPPlay(this) for those missing it.
			if (typeof vPIPIt == "function") {
				vPIPIt();
			}
		}
	}
	vpipPlayerRef.isOpen = false;
	
}

/**
 * Find oDiv in aDIVs array.
 * Returns array position in aDIVs that oDiv is found or -1
 */
vPIPPlayer.prototype.findDIV = function(oDiv) {
	var i;
	var iFound = -1;
	if (oDiv.id != undefined && oDiv.id != null && oDiv.id.length > 0) {
		
		for(i=0; i<this.aDIVs.length; i++) {
			if (this.aDIVs[i][vPIPPlayer.DIVIDPOS] === this.oDiv.id) {
				iFound = i;
				break;
			}
		}
	}
	
	return iFound;
}

vPIPPlayer.prototype.findLinkID = function(aDIV, iCurrLinkid) {
	var iFound = -1;
	for (var i=3; i<aDIV.length; i++) {
		if (aDIV[i][vPIPPlayer.LINKIDPOS] == iCurrLinkid) {
			iFound = i;
			break;
		}
	}
	
	return iFound;
}

vPIPPlayer.prototype.findLinkInDiv = function(aDiv, iLinkid) {
	var iLinkPosInDiv = -1;
	for(var i=3; i< aDiv.length; i++) {
		if (aDiv[i][vPIPPlayer.LINKIDPOS] != undefined) {
			if (aDiv[i][vPIPPlayer.LINKIDPOS] == iLinkid) {
				iLinkPosInDiv = i;
				break;
			}
		}
	}
	
	return iLinkPosInDiv;
}

vPIPPlayer.prototype.addEvent = function(obj, evType, fn){
	if (obj.addEventListener) {
		obj.addEventListener(evType, fn, false);
		return true;
	} else if (obj.attachEvent){
		var r = obj.attachEvent("on"+evType, fn);
		return r;
	} else {
		return false;
	}
}



/* Searching up DOM tree from oElementStart for element with nodeName == sNodeName &&
 *   attribute == sAttrName && attribute value has sAttrValue
 *  TODO
 */
vPIPPlayer.findElementbyAttrValue = function(oElementStart, sNodeName, sAttrName, sAttrValue)
{
	var oElement = null;
	
	return 	oElement;
}

vPIPPlayer.findAttribute = function(oElement, sAttribute) {
	var oValue = null;
	var attrs = oElement.attributes;
	if (attrs != undefined && attrs != null) {
		for(var i=attrs.length-1; i>=0; i--) {
			if (attrs[i].name.toLocaleLowerCase() == sAttribute.toLocaleLowerCase()) {
				oValue = attrs[i].value;
				break;
			}
		}
	}
	
	return oValue;
}

vPIPPlayer.toAlphaNum = function(sString, sAllowed) {
	var i;
	var sNewString = "";
	if (sString == undefined || sString == null) {
		return sString;
	}
	else {
		for (i=0; i<sString.length; i++) {
         	ch = sString.charAt(i);
			if (ch >= " "  && ch <= "z") {
				sNewString += sString.charAt(i);
			}
         	else if (sAllowed != undefined && sAllowed != null && sAllowed.indexOf(ch) > -1) {
				sNewString += sString.charAt(i);
         	}
		}
		return sNewString;
	}
}

vPIPPlayer.isDebugging = function(byDebugging)
{
	if (vpipPlayerRef != undefined && vpipPlayerRef != null) {
		vpipPlayerRef.byDebug = byDebugging;
		if (vpipPlayerRef.byDebug)
		{
			alert("Debugging turned on.");
		}
	}
}

/*vPIP version of ThickBox By Cody Lindley (http://www.codylindley.com)
 * Thickbox is built on top of the very light weight jquery library.
*/


vPIPPlayer.prototype.thickBox_show = function(sCaption, sEmbed, vPIP_TB_WIDTH, vPIP_TB_HEIGHT, sBackground) {//function called when the user clicks on a thickbox link
	try {
		var sUserAgent = navigator.userAgent;
		var bySafari = sUserAgent.indexOf('Safari') > -1;
		var nSafariBuild = -1;
		if (bySafari) {
			nSafariBuild = Number(sUserAgent.substring(sUserAgent.indexOf('Safari')+7));
		}


		if (typeof document.body.style.maxHeight === "undefined") {//if IE 6
			jQuery("body","html").css({height: "100%", width: "100%"});
			jQuery("html").css("overflow","hidden");
			if (document.getElementById("vPIP_TB_HideSelect") === null) {//iframe to hide select elements in ie6
				jQuery("body").append("<iframe id='vPIP_TB_HideSelect'></iframe><div id='vPIP_TB_overlay' onclick='vPIPthickBox_remove();' ></div><div id='vPIP_TB_window'></div>");
				//jQuery("#vPIP_TB_overlay").click(this.thickbox_remove);
			}
		}else{//all others
			if(document.getElementById("vPIP_TB_overlay") === null){
				jQuery("body").append("<div id='vPIP_TB_overlay' onclick='vPIPthickBox_remove();' ></div><div id='vPIP_TB_window'></div>");
				//jQuery("#vPIP_TB_overlay").click(this.thickbox_remove);
			}
		}
		if(sCaption===null){sCaption="";}

		vPIP_TB_WIDTH += 30;
		vPIP_TB_HEIGHT += 60;
		var sEntry = "<div id='vPIP_TB_caption'>"+sCaption+"</div><div id='vPIP_TB_closeWindow'><a href='javascript: none' id='vPIP_TB_closeWindowButton' title='Close'>" + vPIPThickBoxCloseItem + "</a></div><div id='vPIP_Object'>" + sEmbed + "</div>";
		document.getElementById("vPIP_TB_window").innerHTML = sEntry;
		document.getElementById("vPIP_TB_window").style.backgroundColor = sBackground;

		jQuery("#vPIP_TB_closeWindowButton").click(vPIPthickBox_remove);

		document.onkeydown = function(e){ 	
			if (e == null) { // ie
				keycode = event.keyCode;
			} else { // mozilla
				keycode = e.which;
			}
			if(keycode == 27){ // close
				vPIPthickBox_remove();
			}
		};
			
		this.thickBox_position(vPIP_TB_WIDTH, vPIP_TB_HEIGHT);
		jQuery("#vPIP_TB_window").css({display:"block"}); //for safari using css instead of show 

		if (bySafari && nSafariBuild < vPIPPlayer.WORKINGSAFARIBUILD) {
			vPIPSetThickBoxID = setTimeout(this.thickBox_refresh, 500);
		}
	} catch(e) {
		setTimeout(e, 0);
	}
}

//helper functions below

function vPIPthickBox_remove() {
	var sUserAgent = navigator.userAgent;
	var bySafari = sUserAgent.indexOf('Safari') > -1;
	var nSafariBuild = -1;
	if (bySafari) {
		nSafariBuild = Number(sUserAgent.substring(sUserAgent.indexOf('Safari')+7));
	}
	//If Safari build where video file does not release, reload page.
	if (bySafari && nSafariBuild < vPIPPlayer.WORKINGSAFARIBUILD) {
		document.location.reload();
	}
	else 
	{
		jQuery("#vPIP_TB_closeWindowButton").unbind("click");
		jQuery("#vPIP_TB_window").html(""); 
		jQuery("#vPIP_TB_window").fadeOut("fast",function(){jQuery('#vPIP_TB_window,#vPIP_TB_overlay,#vPIP_TB_HideSelect').remove();});
		if (typeof document.body.style.maxHeight == "undefined") {//if IE 6
			jQuery("body","html").css({height: "auto", width: "auto"});
			jQuery("html").css("overflow","");
		}
	
		document.onkeydown = "";
	
		// Setup onclick to vPIPPlay(this) for those missing it.
		if (typeof vPIPIt == "function") {
			vPIPIt();
		}
		
	}
	
	return false;
}

vPIPPlayer.prototype.thickBox_position = function(vPIP_TB_WIDTH, vPIP_TB_HEIGHT) {
	jQuery("#vPIP_TB_window").css({marginLeft: '-' + parseInt((vPIP_TB_WIDTH / 2),10) + 'px', width: vPIP_TB_WIDTH + 'px'});
	if ( !(jQuery.browser.msie && typeof XMLHttpRequest == 'function')) { // take away IE6
		jQuery("#vPIP_TB_window").css({marginTop: '-' + parseInt((vPIP_TB_HEIGHT / 2),10) + 'px'});
	}
		
}

vPIPPlayer.prototype.thickBox_refresh = function() 
{
	jQuery("#vPIP_TB_window").css({display:"block"}); //for safari using css instead of show 
}

// ** End of vPIP Thickbox code **

//Create and return the hVlog structure
vPIPPlayer.prototype.gen_hVlog = function(aEntries) 
{

	/*if (byStyled == undefined || byStyled == null) 
		byStyled = true;
	if (byStyled)
	{
		embedCodeShareBtnStyle = "style=\"margin-top: 3px; margin-left: 50%; margin-right: 50%; background: #DDDDDD; width: 40px; border: 1px solid #999999;\"";
		embedCodeAreaStyle = "style=\"padding: 0; margin-top: 3px; width: 500px; border: 2px solid #999999; background: #DDDDDD; font-size: 12px; \"";
		embedCodeCloseBtn = "style=\"margin: 0; font-size: 11px; \"";
		embedCodeTextarea = "style=\"font-size: 9px; margin-bottom: 5px; overflow: scroll; overflow-x: hidden; overflow-y: scroll; overflow:-moz-scrollbars-vertical; width: 480px; \"";
	}
	else
	{
		embedCodeShareBtnStyle = "";
		embedCodeAreaStyle = "";
		embedCodeCloseBtn = "";
		embedCodeTextarea = "";
	}*/
}

// ** Other code **

function vPIP_copyToClipBrd(oElement)
{
	oElement.select();
	if (window.clipboardData)
	{ 
		var rtn = clipboardData.setData('Text',oElement.value); 
		return 1; 
	} 
	else 
		return 0; 	
}

/* Get script path by id or first found */
function vPIP_getContainer(sClassName, oElement)
{
	var oContain = oElement.parentNode;
	while (oContain != undefined && oContain != null && 
			(vPIPPlayer.findAttribute(oContain, "class") == null || 
			vPIPPlayer.findAttribute(oContain, "class").toLowerCase() != sClassName.toLowerCase())) {
		oContain = oContain.parentNode;
	}
	
	return oContain;
}

function vPIP_CloseMe(aDIVs, iCurrDIVid)
{
	
}

function vPIP_getPath(sID) {
	
	//If sID != null look for script element with parameter of id=<sid>
	//If not found, look in first document.getElementsByTagName ( "script" )
	
	var scripts = document.getElementsByTagName ( "script" );
	var src;
	var index;
    var sVPIPpath = "";
    
    //id search;
	if (sID != null)
	{
		for (var i=0; i<scripts.length; i++) {
			src = scripts[i].getAttribute ( "src" );
			if (src != undefined && src != null) {
				index = src.indexOf(sID);
				if (index > -1) {
					sVPIPpath = src.substring ( 0, index);
					// Strip out anything after the url
					sVPIPpath = sVPIPpath.substr(0, sVPIPpath.lastIndexOf("/")+1);
					return sVPIPpath;
				}
			}
		}
		
	}
	
	//"vpip.js" search
	for (var i=0; i<scripts.length; i++) {
		src = scripts[i].getAttribute ( "src" );
		if (src != undefined && src != null) {
			index = src.search(/vpip.js/i);
			if (index > -1) {
				sVPIPpath = src.substring ( 0, index);
				// Strip out anything after the url
				sVPIPpath = sVPIPpath.substr(0, sVPIPpath.lastIndexOf("/")+1);
				return sVPIPpath;
			}
		}
	}

    return sVPIPpath;
}

/**
 * (in use?)
 */
function vPIP_setEmbedFormat(oSelect, sEmbedCodeArea, sScripts, aEmbeds)
{
	oEmbedCodeArea = document.getElementById(sEmbedCodeArea);
	if (oSelect.options[oSelect.selectedIndex].text != "All")
	{
		oEmbedCodeArea.value = unescape(sScripts) + 
							   "<div class=\"hVlog\" style=\"text-align: center\">" + 
							   aEmbeds[oSelect.selectedIndex] +
							   "</div>";
	}
	else
	{
		oEmbedCodeArea.value = unescape(sScripts) + 
							   aEmbeds[oSelect.selectedIndex] +
							   "</div>";
	}
}

/**
 * vPIP_setEmbed sets the embed code to copy and share to the current hVlog entry.
 * oElement is the HTML element from where the request came, usually a anchor.
 * sEmbedCodeArea is the ID of the textArea where the embed code is inserted.
 */
function vPIP_setEmbed(oElement, sEmbedCodeArea, byIncludePosterImage, byInsertCustomCSS)
{
	//var wasOpen = false;
//	if (vpipPlayerRef != undefined && vpipPlayerRef.isOpen)
//	{
//		vPIPClose(vpipPlayerRef.iCurrDIVid, vpipPlayerRef.iCurrLink, vpipPlayerRef.sMediaFormat);
//		var sPostID = sEmbedCodeArea.substr(14);
//		wasOpen = true;
//		vPIP_setVisible("divEmbedCode" + sPostID , true);
	//	oEmbedCodeArea = document.getElementById(sEmbedCodeArea);
	//	oEmbedCodeArea.value = "Sorry, embed code only available when movie is closed.";
//	}
//	else
//	{
		var sUserAgent = navigator.userAgent;
		var bySafari = sUserAgent.indexOf('Safari') > -1;
		var byOpera = sUserAgent.indexOf('Opera') > -1;
		var byIE7 = sUserAgent.indexOf("MSIE 7") > -1;
		var byIE6 = sUserAgent.indexOf("MSIE 6") > -1;
	
		if (byIncludePosterImage == undefined || byIncludePosterImage == null) 
			byIncludePosterImage = true;
			
		if (byInsertCustomCSS == undefined || byInsertCustomCSS == null) 
			byInsertCustomCSS = true;
	
		oEmbedCodeArea = document.getElementById(sEmbedCodeArea);
		
		if (oEmbedCodeArea.value.trim().length == 0)
		{
			var oDiv = vPIP_getContainer("hVlog", oElement)
			if (oDiv != undefined && oDiv != null) 
			{
				
				var byIDIsThere = false;
				//Locate the ID
				var sID = null;
				var anchors = oDiv.getElementsByTagName("a");
				for (var i=0; i<anchors.length; i++) {
					var sOnclick = anchors[i].getAttribute("onclick");
					if (typeof sOnclick == 'function')
					{
						sOnclick = sOnclick.toString();
					}
					if (sOnclick != undefined && sOnclick != null) {
						var iStart = sOnclick.indexOf("id=");
						if (iStart > -1) {
							var iEnd = sOnclick.indexOf(",", iStart);
							sID = sOnclick.substring ( iStart+3, iEnd);
							byIDIsThere = true;
							break;
						}
					}
				}
				
				if (sID == null)
				{
					sID = escape(window.location.href + "-" + (new Date()).getTime());
				}
				
				sScripts = " 	<script src=\"" + vPIP_getPath(sID) + "vpip.js?id=" + sID + "\" type=\"text/javascript\"></script>";
				
				// Get DIV parameters to include
				aDivAttribs = oDiv.attributes;
				sDiv = "<div ";
				for (i=0; i<aDivAttribs.length; i++)
				{
					if (aDivAttribs[i].value != null && aDivAttribs[i].value != undefined &&
						aDivAttribs[i].value != "null" && aDivAttribs[i].value.length > 0)
						sDiv += aDivAttribs[i].name + "=\"" + aDivAttribs[i].value + "\" ";
				}
				sDiv += ">"
		
			if (vpipPlayerRef != undefined && vpipPlayerRef.isOpen)
				var sEmbed = vpipPlayerRef.getInnerHTML(); 
			else
				var sEmbed = oDiv.innerHTML;
			
				sEmbed = sEmbed.replace(/\n/g,"");
				if (!byIDIsThere)
				{
					var sReplace = "vPIPPlay(this,'id=" + sID + ",";
					sEmbed = sEmbed.replace(/vPIPPlay\(this\,\'/ig, sReplace);
				}
				//Put in new class identifier 
				iDivIDStart = sEmbed.indexOf("divEmbedCodeShare")+17;
				if (iDivIDStart > -1)
				{
					iDivIDEnd = sEmbed.indexOf("\"", iDivIDStart);
					sOldDivID = sEmbed.substring(iDivIDStart, iDivIDEnd);
					sNewDivID = String((new Date()).getTime());
					sFind = sOldDivID + "\"";
					sReplace = sNewDivID + "\"";
					sEmbed = sEmbed.replace(sFind, sReplace, "gi");
					sFind = sOldDivID + "\'";
					sReplace = sNewDivID + "\'";
					sEmbed = sEmbed.replace(sFind, sReplace, "gi");
				}
				// If not byIncludePosterImage, parse out image a href. 
				if (! byIncludePosterImage)
				{
					iImgPos = sEmbed.toLowerCase().indexOf("<img ");
					if (iImgPos > -1)
					{
						sEmbedImgSrchStart = sEmbed.substr(0, iImgPos);
						sEmbedImgSrchEnd = sEmbed.substr(iImgPos);
						iLinkStart = sEmbedImgSrchStart.toLowerCase().lastIndexOf("<a ");
						iLinkEnd = sEmbedImgSrchEnd.toLowerCase().indexOf("</a")+iLinkStart;
						sEmbed = sEmbed.substr(0, iLinkStart-1) + sEmbed.substr(iLinkEnd+1);
					}
				}
				
				//If adding non-inline CSS
				if (byInsertCustomCSS)
				{
					if (! byIE6 && ! byIE7)
					{
						//TODO:  Move to where error occurs (on stylesheet load?)
						try {
							sDiv = insertCustomCSS(sDiv, false);
							sEmbed = insertCustomCSS(sEmbed);
						}
						catch (err)
						{
							
						}
					}
				}
				
				oEmbedCodeArea.value = sScripts + sDiv + sEmbed + "</div>";
			}
		
		}
//	if (wasOpen)
//	{
//		vPIP_setVisible("divEmbedCodeShare" + sPostID, false);
//	}
//	}
}

/**
 * insertCustomCSS inserts non-inline CSS into tags
 * sHTML is a string of HTML 
 * returns HTML string with inserted custom CSS
 */
function insertCustomCSS(sHTML, byCheckIE)
{
	if (byCheckIE == null || byCheckIE == undefined)
		byCheckIE = true;
		
	var sUserAgent = navigator.userAgent;
	var bySafari = sUserAgent.indexOf('Safari') > -1;
	var byOpera = sUserAgent.indexOf('Opera') > -1;
	var byIE7 = sUserAgent.indexOf("MSIE 7") > -1;
	var byIE6 = sUserAgent.indexOf("MSIE 6") > -1;

	var sClass = "";
	var sCSS = "";
	var sQuoteType = "D";

	var sHTMLSub = sHTML;
	var iClassStart = 0;
	var iClassSubStart = sHTMLSub.search(/\bclass\b\s*=/i);
	if (iClassSubStart > -1)
	{
		sHTMLSub = sHTML.substr(iClassSubStart);
		//iClassStart += iClassSubStart;
	}
	while (iClassSubStart > -1)
	{
		var iClassNameEnd = -1;
		if (byCheckIE && (byIE6 || byIE7))
		{
			var iClassNameStart = sHTMLSub.indexOf("=");
			iClassNameEnd = vPIP_GetFirstNonAlphaNum(sHTMLSub, iClassNameStart+1);
			sQuoteType = "D";
		}
		else
		{
			var iClassNameStart = vPIP_GetFirstQuote(sHTMLSub, 0);
			if (sHTMLSub.substr(iClassNameStart,1) == "'")
			{
				iClassNameEnd = sHTMLSub.indexOf("'", iClassNameStart+1);
				sQuoteType = "S";
			}
			else
			{
				iClassNameEnd = sHTMLSub.indexOf("\"", iClassNameStart+1);
				sQuoteType = "D";
			}
		}
		sClass = sHTMLSub.substring(iClassNameStart+1, iClassNameEnd);
		var oStyle = (vPIP_getCSSRule("." + sClass));
		if (oStyle && oStyle.style != undefined)
		{
			sCSS = (vPIP_getCSSRule("." + sClass)).style.cssText;
			
			//alert(sClass + " sCSS: " + sCSS)
			//See if style is already set
			var iTagStart = sHTML.substr(0, iClassStart+iClassSubStart).lastIndexOf("<");
			var iTagEnd = sHTML.substr(iTagStart).indexOf(">");
			var iStyleStart = sHTML.substr(iTagStart,iTagEnd).search(/\bstyle\bs*=/i);
			//alert("HTML before insert: " + sHTML)
			if (iStyleStart > -1)
			{
				var iStyleEnd = vPIP_GetFirstQuote(sHTML, iTagStart+iStyleStart+1);
				iStyleEnd = vPIP_GetFirstQuote(sHTML, iStyleEnd+1);
				//Check if CSS is already in style="..."
				var sCSSCompare = "";
				//Check only first 50 chars. 
				// (kludge to fix for when same entries in different order)
				if (sCSS.length > 50)
					sCSSCompare = sCSS.toLowerCase().substr(0,50);
				else
					sCSSCompare = sCSS.toLowerCase();
				
				if (sHTML.substring(iTagStart+iStyleStart,iStyleEnd).toLowerCase().indexOf(sCSSCompare) == -1)
				{
					sHTML = sHTML.substring(0, iStyleEnd) + "; " + sCSS + 
							sHTML.substring(iStyleEnd);
					iClassStart = iTagStart+iTagEnd+sCSS.length;
				}
				else
				{
					iClassStart = iTagStart+iTagEnd;
				}
			}
			else
			{
				iClassStart += iClassNameEnd+iClassSubStart;
				if (sQuoteType == "D")
				{
					sHTML = sHTML.substring(0, iClassStart+1) + " style=\"" + sCSS + "\" " +
							sHTML.substring(iClassStart+1);
				}
				else 
				{
					sHTML = sHTML.substring(0, iClassStart+1) + " style='" + sCSS + "' " +
							sHTML.substring(iClassStart+1);
				}
				iClassStart += sCSS.length + 9;
			}
			//alert("iStyleStart: " + iStyleStart + " for " + sClass + " with css rule \"" + sCSS + 
			//	"\" \nResulting in: " + 
			//	sHTML)
			iClassSubStart = sHTML.substr(iClassStart).search(/\bclass\b\s*=/i);
			if (iClassSubStart > -1)
				sHTMLSub = sHTML.substr(iClassStart+iClassSubStart);
		}
		//If no Style Sheet entry for class, find the next one.
		else
		{
			if (iClassSubStart > 0)
				iClassStart += iClassSubStart;
			else
				iClassStart += 10;
			iClassSubStart = sHTML.substr(iClassStart).search(/\bclass\b\s*=/i);
			if (iClassSubStart > -1)
				sHTMLSub = sHTML.substr(iClassStart+iClassSubStart);
		}
	}
	
	return sHTML;
}

function vPIP_GetFirstQuote(sText, iIndexStart)
{
	if (iIndexStart == null || iIndexStart == undefined)
		iIndexStart = 0;
	for (var i=iIndexStart; i<sText.length; i++)
	{
    	ch = sText.charAt(i);
		if (ch == "\"" || ch == "'")
			return i;
	}
	
	return -1;
}

function vPIP_GetFirstNonAlphaNum(sText, iIndexStart)
{
	if (iIndexStart == null || iIndexStart == undefined)
		iIndexStart = 0;
	for (var i=iIndexStart; i<sText.length; i++)
	{
     	ch = sText.charAt(i);
		if (!(ch >= "0" && ch <="9") &&
			!(ch >="A" && ch <= "z")) 
		{
			return i;
		}
	}
	
	return -1;
	//return sText.substr(iIndexStart).search(/\w/);
}

function vPIP_getCSSRule(ruleName, deleteFlag) {               // Return requested style obejct
	if (deleteFlag == undefined || deleteFlag == null) 
		deleteFlag = "";

   ruleName=ruleName.toLowerCase();                       // Convert test string to lower case.
   if (document.styleSheets) {                            // If browser can play with stylesheets
      for (var i=0; i<document.styleSheets.length; i++) { // For each stylesheet
         var styleSheet=document.styleSheets[i];          // Get the current Stylesheet
         var ii=0;                                        // Initialize subCounter.
         var cssRule=false;                               // Initialize cssRule. 
         do {                                             // For each rule in stylesheet
            if (styleSheet.cssRules) {                    // Browser uses cssRules?
               cssRule = styleSheet.cssRules[ii];         // Yes --Mozilla Style
            } else {                                      // Browser usses rules?
               cssRule = styleSheet.rules[ii];            // Yes IE style. 
            }                                             // End IE check.
            if (cssRule && cssRule.selectorText != undefined)  {                               // If we found a rule...
               if (cssRule.selectorText.toLowerCase()==ruleName) { //  match ruleName?
                  if (deleteFlag=='delete') {             // Yes.  Are we deleteing?
                     if (styleSheet.cssRules) {           // Yes, deleting...
                        styleSheet.deleteRule(ii);        // Delete rule, Moz Style
                     } else {                             // Still deleting.
                        styleSheet.removeRule(ii);        // Delete rule IE style.
                     }                                    // End IE check.
                     return true;                         // return true, class deleted.
                  } else {                                // found and not deleting.
                     return cssRule;                      // return the style object.
                  }                                       // End delete Check
               }                                          // End found rule name
            }                                             // end found cssRule
            ii++;                                         // Increment sub-counter
         } while (cssRule)                                // end While loop
      }                                                   // end For loop
   }                                                      // end styleSheet ability check
   return false;                                          // we found NOTHING!
}                                                         // end getCSSRule 

/**
 * vPIP_getStyle gets the style of a element.
 * el is the HTML element.
 * styleProp is the property style to return.
 * returns the style property.
 */
function vPIP_getStyle(el,styleProp)
{
	var x = document.getElementById(el);
	if (x.currentStyle)
		var y = x.currentStyle[styleProp];
	else if (window.getComputedStyle)
		var y = document.defaultView.getComputedStyle(x,null).getPropertyValue(styleProp);
	return y;
}

function vPIP_setVisible(sElement, byShow)
{
	if (document.layers)
	{
		vista = byShow ? 'show' : 'hide'
		document.layers[sElement].visibility = vista;
		if (byShow)
			document.layers[sElement].display = 'block';
		else
			document.layers[sElement].display = 'none';
	}
	else if (document.all)
	{
		vista = byShow ? 'visible'	: 'hidden';
		document.all[sElement].style.visibility = vista;
		if (byShow)
			document.all[sElement].style.display = 'block';
		else
			document.all[sElement].style.display = 'none';
	}
	else if (document.getElementById)
	{
		oElement = document.getElementById(sElement);
		vista = byShow ? 'visible' : 'hidden';
		oElement.style.visibility = vista;
		if (byShow)
			oElement.style.display = 'block';
		else
			oElement.style.display = 'none';

	}
}

String.prototype.trim = function() {
	return this.replace(/^\s+|\s+$/g,"");
}
String.prototype.ltrim = function() {
	return this.replace(/^\s+/,"");
}
String.prototype.rtrim = function() {
	return this.replace(/\s+$/,"");
}

Array.prototype.find = function(searchStr) {
  var returnArray = false;
  for (i=0; i<this.length; i++) {
    if (typeof(searchStr) == 'function') {
      if (searchStr.test(this[i])) {
        if (!returnArray) { returnArray = [] }
        returnArray.push(i);
      }
    } else {
      if (this[i]===searchStr) {
        if (!returnArray) { returnArray = [] }
        returnArray.push(i);
      }
    }
  }
  return returnArray;
}

Array.prototype.findFirst = function(searchStr) {
  for (i=0; i<this.length; i++) {
    if (typeof(searchStr) == 'function') {
      if (searchStr.test(this[i])) {
        return i;
      }
    } else {
      if (this[i]===searchStr) {
         return i;
      }
    }
  }
  return null;
}
