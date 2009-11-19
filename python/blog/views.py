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

from datetime import datetime, timedelta
import pprint
from textwrap import wrap

import markdown

from django import http, shortcuts
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from google.appengine.ext import db

from cc.vidr.util import admin, slugify, md_convert, split_url, flush_cache
from blog.models import Post, PostForm, Category, CategoryForm
from blog.ping import ping_all_search_engines, pingomatic

def get_post(y, m, d, slug):
    y,m,d = map(int, (y,m,d))
    date = datetime(y,m,d)
    post = Post.all() \
               .filter('slug', slug) \
               .filter('date >=', date) \
               .filter('date <', date + timedelta(1)) \
               .get()
    if post is None: raise http.Http404
    return post

def get_category(url):
    cat = Category.all().filter('path', url).get()
    if cat is None: raise http.Http404
    return cat

def paginate(objects, page):
    page = int(page)
    paginator = Paginator(objects, 10)
    try:
        return paginator.page(page)
    except (EmptyPage, InvalidPage):
        raise http.Http404

def index(request, page=1):
    posts = paginate(Post.all().order('-date'), page)
    return shortcuts.render_to_response('blog/index.html', {'posts': posts})

def view(request, y, m, d, slug):
    post = get_post(y, m, d, slug)
    return shortcuts.render_to_response('blog/view.html', {'post': post})

def view_category(request, url, page=1):
    cat = get_category(url)
    subcats = Category.all().filter('ancestors', cat.slug)
    posts = Post.all().filter('category', cat.slug).order('-date')
    posts_paginated = paginate(posts, page)
    return shortcuts.render_to_response('blog/category/view.html',
        {'category': cat, 'subcategories': subcats, 'posts': posts_paginated})

@admin
def edit(request, y=None, m=None, d=None, slug=None):
    data = request.POST or None
    if slug: instance = get_post(y, m, d, slug)
    else:    instance = None
    form = PostForm(data=data, instance=instance)
    valid_submission = request.POST and form.is_valid()
    
    if valid_submission:
        post = form.save(commit=False)
        post.content_html = md_convert(post.content)
        if not slug:
            # don't replace current slug
            post.slug = slugify(post.title)
    else:
        post = None

    if not valid_submission or request.POST['submit'] == 'Preview':
        return shortcuts.render_to_response(
            'blog/edit.html', {'form': form, 'preview': post, 'slug': slug,
                               'y': y, 'm': m, 'd': d})
    else:
        post.put()
        flush_cache()
        return http.HttpResponseRedirect(post.get_absolute_url())

def category_slug_changed(from_cat, to_cat):
    posts = Post.all().filter('category', from_cat)
    for post in posts:
        i = post.category.index(from_cat)
        post.category[i] = to_cat
        post.put()
    
    cats = Category.all().filter('ancestors', from_cat)
    for cat in cats:
        i = cat.ancestors.index(from_cat)
        cat.ancestors[i] = to_cat
        cat.path = '/'.join(cat.ancestors + [cat.slug])
        cat.put()

@admin
def edit_category(request, url=None):
    data = request.POST or None
    if url: instance = get_category(url)
    else:   instance = None
    orig_slug = instance.slug
    form = CategoryForm(data=data, instance=instance)
    valid_submission = request.POST and form.is_valid()
    if not valid_submission:
        return shortcuts.render_to_response(
            'blog/category/edit.html', {'form': form})
    else:
        cat = form.save(commit=False)
        cat.path = '/'.join(cat.ancestors + [cat.slug])
        cat.put()
        if orig_slug != cat.slug:
            category_slug_changed(orig_slug, cat.slug)
        flush_cache()
        return http.HttpResponseRedirect(cat.get_absolute_url())

@admin
def ping(request):
    output = {}
    for site, out in ping_all_search_engines():
        output[site] = '\n'.join(wrap(out, 80))
    output['Pingomatic'] = pprint.pformat(pingomatic(), 4)
    return shortcuts.render_to_response('blog/ping/view.html',
        {'output': output})

