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

import java.lang.reflect.InvocationTargetException;

public final class DynamicClassLoader extends ClassLoader {
    private static DynamicClassLoader classLoader = new DynamicClassLoader();
    
    private DynamicClassLoader() {}
    
    public static Class<?> fromBytes(byte[] bytes) {
        return classLoader.defineClass(null, bytes, 0, bytes.length);
    }
    
    public static void invokeMainMethod(Class<?> cls, String[] args)
    throws SecurityException, NoSuchMethodException, IllegalArgumentException,
    IllegalAccessException, InvocationTargetException {
        cls.getMethod("main", String[].class).invoke(null, (Object)args);
    }
    
    public static void invokeMainMethod(Class<?> cls)
    throws SecurityException, NoSuchMethodException, IllegalArgumentException,
    IllegalAccessException, InvocationTargetException {
        invokeMainMethod(cls, new String[0]);
    }
}
