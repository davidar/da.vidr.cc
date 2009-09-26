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

from datetime import datetime
import os
from cStringIO import StringIO
import zipfile
import logging

import simplejson as json
from xml.etree import ElementTree
import html2text

from django import http, shortcuts, forms

from appenginepatcher import appid
from aecmd import PROJECT_DIR, COMMON_DIR

from util import admin, md_convert, flush_cache
from blog.models import Post, Category
from pages.models import Page

datetime_format = "%Y-%m-%d %H:%M:%S"

def export_posts():
    return [{
        'title': post.title,
        'slug': post.slug,
        'date': post.date.strftime(datetime_format),
        'mod_date': post.mod_date.strftime(datetime_format),
        'category': post.category,
        'content': post.content,
        } for post in Post.all()]

def export_categories():
    return [{
        'title': cat.title,
        'slug': cat.slug,
        'ancestors': cat.ancestors,
        } for cat in Category.all()]

def export_pages():
    return [{
        'title': page.title,
        'slug': page.slug,
        'parent_page': page.parent_page,
        'date': page.date.strftime(datetime_format),
        'mod_date': page.mod_date.strftime(datetime_format),
        'description': page.description,
        'head': page.head,
        'content': page.content,
        } for page in Page.all()]

def import_posts(posts):
    Post.mod_date.auto_now = False # don't set mod_date to now
    for d in posts:
        post = Post()
        post.title = d['title']
        post.slug = d['slug']
        post.date = datetime.strptime(d['date'], datetime_format)
        post.mod_date = datetime.strptime(d['mod_date'], datetime_format)
        post.category = d['category']
        post.content = d['content']
        post.content_html = md_convert(post.content)
        post.put()
    Post.mod_date.auto_now = True

def import_categories(cats):
    for d in cats:
        cat = Category()
        cat.title = d['title']
        cat.slug = d['slug']
        cat.ancestors = d['ancestors']
        cat.path = '/'.join(cat.ancestors + [cat.slug])
        cat.put()

def import_pages(pages):
    Page.mod_date.auto_now = False # don't set mod_date to now
    for d in pages:
        page = Page()
        page.title = d['title']
        page.slug = d['slug']
        page.parent_page = d['parent_page']
        page.date = datetime.strptime(d['date'], datetime_format)
        page.mod_date = datetime.strptime(d['mod_date'], datetime_format)
        page.description = d['description']
        page.head = d['head']
        page.content = d['content']
        page.content_html = md_convert(page.content)
        page.put()
    Page.mod_date.auto_now = True

@admin
def export_json(request):
    response = http.HttpResponse(mimetype='text/plain')
    json.dump({'posts': export_posts(),
               'categories': export_categories(),
               'pages': export_pages()},
              response, indent=True)
    return response

@admin
def export_source_zip(request, full=False):
    f = StringIO()
    z = zipfile.ZipFile(f, 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(PROJECT_DIR):
        if not full and dirpath.startswith(COMMON_DIR):
            continue
        for filename in filenames:
            fname = os.path.join(dirpath, filename)
            aname = os.path.join(appid, fname[len(PROJECT_DIR)+1:])
            try:
                z.write(fname, aname)
            except:
                logging.error("unable to write '%s' to zip file", fname)
    z.close()
    f.seek(0)
    return http.HttpResponse(f, mimetype='application/x-zip-compressed')

class UploadFileForm(forms.Form):
    # make sure that the form tag has enctype="multipart/form-data"
    file = forms.FileField()

@admin
def import_json(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            d = json.load(request.FILES['file'])
            import_posts(d['posts'])
            import_categories(d['categories'])
            import_pages(d['pages'])
            flush_cache()
            return http.HttpResponseRedirect('/')
    else:
        form = UploadFileForm()
    return shortcuts.render_to_response('backup/import.html', {'form': form})

def process_wxr(f):
    NS_WP = 'http://wordpress.org/export/1.0/'
    NS_C = 'http://purl.org/rss/1.0/modules/content/'
    html2text.BODY_WIDTH = 0 # disable word wrap
    
    wxr = ElementTree.parse(f).getroot()
    posts = []
    pages = []
    
    cats = {}
    
    for item in wxr.findall('channel/item'):
        p = {
            'title': item.find('title').text,
            'slug': item.find('{%s}post_name' % NS_WP).text,
            'date': item.find('{%s}post_date_gmt' % NS_WP).text,
            'mod_date': datetime.utcnow().strftime(datetime_format),
            'content': html2text.html2text(
                item.find('{%s}encoded' % NS_C).text),
        }
        
        ptype = item.find('{%s}post_type' % NS_WP).text
        if ptype == 'post':
            p['category'] = []
            for cat in item.findall('category'):
                cat_slug = cat.get('nicename')
                if cat_slug is None: continue
                p['category'].append(cat_slug)
                cats[cat_slug] = cat.text
            posts.append(p)
        elif ptype == 'page':
            p['parent_page'] = '/'.join(
                item.find('link').text.split('/')[3:-2]) or None
            p['description'] = None
            p['head'] = None
            pages.append(p)
    
    categories = [{'title': title, 'slug': slug, 'ancestors': []}
                  for slug, title in cats.iteritems()]
    
    return {'posts': posts, 'pages': pages, 'categories': categories}

@admin
def import_wxr(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                d = process_wxr(request.FILES['file'])
            except Exception, e:
                msg = "Error parsing WXR file: %s\n" % e
                msg += "Make sure content containing special characters is " \
                       "wrapped in <![CDATA[ ... ]]> (this is often an " \
                       "issue with the content of <wp:meta_value> tags)"
                return shortcuts.render_to_response('backup/import.html',
                    {'form': form, 'message': msg})
            import_posts(d['posts'])
            import_categories(d['categories'])
            import_pages(d['pages'])
            flush_cache()
            return http.HttpResponseRedirect('/')
    else:
        form = UploadFileForm()
    return shortcuts.render_to_response('backup/import.html', {'form': form})

