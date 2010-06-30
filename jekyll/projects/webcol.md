---
layout: project-page
title: WebCol
head: |
    <link rel="stylesheet" media="screen" type="text/css" href="http://static.da.vidr.cc/colorpicker/css/colorpicker.css" />
    <script type="text/javascript" src="http://static.da.vidr.cc/colorpicker/js/colorpicker.js"></script>
    <style type="text/css">
    #color-bg-div {
        width: 90%;
        background-color: #ffffff;
        border: 1px solid;
        padding: 1em;
        margin: 0 auto;
        color: black;
    }
    #color-title-div {
        font-size: 3em;
        color: #000000;
    }
    #color-text-div {
        color: #000000;
    }
    #block-wrap {
        border: 1px solid black;
        height: 100px;
    }
    #color-blocka-div, #color-blockb-div {
        height: 100px;
        font-size: 4em;
        text-align: center;
        float: left;
        width: 50%;
    }
    #color-blocka-div {
        background-color: #dddddd;
    }
    #color-blockb-div {
        background-color: #aaaaaa;
    }
    </style>
---

Compare colors for website designs.

<table id="colorpick">
<tr id="colorpick-bg">     <th class="align-right">Background</th> <td><input id="color-bg"     name="color-bg"     size="13" type="text" value="#ffffff" /></td> </tr>
<tr id="colorpick-title">  <th class="align-right">Title</th>      <td><input id="color-title"  name="color-title"  size="13" type="text" value="#000000" /></td> </tr>
<tr id="colorpick-text">   <th class="align-right">Text</th>       <td><input id="color-text"   name="color-text"   size="13" type="text" value="#000000" /></td> </tr>
<tr id="colorpick-blocka"> <th class="align-right">Block A</th>    <td><input id="color-blocka" name="color-blocka" size="13" type="text" value="#dddddd" /></td> </tr>
<tr id="colorpick-blockb"> <th class="align-right">Block B</th>    <td><input id="color-blockb" name="color-blockb" size="13" type="text" value="#aaaaaa" /></td> </tr>
<tr><td colspan="2" class="align-center">Click on the above text fields to open <a href="http://eyecon.ro/colorpicker/">color picker</a>.</td></tr>
</table>

<hr />

<div id="color-bg-div" class="bg">
    <div id="color-title-div" class="fg">Lorem Ipsum</div>
    <div id="color-text-div" class="fg"><strong>Lorem ipsum</strong> dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</div>
    <br />
    <div id="block-wrap"><div id="color-blocka-div" class="bg">A</div><div id="color-blockb-div" class="bg">B</div></div>
</div>

<script type="text/javascript">
// <![CDATA[
function set_color(el, hex) {
    $(el).ColorPickerSetColor(hex);
    $(el).val(hex);
    id = $(el).attr('id') + '-div';
    div = $('#' + id);
    if(div.attr('class') == 'bg')
        div.css('backgroundColor', hex);
    else
        div.css('color', hex);
}

$('#color-bg, #color-title, #color-text, #color-blocka, #color-blockb')
.ColorPicker({
    onShow: function(colpkr) {$(colpkr).fadeIn(500); return false;},
    onHide: function(colpkr) {$(colpkr).fadeOut(500);return false;},
    onSubmit: function(hsb, hex, rgb, el) {set_color(el, '#' + hex);},
    onBeforeShow: function() {set_color(this, this.value);}
}).bind('keyup', function() {set_color(this, this.value);});
// ]]>
</script>
