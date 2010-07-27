<jsp:include page="header.jsp">
    <jsp:param name="title" value="ParseViz" />
</jsp:include>

<%@ page
    language="java"
    contentType="text/html;charset=UTF-8"
    pageEncoding="UTF-8"
    import="java.net.URLEncoder"
    import="org.apache.commons.lang.*"
    import="edu.stanford.nlp.trees.Tree"
    import="cc.vidr.parseviz.ParseViz"
%>

<%
String s = request.getParameter("q");
if(s == null)
    s = "Colorless green ideas sleep furiously.";
String q = URLEncoder.encode(s, "UTF-8");
Tree tree = ParseViz.parse(s);
%>

<form action="" method="get">
    <p>
    <input type="text" name="q" size="80"
        value="<% StringEscapeUtils.escapeHtml(out, s); %>" />
    <input type="submit" />
    </p>
</form>

<h2>Parse Tree</h2>
<pre><% ParseViz.printTree(tree, out); %></pre>
<a href="?type=tree&amp;format=png&amp;q=<%=q%>">
    <img src="?type=tree&amp;format=png&amp;q=<%=q%>"
        style="max-width:100%" alt="Parse Tree" />
</a>

<h2>Stanford Dependencies</h2>
<pre><% ParseViz.printDependencies(tree, out); %></pre>
<a href="?type=deps&amp;format=png&amp;q=<%=q%>">
    <img src="?type=deps&amp;format=png&amp;q=<%=q%>"
        style="max-width:100%" alt="Stanford Dependencies" />
</a>

<jsp:include page="footer.jsp" />
