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

from django.template.loader import render_to_string

from util import humanize_list

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

