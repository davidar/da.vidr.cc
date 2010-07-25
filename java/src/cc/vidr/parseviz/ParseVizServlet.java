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

import java.io.InputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.io.Reader;
import java.io.StringReader;

import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLEncoder;

import java.util.HashMap;
import java.util.List;
import java.util.logging.Logger;
import java.util.Map;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import edu.stanford.nlp.ling.CategoryWordTagFactory;
import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.objectbank.TokenizerFactory;
import edu.stanford.nlp.parser.lexparser.Debinarizer;
import edu.stanford.nlp.parser.lexparser.LexicalizedParser;
import edu.stanford.nlp.parser.lexparser.Options;
import edu.stanford.nlp.parser.lexparser.ParserData;
import edu.stanford.nlp.process.DocumentPreprocessor;
import edu.stanford.nlp.trees.GrammaticalRelation;
import edu.stanford.nlp.trees.GrammaticalStructure;
import edu.stanford.nlp.trees.GrammaticalStructureFactory;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.trees.TreebankLanguagePack;
import edu.stanford.nlp.trees.TreeGraphNode;
import edu.stanford.nlp.trees.TreePrint;
import edu.stanford.nlp.trees.TypedDependency;
import edu.stanford.nlp.util.Timing;

import cc.vidr.StreamUtils;

@SuppressWarnings("serial")
public class ParseVizServlet extends HttpServlet {
    private static final Logger log =
        Logger.getLogger(ParseVizServlet.class.getName());
    private static final Map<String, Tree> treeCache =
        new HashMap<String, Tree>();

    private static final ParserData parserData;
    private static final Options options;
    private static final TreebankLanguagePack tlp;
    private static final TokenizerFactory<? extends HasWord> tokenizerFactory;
    private static final Debinarizer debinarizer;
    private static final GrammaticalStructureFactory gsf;

    static {
        ParserData pd = null;
        try {
            Timing timing = new Timing();
            InputStream ser = ParseVizServlet.class.getResourceAsStream(
                    "englishPCFG.ser");
            ObjectInputStream ois = new ObjectInputStream(ser);
            pd = (ParserData) ois.readObject();
            ois.close();
            log.info("Loaded parser data in " +
                    timing.toSecondsString() + " seconds");
        } catch(Exception e) {
            log.severe("Error reading parser data: " + e);
        }

        parserData = pd;
        options = parserData.pt;
        tlp = options.tlpParams.treebankLanguagePack();
        tokenizerFactory = tlp.getTokenizerFactory();
        debinarizer = new Debinarizer(
                options.forceCNF, new CategoryWordTagFactory());
        gsf = tlp.grammaticalStructureFactory(
                tlp.punctuationWordRejectFilter());
    }

    private static Tree parse(String s) {
        if(treeCache.containsKey(s))
            return treeCache.get(s);
        Reader r = new StringReader(s);
        List<? extends HasWord> sentence =
            tokenizerFactory.getTokenizer(r).tokenize();
        LexicalizedParser parser = new LexicalizedParser(parserData);
        parser.parse(sentence);
        Tree tree = parser.getBestParse();
        tree = debinarizer.transformTree(tree);
        treeCache.put(s, tree);
        return tree;
    }

    private static List<TypedDependency> typedDependencies(Tree tree) {
        GrammaticalStructure gs = gsf.newGrammaticalStructure(tree);
        return gs.typedDependenciesCCprocessed();
    }

    private static void printTree(Tree tree, PrintWriter out) {
        printTree(tree, out, "penn");
    }

    private static void printTree(Tree tree, PrintWriter out, String format) {
        TreePrint treePrint = new TreePrint(
                format, "", tlp, options.tlpParams.headFinder());
        treePrint.printTree(tree, out);
    }

    private static String printTreeDot(Tree tree) {
        StringBuilder sb = new StringBuilder();
        printTreeDot(tree, sb);
        return sb.toString();
    }

    private static void printTreeDot(Tree tree, StringBuilder sb) {
        sb.append("graph{\nnode[shape=none];\n");
        printTreeDot(tree, sb, tree);
        sb.append("{rank=same;\n");
        for(Tree leaf : tree.getLeaves())
            sb.append("n").append(leaf.nodeNumber(tree)).append(";\n");
        sb.append("};\n");
        sb.append("}\n");
    }

