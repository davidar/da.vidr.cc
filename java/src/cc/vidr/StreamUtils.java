/*
 * Copyright (C) 2009-2010  David A Roberts <d@vidr.cc>
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

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

public final class StreamUtils {
    private static final int BUF_SIZE = 8192;

    private StreamUtils() {}
    
    public static void copyStream(InputStream in, OutputStream out)
    throws IOException {
        byte[] buf = new byte[BUF_SIZE];
        int len;
        try {
            while((len = in.read(buf)) > 0)
                out.write(buf, 0, len);
        } finally {
            in.close();
        }
    }
}
