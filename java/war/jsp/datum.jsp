<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<%--
 Copyright (C) 2010  David Roberts <d@vidr.cc>

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU Affero General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Affero General Public License for more details.

 You should have received a copy of the GNU Affero General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
--%>

<%@ page
    language="java"
    contentType="text/html;charset=UTF-8"
    pageEncoding="UTF-8"
    import="java.io.*"
    import="java.net.*"
    import="cc.vidr.*"
    import="cc.vidr.datum.*"
    import="org.apache.commons.lang.*"
%>

<%!
void printFact(JspWriter out, Literal fact) throws IOException {
    Literal[] proof = Server.getProof(fact);
    String response = QA.respond(fact);
    out.println("<li>");
    if(response != null)
        out.print(StringEscapeUtils.escapeHtml(response));
    else
        out.print(fact);
    if(proof.length > 0) {
        int id = (int) UniqueID.get();
        out.println(
                "<a class=\"toggleproof\" id=\"toggleproof" + id + "\">" +
                ", because:</a>" +
                "<ul class=\"proof\" id=\"proof" + id + "\" " +
                "style=\"display:none\">");
        for(Literal literal : proof)
            printFact(out, literal);
        out.println("</ul>");
    } else {
        out.println(".");
    }
    out.println("</li>");
}
%>

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />
<title>Datum</title>
<link type="text/css" rel="stylesheet" href="/media/css/datum.css" />
<script type="text/javascript" src="http://www.google.com/jsapi"></script>
<script type="text/javascript">google.load("jquery", "1");</script>
</head>
<body>

<%
String q = request.getParameter("q");
if(q == null) q = "";
%>

<div id="logo">datum&#8592;</div>
<form method="get" action=""><p>
<input name="q" id="q" value="<%=q%>" size="55" />
<input type="submit" value="Ask" />
</p></form>

<%
if(q.isEmpty()) {
%>
<div id="examples">
<ul>
<%
    String[] questions = {
        "Who are Hans Albert Einstein's ancestors?",
        "Who are the sons of Albert Einstein?",
        "Who were Hermann Einstein's children?",
    };
    for(String question : questions) {
%>
<li>
<a href="?q=<%=URLEncoder.encode(question, "UTF-8")%>"><%=question%></a>
</li>
<%
    }
%>
</ul>
</div>
<%
} else {
%>
<div id="response">
<ul>
<%
    Literal[] facts = QA.query(q);
    for(Literal fact : facts)
        printFact(out, fact);
    if(facts.length == 0) {
%>
<li>I don't know.</li>
<%
    }
%>
</ul>
</div>
<%
}
%>

<script type="text/javascript">
$(".toggleproof").click(function(){
    $("#" + $(this).attr("id").substring(("toggle").length)).toggle("slow");
});
</script>

<p>&nbsp;</p>
<p>&nbsp;</p>
<div id="footer">
<p>
&copy; 2010
<a href="mailto:&#100;&#064;&#118;&#105;&#100;&#114;&#046;&#099;&#099;">
David Roberts</a>.
<a href="http://da.vidr.cc/projects/datum/">Project page</a>.
</p>
<p>
<a href="http://www.fsf.org/licensing/licenses/agpl-3.0.html">
<img src="http://www.gnu.org/graphics/agplv3-155x51.png" alt="AGPLv3" /></a>
</p>
</div>

<script type="text/javascript">
var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
</script>
<script type="text/javascript">
try {
var pageTracker = _gat._getTracker("UA-3316928-4");
pageTracker._setDomainName(".da.vidr.cc");
pageTracker._trackPageview();
} catch(err) {}
</script>

</body>
</html>
