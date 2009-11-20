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

package cc.vidr;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.io.Writer;

public final class StreamUtils {
    private StreamUtils() {}
    
    public static void pipe(PrintWriter dest, InputStream src)
    throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(src));
        String line;
        while((line = reader.readLine()) != null)
            dest.println(line);
    }
    
    public static void pipe(OutputStream dest, InputStream src)
    throws IOException {
        pipe(new PrintWriter(dest), src);
    }
    
    public static void pipe(Writer dest, InputStream src)
    throws IOException {
        pipe(new PrintWriter(dest), src);
    }
    
    public static String readAll(InputStream src)
    throws IOException {
        StringWriter writer = new StringWriter();
        pipe(writer, src);
        return writer.toString();
    }
}
