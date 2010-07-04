import os
import cgi
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from util import humanize_list
from pytextcat import classify

class PyTextCat(webapp.RequestHandler):
    def render(self, template_dict={}):
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_dict))

    def get(self):
        self.render()

    def post(self):
        text = self.request.get('text')
        if not text:
            self.render()
            return

        text = text.encode('utf-8')
        ranks = classify(text)
        ans = []
        for i,(rank,(lang,enc)) in enumerate(ranks):
            lang = lang.replace('_',' ').title()
            if enc: lang = "%s (%s)" % (lang,enc)
            if rank < 1.05: ans.append(lang)
            rank = int(100*rank) - 100
            ranks[i] = (lang,rank)
        self.render({'text': cgi.escape(text), 'ans': humanize_list(ans, 'or'), 'ranks': ranks})

def main():
    application = webapp.WSGIApplication([
        ('/projects/pytextcat/', PyTextCat),
    ])
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
