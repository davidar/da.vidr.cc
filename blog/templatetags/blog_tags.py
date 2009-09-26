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

import logging

from django import template
from django.contrib.sites.models import Site

from blog.models import Post, Category

register = template.Library()

def inflate_category(posts):
    slug_map = Category.slug_map()
    for post in posts:
        for i,slug in enumerate(post.category):
            if slug in slug_map:
                post.category[i] = slug_map[slug]
            else:
                logging.error("post '%s' refers to non-existent "
                              "category '%s'", post.slug, slug)
                post.category[i] = Category(title=slug, slug=slug, path=slug)

@register.inclusion_tag('blog/sidebar/recent_posts.html')
def recent_posts():
    posts = Post.all().order('-date').fetch(10)
    return {'posts': posts}

@register.inclusion_tag('blog/sidebar/categories.html')
def categories():
    categories = Category.hierarchy()
    return {'categories': categories}

@register.inclusion_tag('blog/post.html')
def blog_post(post):
    if post.category and type(post.category[0]) is not Category:
        inflate_category([post])
    return {'post': post, 'site': Site.objects.get_current()}

@register.inclusion_tag('blog/post_index.html')
def blog_post_index(posts):
    inflate_category(posts)
    return {'posts': posts}

@register.inclusion_tag('blog/pagination.html')
def pagination(posts, path='/'):
    return {'posts': posts, 'path': path}