    private static void printTreeDot(Tree tree, StringBuilder sb, Tree root) {
        sb.append("n").append(tree.nodeNumber(root))
            .append("[label=\"").append(tree.label()).append("\"];\n");
        for(Tree child : tree.children()) {
            sb.append("n").append(tree.nodeNumber(root))
                .append("--n").append(child.nodeNumber(root)).append(";\n");
            printTreeDot(child, sb, root);
        }
    }

    private static String printDependenciesDot(Tree tree) {
        StringBuilder sb = new StringBuilder();
        printDependenciesDot(tree, sb);
        return sb.toString();
    }

    private static void printDependenciesDot(Tree tree, StringBuilder sb) {
        sb.append("digraph{\n");
        for(TypedDependency td : typedDependencies(tree)) {
            GrammaticalRelation reln = td.reln();
            TreeGraphNode gov = td.gov();
            TreeGraphNode dep = td.dep();
            sb.append("n").append(gov.index())
                .append("[label=\"").append(gov).append("\"];\n")
                .append("n").append(dep.index())
                .append("[label=\"").append(dep).append("\"];\n")
                .append("n").append(gov.index())
                .append("->n").append(dep.index())
                .append("[label=\"").append(reln).append("\"];\n");
        }
        sb.append("}\n");
    }

    private static void renderDot(String id, String dot, OutputStream out)
    throws IOException {
        URL url = new URL("http://chart.apis.google.com/chart?chid=" +
                URLEncoder.encode(id, "UTF-8"));
        log.info("Fetching " + url);
        HttpURLConnection connection =
            (HttpURLConnection) url.openConnection();
        connection.setDoOutput(true);
        connection.setRequestMethod("POST");

        OutputStreamWriter writer = new OutputStreamWriter(
                connection.getOutputStream());
        writer.write("cht=gv:dot&chl=" + URLEncoder.encode(dot, "UTF-8"));
        writer.close();

        if (connection.getResponseCode() == HttpURLConnection.HTTP_OK)
            StreamUtils.copyStream(connection.getInputStream(), out);
        else
            throw new IOException("Charts API returned status code " +
                    connection.getResponseCode());
    }

    public void doGet(HttpServletRequest req, HttpServletResponse resp)
    throws IOException, ServletException {
        String type = req.getParameter("type");
        String format = req.getParameter("format");
        String s = req.getParameter("q");

        if(s == null) {
            resp.getWriter().println(
                    "<form action=\"\" method=\"get\">" +
                    "<input type=\"text\" name=\"q\" size=\"80\" " +
                    "value=\"The quick brown fox jumps over the lazy dog.\" " +
                    "/>" +
                    "<input type=\"submit\" />" +
                    "</form>");
            return;
        }

        Tree tree = parse(s);
        if(type == null || format == null) {
            PrintWriter out = resp.getWriter();

            out.println("<pre>");
            printTree(tree, out);
            out.println("</pre>");
            out.println("<img src=\"?type=tree&amp;format=png&amp;q=" +  
                    URLEncoder.encode(s, "UTF-8") + "\" " +
                    "style=\"max-width:100%\" />");

            out.println("<pre>");
            for(TypedDependency td : typedDependencies(tree))
                out.println(td);
            out.println("</pre>");
            out.println("<img src=\"?type=deps&amp;format=png&amp;q=" +  
                    URLEncoder.encode(s, "UTF-8") + "\" " +
                    "style=\"max-width:100%\" />");

        } else if(format.equals("png") || format.equals("dot")) {
            String dot;
            if(type.equals("tree"))
                dot = printTreeDot(tree);
            else if(type.equals("deps"))
                dot = printDependenciesDot(tree);
            else
                dot = "graph{\"Unrecognised type\"}";

            if(format.equals("png")) {
                resp.setContentType("image/png");
                renderDot(s, dot, resp.getOutputStream());
            } else {
                resp.setContentType("text/plain");
                resp.getWriter().println(dot);
            }

        } else if(type.equals("tree") &&
                (format.equals("penn") || format.equals("text"))) {
            resp.setContentType("text/plain");
            printTree(tree, resp.getWriter());

        } else if(type.equals("deps") && format.equals("text")) {
            resp.setContentType("text/plain");
            for(TypedDependency td : typedDependencies(tree))
                resp.getWriter().println(td);

        } else {
            resp.sendError(resp.SC_NOT_FOUND);
        }
    }
}
