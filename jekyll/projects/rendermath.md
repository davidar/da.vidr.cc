---
layout: project-page
title: RenderMath
head: |
    <!--
    <style type="text/css">#jsMath_Warning {display: none}</style>
    <script type="text/javascript" src="http://static.da.vidr.cc/jsmath/plugins/noImageFonts.js"></script>
    -->
    <script type="text/javascript" src="http://static.da.vidr.cc/jsmath/jsMath.js"></script>
    <script type="text/javascript">
    jsMath.Setup.Script("plugins/tex2math.js");
    jsMath.Extension.Require("AMSmath");
    jsMath.Controls.cookie.scale = 133; // scale font by 133%
    </script>
    <link type="text/css" rel="stylesheet" href="http://alexgorbatchev.com/pub/sh/current/styles/shThemeDefault.css"></link>
    <script type="text/javascript" src="http://alexgorbatchev.com/pub/sh/current/scripts/shCore.js"></script>
    <script type="text/javascript" src="http://alexgorbatchev.com/pub/sh/current/scripts/shBrushXml.js"></script>
---

Render TeX-style math as HTML.

Click on the math below to change it, hit enter or click elsewhere on the page to render it. HTML code for the math is displayed at the bottom of the page.

<div class="centred">
    <div id="mathdisplay"></div>
    <input id="mathinput" class="centred" type="text" size="40" value="e^{i\pi}+1=0" />
</div>

Download math as a single GIF image:
<a href="http://www.problem-solving.be/cgi-bin/mathtex.cgi?" class="mathtexlink">[1]</a> or
<a href="http://www.openmaths.org/cgi-bin/mathtex.cgi?" class="mathtexlink">[2]</a> or
<a href="http://www.forkosh.dreamhost.com/mathtex.cgi?" class="mathtexlink">[3]</a> or
<a href="http://www.cyberroadie.org/cgi-bin/mathtex.cgi?" class="mathtexlink">[4]</a>
(rendering provided by <a href="http://www.forkosh.dreamhost.com/source_mathtex.html#webservice">mathTeX web services</a>)

<hr />

<div id="mathdiv"></div>

<script type="text/javascript">
// <![CDATA[
$('#mathdisplay').click(function() {
    $('#mathdisplay').hide();
    $('#mathinput').show();
    $('#mathinput').focus();
    return false;
});
$('#mathinput').blur(function() {
    var s = $('#mathinput').val();
    // make sure math contains something other than whitespace:
    if(s.match(/^\s*$/)) s = '\\ldots';
    
    $('#mathdisplay').text('$$ ' + s + ' $$');
    jsMath.ConvertTeX('mathdisplay');
    jsMath.ProcessBeforeShowing('mathdisplay');
    jsMath.Synchronize(function() {
        var html = $('#mathdisplay').html();
        html = html.match(/.{0,80}[> ]/g).join('\n'); // wrap html
        $('#mathdiv').html('<pre id="mathpre" class="brush:html"></pre>');
        $('#mathpre').text(html);
        SyntaxHighlighter.highlight();
    });
    
    $('.mathtexlink').each(function() {
        var server = $(this).attr('href').split('?',1)[0];
        $(this).attr('href', server + '?' + s);
    });
    
    $('#mathinput').hide();
    $('#mathdisplay').show();
});
$('input').live("keypress", function(e) {
    if(e.keyCode == 13) $(this).blur();
});
$('#mathinput').blur();
// ]]>
</script>
