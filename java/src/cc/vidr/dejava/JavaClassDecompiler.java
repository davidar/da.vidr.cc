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

import classfileanalyzer.Builder;
import classfileanalyzer.ClassFile;

public class JavaClassDecompiler {
    private ClassFile cls;
    private String asm;
    
    public JavaClassDecompiler(String className, byte[] classData) {
        cls = new ClassFile(className, classData);
    }
    
    public void decompile() throws ClassFormatError {
        cls.parse();
        Builder builder = new Builder();
        builder.buildHeader(
                cls.getMinorVersion(), 
                cls.getMajorVersion(), 
                cls.getConstantPool(),
                cls.getAccessFlags(), 
                cls.getThisClass(), 
                cls.getSuperClass(),
                cls.getInterfaces(),
                cls.getAttributes(),
                false);
        builder.buildFields(cls.getFields(), cls.getConstantPool());
        builder.buildMethods(cls.getMethods(), cls.getConstantPool());
        asm = builder.getAssemblerSourceText().toString();
    }
    
    public String getAssemblyCode() {
        return asm;
    }
}
