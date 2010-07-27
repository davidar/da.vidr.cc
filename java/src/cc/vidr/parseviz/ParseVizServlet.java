/*
 * Copyright (C) 2010  David A Roberts <d@vidr.cc>
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

package cc.vidr.parseviz;

import java.io.IOException;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import edu.stanford.nlp.trees.Tree;

@SuppressWarnings("serial")
public class ParseVizServlet extends HttpServlet {
    public void doGet(HttpServletRequest req, HttpServletResponse resp)
    throws IOException, ServletException {
        String type = req.getParameter("type");
        String format = req.getParameter("format");
        String s = req.getParameter("q");

        if(s == null || type == null || format == null) {
            req.getRequestDispatcher("/jsp/parseviz.jsp").forward(req, resp);

        } else if(format.equals("png") || format.equals("dot")) {
            Tree tree = ParseViz.parse(s);
            String dot;
            if(type.equals("tree"))
                dot = ParseViz.printTreeDot(tree);
            else if(type.equals("deps"))
                dot = ParseViz.printDependenciesDot(tree);
            else
                dot = "graph{\"Unrecognised type\"}";

            if(format.equals("png")) {
                resp.setContentType("image/png");
                ParseViz.renderDot(s, dot, resp.getOutputStream());
            } else {
                resp.setContentType("text/plain");
                resp.getWriter().println(dot);
            }

        } else if(type.equals("tree") &&
                (format.equals("penn") || format.equals("text"))) {
            resp.setContentType("text/plain");
            Tree tree = ParseViz.parse(s);
            ParseViz.printTree(tree, resp.getWriter());

        } else if(type.equals("deps") && format.equals("text")) {
            resp.setContentType("text/plain");
            Tree tree = ParseViz.parse(s);
            ParseViz.printDependencies(tree, resp.getWriter());

        } else {
            resp.sendError(resp.SC_NOT_FOUND);
        }
    }
}
