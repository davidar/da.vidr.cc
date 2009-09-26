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

from google.appengine.ext import db
from django.contrib.sitemaps import Sitemap
from django import forms

class Page(db.Model):
    title = db.StringProperty()
    slug = db.StringProperty()
    parent_page = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    mod_date = db.DateTimeProperty(auto_now=True)
    description = db.StringProperty()
    head = db.TextProperty()
    content = db.TextProperty()
    content_html = db.TextProperty()
    
    def get_absolute_url(self):
        return "/%s/" % self.path
    
    @property
    def root(self):
        if not self.parent_page: return self.slug
        slash = self.parent_page.find('/')
        if slash == -1: return self.parent_page
        else:           return self.parent_page[:slash]
    
    @property
    def path(self):
        if self.parent_page: return "%s/%s" % (self.parent_page, self.slug)
        else:                return self.slug

class PageForm(forms.ModelForm):
    head = forms.CharField(widget=forms.Textarea(attrs={'rows':'6'}),
                           required=False)
    class Meta:
        model = Page
        exclude = ['date', 'mod_date', 'content_html']

class PagesSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Page.all()

    def lastmod(self, obj):
        return obj.mod_date

