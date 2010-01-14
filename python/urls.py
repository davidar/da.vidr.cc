from django.conf.urls.defaults import *
from ragendja.urlsauto import urlpatterns
from ragendja.auth.urls import urlpatterns as auth_patterns
from django.contrib import admin

from blog.models import BlogSitemap, BlogFeed
from pages.models import PagesSitemap

admin.autodiscover()
handler500 = 'ragendja.views.server_error'
urlpatterns = auth_patterns + patterns('',
    (r'^admin/(.*)', admin.site.root),
    
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': {'blog': BlogSitemap, 'pages': PagesSitemap}}),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
        {'feed_dict': {'blog': BlogFeed}}),
    
    (r'^google617b8218f69f98a2.html$', 'cc.vidr.util.dummy_view'),
    (r'^googlea23819e3375b5c52.html$', 'cc.vidr.util.dummy_view'),
    (r'^LiveSearchSiteAuth.xml$', 'cc.vidr.util.dummy_view',
        {'output': '<?xml version="1.0"?>\n<users>\n'
                   '<user>5C6F26063F93958A50C0EE134949F0B9</user>\n'
                   '</users>\n',
         'mimetype': 'application/xml'}),
    (r'^y_key_2916d2d19e6cfb1a.html$', 'cc.vidr.util.dummy_view',
        {'output': '3fc5855b0a114b46\n', 'mimetype': 'text/plain'}),
    
    (r'^blank.html$', 'cc.vidr.util.dummy_view'),
    
    (r'^rpc_relay.html$', 'cc.vidr.util.dummy_view',
        {'output': '<html><head><script type="text/javascript" '
         'src="http://www.google.com/friendconnect/script/rpc_relay.js">'
         '</script></head></html>'}),
    (r'^canvas.html$', 'django.views.generic.simple.direct_to_template',
        {'template': 'gfc-canvas.html'}),
    
    (r'^robots.txt$', 'django.views.generic.simple.direct_to_template',
        {'template': 'robots.txt', 'mimetype': 'text/plain'}),
    (r'^xrds$', 'django.views.generic.simple.direct_to_template',
        {'template': 'xrds.xml', 'mimetype': 'application/xrds+xml'}),
    
    #(r'^avatar.png$', 'django.views.generic.simple.redirect_to', # 80x80
    #    {'url': 'http://i36.photobucket.com/albums/e36/nemti/avatar.png'}),
    
    (r'^jsmath/fonts/(.*)$', 'cc.vidr.util.zipserve',
        {'zipfilename': 'jsMath-fonts-1.3', 'prefix': 'jsMath/fonts'}),
    (r'^jsmath/(.*)$', 'cc.vidr.util.zipserve',
        {'zipfilename': 'jsMath-3.6b', 'prefix': 'jsMath'}),
    (r'^colorpicker/(.*)$', 'cc.vidr.util.zipserve',
        {'zipfilename': 'colorpicker'}),
    (r'^projects/lljvm/doc/(.*)$', 'cc.vidr.util.zipserve',
        {'zipfilename': 'lljvm-doc-0.2', 'prefix': 'lljvm-doc-0.2'}),
    
    (r'^export.json$', 'backup.views.export_json'),
    (r'^source.zip$', 'backup.views.export_source_zip'),
    (r'^source-full.zip$', 'backup.views.export_source_zip', {'full': True}),
    (r'^import/json/$', 'backup.views.import_json'),
    (r'^import/wxr/$', 'backup.views.import_wxr'),
    
    (r'^ping/$', 'blog.views.ping'),
    
    (r'^$', 'blog.views.index'),
    (r'^page/(\d*)/$', 'blog.views.index'),
    
    (r'^new/post/$', 'blog.views.edit'),
    (r'^new/category/$', 'blog.views.edit_category'),
    (r'^new/page/$', 'pages.views.edit'),
    
    (r'^(\d{4})/(\d{2})/(\d{2})/([\w-]+)/edit/$', 'blog.views.edit'),
    (r'^(\d{4})/(\d{2})/(\d{2})/([\w-]+)/$', 'blog.views.view'),
    
    (r'^category/([\w/-]+)/edit/$', 'blog.views.edit_category'),
    (r'^category/([\w/-]+)/$', 'blog.views.view_category'),
    (r'^category/([\w/-]+)page/(\d*)/$', 'blog.views.view_category'),
    
    (r'^([\w/-]+)/edit/$', 'pages.views.edit'),
    (r'^([\w/-]+)/source/$', 'pages.views.view_source'),
    (r'^([\w/-]+)/$', 'pages.views.view'),
) + urlpatterns
