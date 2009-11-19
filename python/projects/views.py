# Copyright (C) 2009  David Roberts <d@vidr.cc>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from cc.vidr.jasminlexer import JasminLexer

import re
from urllib import urlopen, urlencode
from xml.etree.ElementTree import parse

from django.template.loader import render_to_string
from django.conf import settings

from cc.vidr.util import humanize_list

from pytextcat import classify

def pytextcat(request):
    if not request.POST or 'text' not in request.POST: return ''
    
    text = request.POST['text'].encode('utf-8')
    ranks = classify(text)
    ans = []
    
    for i,(rank,(lang,enc)) in enumerate(ranks):
        lang = lang.replace('_',' ').title()
        if enc: lang = "%s (%s)" % (lang,enc)
        
        if rank < 1.05: ans.append(lang)
        
        rank = int(100*rank) - 100
        ranks[i] = (lang,rank)
    
    ans = humanize_list(ans, 'or')
    
    return render_to_string('projects/pytextcat.html',
        {'text': text, 'ans': ans, 'ranks': ranks})

def dejava(request):
    if not request.POST or 'source' not in request.POST \
                        or 'classname' not in request.POST:
        return render_to_string('projects/dejava.html')
    
    source = request.POST['source'].strip()
    lines = source.split('\n')
    classname = request.POST['classname']
    
    root = parse(urlopen(
        "http://" + settings.JAVA_DOMAIN + "/projects/dejava/",
        urlencode({'source': source, 'classname': classname}))).getroot()
    errors = []
    for error in root.findall('errors/error'):
        errors.append(error.text.strip())
    warnings = []
    for warning in root.findall('warnings/warning'):
        warnings.append(warning.text.strip())
    classes = {}
    for cls in root.findall('classes/class'):
        classes[cls.get('classname')] = cls.text.strip()
    
    def inject_java_source(matchobj):
        line = int(matchobj.group(1))
        return ';' + lines[line-1] + '\n' + matchobj.group(0)
    for name,cls in classes.iteritems():
        classes[name] = re.sub(r'.*\.line\s+([0-9]+)', inject_java_source, cls)
    
    return render_to_string('projects/dejava.html',
        {'source': source, 'classname': classname,
         'errors': errors, 'warnings': warnings, 'classes': classes})

