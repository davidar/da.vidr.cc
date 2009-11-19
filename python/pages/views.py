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

import re

from django import http, shortcuts

from cc.vidr.util import admin, md_convert, split_url, flush_cache, call_fn
from pages.models import Page, PageForm

def get_page(url):
    parent, slug = split_url(url)
    page = Page.all() \
               .filter('slug', slug) \
               .filter('parent_page', parent) \
               .get()
    if page is None: raise http.Http404
    return page

def process_incudes(page, request):
    page.content_html = re.sub(
        r'<p>\$\(([a-zA-Z0-9.]*)\)</p>',
        lambda matchobj: call_fn(matchobj.group(1), request),
        page.content_html)

def view(request, url):
    page = get_page(url)
    if page.content:
        process_incudes(page, request)
        return shortcuts.render_to_response('pages/view.html', {'page': page})
    else:
        children = Page.all().filter('parent_page', page.path).order('title')
        return shortcuts.render_to_response(
            'pages/dir.html', {'page': page, 'children': children})

def view_source(request, url):
    page = get_page(url)
    if page.content:
        return shortcuts.render_to_response('pages/source.html',
                                            {'page': page})
    else:
        raise http.Http404

@admin
def edit(request, url=None):
    data = request.POST or None
    if url: instance = get_page(url)
    else:   instance = None
    form = PageForm(data=data, instance=instance)
    valid_submission = request.POST and form.is_valid()
    
    if valid_submission:
        page = form.save(commit=False)
        page.content_html = md_convert(page.content)
    else:
        page = None

    if not valid_submission or request.POST['submit'] == 'Preview':
        if page and page.content_html: process_incudes(page, request)
        return shortcuts.render_to_response(
            'pages/edit.html', {'form': form, 'preview': page})
    else:
        page.put()
        flush_cache()
        return http.HttpResponseRedirect(page.get_absolute_url())

