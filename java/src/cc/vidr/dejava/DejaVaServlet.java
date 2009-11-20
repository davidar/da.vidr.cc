/*
 * Copyright (C) 2009  David Roberts <d@vidr.cc>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

package cc.vidr.dejava;

import java.io.IOException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.commons.jci.problems.CompilationProblem;
import org.apache.commons.lang.StringEscapeUtils;

import cc.vidr.StreamUtils;

@SuppressWarnings("serial")
public class DejaVaServlet extends HttpServlet {
    public void doGet(HttpServletRequest req, HttpServletResponse resp)
    throws IOException {
        resp.setContentType("text/html");
        StreamUtils.pipe(resp.getWriter(),
                DejaVaServlet.class.getResourceAsStream("dejava.html"));
    }
    
    public void doPost(HttpServletRequest req, HttpServletResponse resp)
    throws IOException {
        resp.setContentType("application/xml");
        
        String source = req.getParameter("source");
        String filename = req.getParameter("classname") + ".java";
        
        JavaSourceCompiler compiler =
            new JavaSourceCompiler(filename, source);
        compiler.compile();

        resp.getWriter().println(
                "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>");
        resp.getWriter().println("<dejava>");
        
        resp.getWriter().println("<errors>");
        for(CompilationProblem err : compiler.getErrors()) {
            resp.getWriter().print("<error>");
            StringEscapeUtils.escapeXml(resp.getWriter(), err.toString());
            resp.getWriter().println("</error>");
        }
        resp.getWriter().println("</errors>");

        resp.getWriter().println("<warnings>");
        for(CompilationProblem warn : compiler.getWarnings()) {
            resp.getWriter().print("<warning>");
            StringEscapeUtils.escapeXml(resp.getWriter(), warn.toString());
            resp.getWriter().println("</warning>");
        }
        resp.getWriter().println("</warnings>");
        
        resp.getWriter().println("<classes>");
        if(compiler.successful())
            for(String className : compiler.getClassNames()) {
                resp.getWriter().print(
                        "<class classname=\"" + className + "\">");
    
                JavaClassDecompiler decompiler = new JavaClassDecompiler(
                        className, compiler.getClassData(className));
                try {
                    decompiler.decompile();
                    StringEscapeUtils.escapeXml(
                            resp.getWriter(), decompiler.getAssemblyCode());
                } catch (ClassFormatError e) {
                    StringEscapeUtils.escapeXml(resp.getWriter(),
                            "; Error decompiling class file:\n" +
                            "; " + e.toString().replace("\n", "\n; "));
                }
                resp.getWriter().println("</class>");
            }
        resp.getWriter().println("</classes>");

        resp.getWriter().println("</dejava>");
    }
}
