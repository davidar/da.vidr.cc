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

import urllib
import sys
import xmlrpclib
import logging

from django.contrib.sites.models import Site

from google.appengine.api import urlfetch

SEARCH_ENGINE_PING_URLS = (
    # adapted from <http://djangosnippets.org/snippets/1308/>
    # also see <http://screeley.com/entries/2009/jan/19/
    #           django-sitemaps-and-better-ping_google-function/>
    ('Google',      'http://www.google.com/webmasters/tools/ping', 'sitemap'),
    ('Yahoo',       'http://search.yahooapis.com/SiteExplorerService/V1/ping',
                                                                   'sitemap'),
    ('Ask',         'http://submissions.ask.com/ping',             'sitemap'),
    # for some reason Windows Live Search uses 'siteMap' instead of the
    # standard 'sitemap'
    ('Live Search', 'http://webmaster.live.com/ping.aspx',         'siteMap'),
)

def ping_sitemap(ping_url='http://www.google.com/webmasters/tools/ping',
                 sitemap_param='sitemap', sitemap_url='/sitemap.xml'):
    current_site = Site.objects.get_current()
    url = "http://%s%s" % (current_site.domain, sitemap_url)
    params = urllib.urlencode({sitemap_param:url})
    try:
        return urllib.urlopen("%s?%s" % (ping_url, params)).read()
    except Exception, e:
        return str(e)

def ping_all_search_engines(sitemap_url='/sitemap.xml'):
    return [(site, ping_sitemap(url, param, sitemap_url))
            for site, url, param in SEARCH_ENGINE_PING_URLS]

class GAEXMLRPCTransport(object):
    """Handles an HTTP transaction to an XML-RPC server.
    
    Adapted from <http://brizzled.clapper.org/id/80>
    """
    def __init__(self):
        pass
    
    def request(self, host, handler, request_body, verbose=0):
        result = None
        url = 'http://%s%s' % (host, handler)
        try:
            response = urlfetch.fetch(url,
                                      payload=request_body,
                                      method=urlfetch.POST,
                                      headers={'Content-Type': 'text/xml'})
        except:
            msg = 'Failed to fetch %s' % url
            logging.error(msg)
            raise xmlrpclib.ProtocolError(host + handler, 500, msg, {})

        if response.status_code != 200:
            logging.error('%s returned status code %s' %
                          (url, response.status_code))
            raise xmlrpclib.ProtocolError(host + handler,
                                          response.status_code,
                                          "",
                                          response.headers)
        else:
            result = self.__parse_response(response.content)

        return result
    
    def __parse_response(self, response_body):
        p, u = xmlrpclib.getparser(use_datetime=False)
        p.feed(response_body)
        return u.close()

def pingomatic():
    # see <http://fxp0.org.ua/2006/oct/29/pinging-pingomatic-django-blog/>
    server = xmlrpclib.ServerProxy('http://rpc.pingomatic.com/',
                                   GAEXMLRPCTransport())
    site = Site.objects.get_current()
    try:
        return server.weblogUpdates.ping(site.name, 'http://%s/' % site.domain)
    except Exception, e:
        return str(e)

