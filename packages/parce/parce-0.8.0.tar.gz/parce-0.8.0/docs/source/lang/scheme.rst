scheme
======

.. automodule:: parce.lang.scheme
    :members:
    :undoc-members:
    :show-inheritance:

Example:
--------

Root lexicon ``Scheme.root`` and text:

.. code-block:: scheme

    
    ; convert to html entities
    (define (attribute-escape s)
      (string-substitute "\n" "&#10;"
        (string-substitute "\"" "&quot;"
          (string-substitute "&" "&amp;"
            s))))
    

Result tree::

    <Context Scheme.root at 1-178 (4 children)>
     ├╴<Token ';' at 1:2 (Comment)>
     ├╴<Context Scheme.singleline_comment at 2-27 (1 child)>
     │  ╰╴<Token ' convert to html entities' at 2:27 (Comment)>
     ├╴<Token '(' at 28:29 (Delimiter.OpenParen)>
     ╰╴<Context Scheme.list at 29-178 (6 children)>
        ├╴<Token 'define' at 29:35 (Keyword)>
        ├╴<Token '(' at 36:37 (Delimiter.OpenParen)>
        ├╴<Context Scheme.list at 37-56 (3 children)>
        │  ├╴<Token 'attribute-escape' at 37:53 (Name)>
        │  ├╴<Token 's' at 54:55 (Name)>
        │  ╰╴<Token ')' at 55:56 (Delimiter.CloseParen)>
        ├╴<Token '(' at 59:60 (Delimiter.OpenParen)>
        ├╴<Context Scheme.list at 60-177 (8 children)>
        │  ├╴<Token 'string-substitute' at 60:77 (Name)>
        │  ├╴<Token '"' at 78:79 (Literal.String)>
        │  ├╴<Context Scheme.string at 79-82 (2 children)>
        │  │  ├╴<Token '\\n' at 79:81 (Literal.String)>
        │  │  ╰╴<Token '"' at 81:82 (Literal.String)>
        │  ├╴<Token '"' at 83:84 (Literal.String)>
        │  ├╴<Context Scheme.string at 84-90 (2 children)>
        │  │  ├╴<Token '&#10;' at 84:89 (Literal.String)>
        │  │  ╰╴<Token '"' at 89:90 (Literal.String)>
        │  ├╴<Token '(' at 95:96 (Delimiter.OpenParen)>
        │  ├╴<Context Scheme.list at 96-176 (8 children)>
        │  │  ├╴<Token 'string-substitute' at 96:113 (Name)>
        │  │  ├╴<Token '"' at 114:115 (Literal.String)>
        │  │  ├╴<Context Scheme.string at 115-118 (2 children)>
        │  │  │  ├╴<Token '\\"' at 115:117 (Literal.String.Escape)>
        │  │  │  ╰╴<Token '"' at 117:118 (Literal.String)>
        │  │  ├╴<Token '"' at 119:120 (Literal.String)>
        │  │  ├╴<Context Scheme.string at 120-127 (2 children)>
        │  │  │  ├╴<Token '&quot;' at 120:126 (Literal.String)>
        │  │  │  ╰╴<Token '"' at 126:127 (Literal.String)>
        │  │  ├╴<Token '(' at 134:135 (Delimiter.OpenParen)>
        │  │  ├╴<Context Scheme.list at 135-175 (7 children)>
        │  │  │  ├╴<Token 'string-substitute' at 135:152 (Name)>
        │  │  │  ├╴<Token '"' at 153:154 (Literal.String)>
        │  │  │  ├╴<Context Scheme.string at 154-156 (2 children)>
        │  │  │  │  ├╴<Token '&' at 154:155 (Literal.String)>
        │  │  │  │  ╰╴<Token '"' at 155:156 (Literal.String)>
        │  │  │  ├╴<Token '"' at 157:158 (Literal.String)>
        │  │  │  ├╴<Context Scheme.string at 158-164 (2 children)>
        │  │  │  │  ├╴<Token '&amp;' at 158:163 (Literal.String)>
        │  │  │  │  ╰╴<Token '"' at 163:164 (Literal.String)>
        │  │  │  ├╴<Token 's' at 173:174 (Name)>
        │  │  │  ╰╴<Token ')' at 174:175 (Delimiter.CloseParen)>
        │  │  ╰╴<Token ')' at 175:176 (Delimiter.CloseParen)>
        │  ╰╴<Token ')' at 176:177 (Delimiter.CloseParen)>
        ╰╴<Token ')' at 177:178 (Delimiter.CloseParen)>


