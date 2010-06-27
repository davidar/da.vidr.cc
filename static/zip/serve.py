from google.appengine.ext import webapp, zipserve

def make_zip_handler(zipfilename, prefix=''):
    zipfilename += '.zip'
    if prefix: prefix += '/'
    class CustomZipHandler(zipserve.ZipHandler):
        def get(self, name):
            self.ServeFromZipFile(zipfilename, prefix + name)
    return CustomZipHandler

def main():
    application = webapp.WSGIApplication([
        ('/jsmath/fonts/(.*)',       make_zip_handler('jsMath-fonts-1.3', 'jsMath/fonts')),
        ('/jsmath/(.*)',             make_zip_handler('jsMath-3.6e',      'jsMath-3.6e')),
        ('/colorpicker/(.*)',        make_zip_handler('colorpicker')),
        ('/projects/lljvm/doc/(.*)', make_zip_handler('lljvm-doc-0.2',    'lljvm-doc-0.2')),
    ])
    webapp.util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
