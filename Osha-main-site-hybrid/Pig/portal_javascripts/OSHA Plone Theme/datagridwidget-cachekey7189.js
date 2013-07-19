
/* - datagridwidget.js - */
// http://osha.europa.eu/portal_javascripts/datagridwidget.js?original=1
dataGridFieldFunctions=new Object()
dataGridFieldFunctions.getInputOrSelect=function(node){var inputs=node.getElementsByTagName("input");if(inputs.length>0){return inputs[0]}
var selects=node.getElementsByTagName("select");if(selects.length>0){return selects[0]}
return null}
dataGridFieldFunctions.getWidgetRows=function(currnode){tbody=this.getParentElementById(currnode,"datagridwidget-tbody");return this.getRows(tbody)}
dataGridFieldFunctions.getRows=function(tbody){var rows=new Array()
child=tbody.firstChild;while(child!=null){if(child.tagName!=null){if(child.tagName.toLowerCase()=="tr"){rows=rows.concat(child)}}
child=child.nextSibling}
return rows}
dataGridFieldFunctions.autoInsertRow=function(e){var currnode=window.event?window.event.srcElement:e.currentTarget;var tbody=this.getParentElement(currnode,"TBODY");var rows=this.getRows(tbody);var lastRow=rows[rows.length-1];var thisRow=this.getParentElementById(currnode,"datagridwidget-row");if(rows.length-1==(thisRow.rowIndex)){var newtr=this.createNewRow(lastRow);lastRow.parentNode.insertBefore(newtr,lastRow);this.updateOrderIndex(tbody)}}
dataGridFieldFunctions.addRowAfter=function(currnode){var tbody=this.getParentElementById(currnode,"datagridwidget-tbody");var thisRow=this.getParentElementById(currnode,"datagridwidget-row");var newtr=this.createNewRow(thisRow);thisRow.parentNode.insertBefore(newtr,thisRow);this.updateOrderIndex(tbody)}
dataGridFieldFunctions.addRow=function(id){var tbody=document.getElementById("datagridwidget-tbody-"+id);var rows=this.getRows(tbody);var lastRow=rows[rows.length-1];var oldRows=rows.length;var newtr=this.createNewRow(lastRow);newNode=lastRow.parentNode.insertBefore(newtr,lastRow);this.updateOrderIndex(tbody)}
dataGridFieldFunctions.createNewRow=function(tr){var tbody=this.getParentElementById(tr,"datagridwidget-tbody");var rows=this.getRows(tbody);var lastRow=rows[rows.length-1];var newtr=document.createElement("tr");newtr.setAttribute("id","datagridwidget-row");newtr.setAttribute("class","datagridwidget-row");child=lastRow.firstChild;while(child!=null){newchild=child.cloneNode(true);newtr.appendChild(newchild);child=child.nextSibling}
return newtr}
dataGridFieldFunctions.removeFieldRow=function(node){var row=this.getParentElementById(node,'datagridwidget-row');var tbody=this.getParentElementById(node,'datagridwidget-tbody');tbody.removeChild(row)}
dataGridFieldFunctions.moveRowDown=function(currnode){var tbody=this.getParentElementById(currnode,"datagridwidget-tbody");var rows=this.getWidgetRows(currnode);var row=this.getParentElementById(currnode,"datagridwidget-row");if(row==null){alert("Couldn't find DataGridWidget row");return}
var idx=null
for(var t=0;t<rows.length;t++){if(rows[t]==row){idx=t;break}}
if(idx==null)
return;if(idx+2==rows.length){var nextRow=rows.item[0]
this.shiftRow(row,nextRow)} else{var nextRow=rows[idx+1]
this.shiftRow(nextRow,row)}
this.updateOrderIndex(tbody)}
dataGridFieldFunctions.moveRowUp=function(currnode){var tbody=this.getParentElementById(currnode,"datagridwidget-tbody");var rows=this.getWidgetRows(currnode);var row=this.getParentElementById(currnode,"datagridwidget-row");if(row==null){alert("Couldn't find DataGridWidget row");return}
var idx=null
for(var t=0;t<rows.length;t++){if(rows[t]==row){idx=t;break}}
if(idx==null)
return;if(idx==0){var previousRow=rows[rows.length-1]
this.shiftRow(row,previousRow)} else{var previousRow=rows[idx-1];this.shiftRow(row,previousRow)}
this.updateOrderIndex(tbody)}
dataGridFieldFunctions.shiftRow=function(bottom,top){bottom.parentNode.insertBefore(bottom,top)}
dataGridFieldFunctions.updateOrderIndex=function(tbody){var xre=new RegExp(/^orderindex__/)
var idx=0;var cell;var rows=this.getRows(tbody);for(var i=0;i<rows.length-1;i++){for(var c=0;(cell=rows[i].getElementsByTagName('INPUT').item(c));c++){if(cell.getAttribute('id')){if(xre.exec(cell.id)){cell.value=idx}}
this.updateRadioButtonGroupName(this.getParentElement(cell,"TR"),idx);idx++}}}
dataGridFieldFunctions.updateRadioButtonGroupName=function(row,newIndex){var cell;var xre=new RegExp(/^radio/)
var xre2=new RegExp(/^checkbox/)
for(var c=0;(cell=row.getElementsByTagName('INPUT').item(c));c++){if(cell.getAttribute('type')){var type=cell.getAttribute('type');if(xre.exec(type)||xre2.exec(type)){var name=cell.getAttribute("NAME")
if(name==null) continue;var baseLabel=name.substring(0,name.lastIndexOf("."));cell.setAttribute("NAME",baseLabel+"."+newIndex)}}}}
dataGridFieldFunctions.getParentElement=function(currnode,tagname){tagname=tagname.toUpperCase();var parent=currnode.parentNode;while(parent.tagName.toUpperCase()!=tagname){parent=parent.parentNode;if(parent.tagName.toUpperCase()=="BODY")
return null}
return parent}
dataGridFieldFunctions.getParentElementById=function(currnode,id){id=id.toLowerCase();var parent=currnode.parentNode;while(true){var parentId=parent.getAttribute("id");if(parentId!=null){if(parentId.toLowerCase().substring(0,id.length)==id) break}
parent=parent.parentNode;if(parent.tagName.toUpperCase()=="BODY")
return null}
return parent}
