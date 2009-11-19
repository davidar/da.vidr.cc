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
    category = db.StringListProperty()
    content = db.TextProperty()
    content_html = db.TextProperty()
    
    def get_absolute_url(self):
        return self.date.strftime("/%Y/%m/%d/") + self.slug + '/'

class PostForm(forms.ModelForm):
    category = forms.CharField(widget=forms.Textarea(attrs={'rows':'3'}),
                               required=False)
    
    class Meta:
        model = Post
        exclude = ['slug', 'date', 'mod_date', 'content_html']

# TODO: the category system is a bit of a mess, perhaps it should be replaced
#       by a simple tagging system
class Category(db.Model):
    title = db.StringProperty()
    slug = db.StringProperty()
    ancestors = db.StringListProperty()
    path = db.StringProperty()
    
    def get_absolute_url(self):
        return "/category/%s/" % self.path
    
    @classmethod
    def slug_map(cls):
        slug_map = memcache.get('category_slugmap')
        if slug_map is None:
            cats = cls.all()
            slug_map = dict([(cat.slug, cat) for cat in cats])
            memcache.add('category_slugmap', slug_map)
        return slug_map
    
    @classmethod
    def hierarchy(cls):
        slug_map = cls.slug_map()
        for cat in slug_map.itervalues():
            cat.subcategories = []
            cat.num_posts = 0
        
        for post in Post.all():
            for cat_slug in post.category:
                if cat_slug in slug_map:
                    slug_map[cat_slug].num_posts += 1
                else:
                    logging.error("post '%s' refers to non-existent "
                        "category '%s'", post.slug, cat_slug)
        
        categories = []
        cats = sorted(slug_map.itervalues(),
                      lambda x,y: cmp(x.title.lower(), y.title.lower()))
        for cat in cats:
            if len(cat.ancestors) == 0:
                categories.append(cat)
            else:
                parent = cat.ancestors[-1]
                if parent in slug_map:
                    slug_map[parent].subcategories.append(cat)
                else:
                    logging.error("category '%s' refers to non-existent "
                        "parent category '%s'", cat.slug, parent)
        
        return categories

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ['path']

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

