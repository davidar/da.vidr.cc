# Copyright (C) 2009-2010  David Roberts <d@vidr.cc>
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

from blog.models import Post

register = template.Library()

@register.inclusion_tag('blog/sidebar/recent_posts.html')
def recent_posts():
    posts = Post.all().order('-date').fetch(10)
    return {'posts': posts}

@register.inclusion_tag('blog/post.html')
def blog_post(post):
    return {'post': post, 'site': Site.objects.get_current()}

@register.inclusion_tag('blog/post_index.html')
def blog_post_index(posts):
    return {'posts': posts}

@register.inclusion_tag('blog/pagination.html')
def pagination(posts, path='/'):
    return {'posts': posts, 'path': path}

