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

from google.appengine.ext import db
from google.appengine.api import memcache
from django.contrib.sitemaps import Sitemap
from django.contrib.syndication.feeds import Feed
from django import forms

class Post(db.Model):
    title = db.StringProperty()
    slug = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    mod_date = db.DateTimeProperty(auto_now=True)
    content = db.TextProperty()
    content_html = db.TextProperty()
    
    def get_absolute_url(self):
        return self.date.strftime("/%Y/%m/%d/") + self.slug + '/'

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['slug', 'date', 'mod_date', 'content_html']

class BlogSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Post.all()

    def lastmod(self, obj):
        return obj.mod_date

class BlogFeed(Feed):
    title = "da.vidr.cc"
    link = "/"
    #description = ""

    def items(self):
        return Post.all().order('-date').fetch(10)

