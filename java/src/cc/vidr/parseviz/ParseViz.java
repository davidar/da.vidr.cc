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
import java.io.Writer;

import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLEncoder;

import java.util.HashMap;
import java.util.List;
import java.util.logging.Logger;
import java.util.Map;

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
public class ParseViz {
    private static final Logger log =
        Logger.getLogger(ParseViz.class.getName());
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

    public static Tree parse(String s) {
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

    public static List<TypedDependency> typedDependencies(Tree tree) {
        GrammaticalStructure gs = gsf.newGrammaticalStructure(tree);
        return gs.typedDependenciesCCprocessed();
    }

    public static void printTree(Tree tree, Writer out) {
        printTree(tree, new PrintWriter(out));
    }

    public static void printTree(Tree tree, PrintWriter out) {
        printTree(tree, out, "penn");
    }

    public static void printTree(Tree tree, PrintWriter out, String format) {
        TreePrint treePrint = new TreePrint(
                format, "", tlp, options.tlpParams.headFinder());
        treePrint.printTree(tree, out);
    }

    public static String printTreeDot(Tree tree) {
        StringBuilder sb = new StringBuilder();
        printTreeDot(tree, sb);
        return sb.toString();
    }

    public static void printTreeDot(Tree tree, StringBuilder sb) {
        sb.append("graph{\nnode[shape=none];\n");
        printTreeDot(tree, sb, tree);
        sb.append("{rank=same;\n");
        for(Tree leaf : tree.getLeaves())
            sb.append("n").append(leaf.nodeNumber(tree)).append(";\n");
        sb.append("};\n");
        sb.append("}\n");
    }

    public static void printTreeDot(Tree tree, StringBuilder sb, Tree root) {
        sb.append("n").append(tree.nodeNumber(root))
            .append("[label=\"").append(tree.label()).append("\"];\n");
        for(Tree child : tree.children()) {
            sb.append("n").append(tree.nodeNumber(root))
                .append("--n").append(child.nodeNumber(root)).append(";\n");
            printTreeDot(child, sb, root);
        }
    }

    public static void printDependencies(Tree tree, Writer out) {
        printDependencies(tree, new PrintWriter(out));
    }

    public static void printDependencies(Tree tree, PrintWriter out) {
        for(TypedDependency td : ParseViz.typedDependencies(tree))
            out.println(td);
    }

    public static String printDependenciesDot(Tree tree) {
        StringBuilder sb = new StringBuilder();
        printDependenciesDot(tree, sb);
        return sb.toString();
    }

    public static void printDependenciesDot(Tree tree, StringBuilder sb) {
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

    public static void renderDot(String id, String dot, OutputStream out)
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
}
