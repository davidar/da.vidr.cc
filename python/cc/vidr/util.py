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
import email
import time
import mimetypes
import os
import zipfile
import logging

from markdown import markdown

from django import http
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.core.urlresolvers import get_callable

from google.appengine.api import users, memcache

from aecmd import PROJECT_DIR
from appenginepatcher import on_production_server
from ragendja.dbutils import db_create
from ragendja.sites.dynamicsite import SITE_ID

def admin(func):
    def check_admin(request, *args, **kwargs):
        # make sure current user is an admin
        if users.get_current_user() is None:
            url = users.create_login_url(request.path)
            return http.HttpResponseRedirect(url)
        elif not users.is_current_user_admin():
            raise http.Http404
        else:
            return func(request, *args, **kwargs)
    return check_admin

def slugify(string):
    string = re.sub('[^\w\s-]', '', string)
    string = re.sub('[\s-]+', '-', string)
    string = string.strip('_- ').lower()
    return string

def md_convert(text):
    if text is None: return None
    return markdown(text, ['codehilite', 'headerid'])

def split_url(url):
    slash = url.rfind('/')
    if slash == -1:
        parent = None
        slug = url
    else:
        parent = url[:slash]
        slug = url[slash+1:]
    return parent, slug

def flush_cache():
    memcache.flush_all()

def dummy_view(request, output='', mimetype=None):
    return http.HttpResponse(output, mimetype=mimetype)

zipfile_cache = {}
def zipserve(request, name, zipfilename, prefix=''):
    # adapted from google.appengine.ext.zipserve
    
    zipfilename += '.zip'
    if prefix: name = prefix + '/' + name
    
    if zipfilename in zipfile_cache:
        zipfile_object = zipfile_cache[zipfilename]
    else:
        try:
            zipfile_object = zipfile.ZipFile(
                os.path.join(PROJECT_DIR, 'common', 'zip-media', zipfilename))
        except (IOError, RuntimeError), e:
            logging.error("can't open zipfile '%s': %s", zipfilename, e)
            zipfile_object = None
        zipfile_cache[zipfilename] = zipfile_object
    
    if zipfile_object is None: raise http.Http404
    
    try:
        data = zipfile_object.read(name)
    except (KeyError, RuntimeError):
        raise http.Http404
    
    content_type, encoding = mimetypes.guess_type(name)
    response = http.HttpResponse(data, mimetype=content_type)
    
    # set caching headers
    max_age = 600
    expire_date = email.utils.formatdate(time.time() + max_age, usegmt=True)
    response['Expires'] = expire_date
    response['Cache-Control'] = "public, max-age=%d" % max_age
    
    return response

def humanize_list(l, conj):
    if len(l) < 1:
        return ''
    elif len(l) == 1:
        return l[0]
    elif len(l) == 2:
        return "%s %s %s" % (l[0], conj, l[1])
    else:
        return "%s, %s %s" % (', '.join(l[:-1]), conj, l[-1])

class OverrideSiteIDMiddleware(object):
    def process_request(self, request):
        if on_production_server: return
        
        domain = 'da.vidr.cc'
        cache_key = 'Site:domain:%s' % domain
        site = Site.all().filter('domain', domain).get()
        if not site:
            site = db_create(Site, domain=domain, name=domain)
            site.put()
        SITE_ID.value = str(site.key())
        cache.set(cache_key, SITE_ID.value, 5*60)

def call_fn(fn, *args):
    return get_callable(fn)(*args)

