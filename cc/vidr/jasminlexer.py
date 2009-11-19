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

from pygments.lexer import RegexLexer, include, bygroups, using, \
                           this, DelegatingLexer
from pygments.token import *

__all__ = ['JasminLexer']

class JasminLexer(RegexLexer):
    """
    For Jasmin assembly code.
    """
    name = 'Jasmin'
    aliases = ['jasmin']
    filenames = ['*.j']
    mimetypes = ['text/x-jasmin']
    
    whitespace = r'[\s\r\n]+'
    label = r'[^=:."\s-]+\s*'
    identifier = r'(?:[^\s\d][^\s]*)'
    string = r'"(\\"|[^"]|\\n|\\t)*"'

    tokens = {
        'numbers': [
            (r'[0-9]*.[0-9]+', Number.Float),
            (r'[0-9]+.[0-9]*', Number.Float),
            (r'0x[0-9a-fA-F]+', Number.Integer),
            (r'[0-9]+', Number.Integer),
        ],
        'root': [
            (r';.*', Comment),
            (whitespace, Text),
            (label+':', Name.Label),
            (r'(\.var\s+)([0-9]+)(\s+is\s+)(' + identifier + r')'
             r'(\s+)(' + identifier + r')(\s+from\s+)(' + label + r')'
             r'(\s+to\s+)(' + label + r')', bygroups(
                Name.Attribute, Number.Integer, Name.Attribute, Name.Constant,
                Text, Name.Constant, Name.Attribute, Name.Label,
                Name.Attribute, Name.Label)),
            (r'(\.catch\s+)(' + identifier + r')(\s+from\s+)(' + label + r')'
             r'(\s+to\s+)(' + label + r')(\s+using\s+)(' + label + r')',
             bygroups(
                Name.Attribute, Name.Constant, Name.Attribute, Name.Label,
                Name.Attribute, Name.Label, Name.Attribute, Name.Label)),
            (r'\.end\s+[a-z]+', Name.Attribute),
            (r'\.[a-z]+', Name.Attribute, 'directive-args'),
            (identifier, Name.Function, 'instruction-args'),
        ],
        'directive-args': [
            (r';.*', Comment, '#pop'),
            (r'\s*[\r\n]+', Text, '#pop'),
            (whitespace, Text),
            (string, String),
            include('numbers'),
            (identifier, Name.Constant),
        ],
        'instruction-args': [
            (r';.*', Comment, '#pop'),
            (r'[\r\n]+', Text, '#pop'),
            (whitespace, Text),
            (string, String),
            include('numbers'),
            (identifier, Name.Constant),
        ],
    }

from pygments.lexers._mapping import LEXERS
LEXERS['JasminLexer'] = ('cc.vidr.jasminlexer',
                         JasminLexer.name,
                         tuple(JasminLexer.aliases),
                         tuple(JasminLexer.filenames),
                         tuple(JasminLexer.mimetypes))

