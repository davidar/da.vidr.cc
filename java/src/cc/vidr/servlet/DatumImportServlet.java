/*
 * Copyright (C) 2010  David Roberts <d@vidr.cc>
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

package cc.vidr.servlet;

import java.io.IOException;
import java.io.InputStream;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.antlr.runtime.RecognitionException;
import org.apache.commons.fileupload.FileItemIterator;
import org.apache.commons.fileupload.FileItemStream;
import org.apache.commons.fileupload.FileUploadException;
import org.apache.commons.fileupload.servlet.ServletFileUpload;

import cc.vidr.datum.Program;
import cc.vidr.datum.Server;
import cc.vidr.datum.UnsafeException;

@SuppressWarnings("serial")
public class DatumImportServlet extends HttpServlet {
    public void doGet(HttpServletRequest req, HttpServletResponse resp)
    throws IOException {
        resp.getWriter().println(
                "<form action=\"\" method=\"post\" " +
                "enctype=\"multipart/form-data\">");
        for(int i = 0; i < 10; i++)
            resp.getWriter().println(
                    "<input type=\"file\" name=\"file" + i + "\" /><br />");
        resp.getWriter().println("<input type=\"submit\" /></form>");
    }

    public void doPost(HttpServletRequest req, HttpServletResponse resp)
    throws IOException, ServletException {
        try {
            ServletFileUpload upload = new ServletFileUpload();
            FileItemIterator iterator = upload.getItemIterator(req);
            while(iterator.hasNext()) {
                FileItemStream item = iterator.next();
                if(item.isFormField())
                    continue;
                String filename = item.getName();
                if(filename.isEmpty())
                    continue;
                InputStream stream = item.openStream();
                resp.getWriter().println("<p>");
                try {
                    resp.getWriter().println("Loading '" + filename + "'... ");
                    Program program = new Program(stream);
                    program.parse();
                    program.assertFacts(Server.factDatabase);
                    program.assertRules(Server.ruleDatabase);
                    resp.getWriter().println("OK");
                } catch(RecognitionException e) {
                    resp.getWriter().println(
                            "Malformed input: " + e.getMessage());
                } catch(UnsafeException e) {
                    resp.getWriter().println(
                            "Unsafe rule or non-ground fact encountered: "
                            + e.getMessage());
                } catch(IOException e) {
                    resp.getWriter().println(
                            "Error opening file: " + e.getMessage());
                }
                resp.getWriter().println("</p>");
            }
        } catch(FileUploadException e) {
            throw new ServletException(e);
        }
        doGet(req, resp);
    }
}
