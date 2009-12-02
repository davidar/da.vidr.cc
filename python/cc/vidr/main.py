from common.appenginepatch.main import main

# prevent "ImportError: cannot import name TextLexer" when
# markdown.extensions.codehilite.Codehilite.hilite tries
# to import TextLexer from pygments.lexers
from pygments.lexers.special import TextLexer

# register JasminLexer
from cc.vidr.jasminlexer import JasminLexer

if __name__ == '__main__': main()
