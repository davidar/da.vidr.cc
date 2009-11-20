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

import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.apache.commons.jci.compilers.CompilationResult;
import org.apache.commons.jci.compilers.EclipseJavaCompiler;
import org.apache.commons.jci.compilers.EclipseJavaCompilerSettings;
import org.apache.commons.jci.compilers.JavaCompiler;
import org.apache.commons.jci.problems.CompilationProblem;
import org.apache.commons.jci.readers.ResourceReader;
import org.apache.commons.jci.stores.ResourceStore;

public class JavaSourceCompiler {
    private JavaCompiler compiler;
    private CompilationResult result;
    private String fileName;
    private String source;
    private Map<String, byte[]> classes;
    
    private JavaSourceCompiler() {
        EclipseJavaCompilerSettings compilerSettings =
            new EclipseJavaCompilerSettings();
        compilerSettings.setTargetVersion("1.6");
        compilerSettings.setSourceVersion("1.6");
        compiler = new EclipseJavaCompiler(compilerSettings);
        classes = new HashMap<String, byte[]>();
    }
    
    public JavaSourceCompiler(String fileName, String source) {
        this();
        this.fileName = fileName;
        this.source = source;
    }
    
    public void compile() {
        result = compiler.compile(
                new String[] {fileName},
                new ResourceReader() {
                    public byte[] getBytes(String resourceName) {
                        if(resourceName == fileName)
                            return source.getBytes();
                        else
                            return null;
                    }
                    public boolean isAvailable(String resourceName) {
                        return resourceName == fileName;
                    }
                },
                new ResourceStore() {
                    public byte[] read(String resourceName) {
                        return classes.get(resourceName);
                    }
                    public void remove(String resourceName) {
                        classes.remove(resourceName);
                    }
                    public void write(String resourceName, byte[] data) {
                        classes.put(resourceName, data);
                    }
                });
    }
    
    public List<CompilationProblem> getErrors() {
        return Arrays.asList(result.getErrors());
    }
    
    public int getNumErrors() {
        return result.getErrors().length;
    }
    
    public boolean successful() {
        return getNumErrors() == 0;
    }
    
    public List<CompilationProblem> getWarnings() {
        return Arrays.asList(result.getWarnings());
    }
    
    public int getNumWarnings() {
        return result.getWarnings().length;
    }
    
    public Set<String> getClassNames() {
        Set<String> classNames = new HashSet<String>();
        for(String className : classes.keySet())
            classNames.add(className.substring(
                    0, className.lastIndexOf(".class")));
        return classNames;
    }
    
    public byte[] getClassData(String className) {
        return classes.get(className + ".class");
    }
}
