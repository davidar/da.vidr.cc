import os

mapping = {
    '/apps/stumble/':     '/projects/stumble/',
    '/feeds/blog/':       '/atom.xml',
    '/tools/3dglobe/':    '/projects/3dglobe/',
    '/tools/rendermath/': '/projects/rendermath/',
    '/tools/webcol/':     '/projects/webcol/',
    '/tools/whatlang/':   '/projects/pytextcat/',
}

path = os.environ['PATH_INFO']
if path in mapping:
    print 'Status: 301'
    print 'Location: ', mapping[path]
    print
else:
    import not_found
