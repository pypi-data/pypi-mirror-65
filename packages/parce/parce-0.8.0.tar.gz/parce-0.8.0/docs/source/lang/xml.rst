xml
===

.. automodule:: parce.lang.xml
    :members:
    :undoc-members:
    :show-inheritance:

Example:
--------

Root lexicon ``Xml.root`` and text:

.. code-block:: xml

    <?xml version="1.0" encoding="ISO-8859-1"?>
    <note type="urgent">
      <to>Tove</to>
      <from>Jani&eacute;</from>
      <heading>Reminder</heading>
      <body>Don't <em>forget me</em> this weekend!</body>
    </note>

Result tree::

    <Context Xml.root at 0-201 (8 children)>
     ├╴<Token '<?' at 0:2 (Comment.PI.Start)>
     ├╴<Context Xml.pi at 2-43 (11 children)>
     │  ├╴<Token 'xml ' at 2:6 (Comment.PI)>
     │  ├╴<Token 'version' at 6:13 (Name.Attribute)>
     │  ├╴<Token '=' at 13:14 (Delimiter.Operator)>
     │  ├╴<Token '"' at 14:15 (Literal.String)>
     │  ├╴<Context Xml.dqstring at 15-19 (2 children)>
     │  │  ├╴<Token '1.0' at 15:18 (Literal.String)>
     │  │  ╰╴<Token '"' at 18:19 (Literal.String)>
     │  ├╴<Token ' ' at 19:20 (Comment.PI)>
     │  ├╴<Token 'encoding' at 20:28 (Name.Attribute)>
     │  ├╴<Token '=' at 28:29 (Delimiter.Operator)>
     │  ├╴<Token '"' at 29:30 (Literal.String)>
     │  ├╴<Context Xml.dqstring at 30-41 (2 children)>
     │  │  ├╴<Token 'ISO-8859-1' at 30:40 (Literal.String)>
     │  │  ╰╴<Token '"' at 40:41 (Literal.String)>
     │  ╰╴<Token '?>' at 41:43 (Comment.PI.End)>
     ├╴<Token '\n' at 43:44 (Text)>
     ├╴<Token '<' at 44:45 (Delimiter)>
     ├╴<Token 'note' at 45:49 (Name.Tag)>
     ├╴<Context Xml.attrs at 50-64 (5 children)>
     │  ├╴<Token 'type' at 50:54 (Name.Attribute)>
     │  ├╴<Token '=' at 54:55 (Delimiter.Operator)>
     │  ├╴<Token '"' at 55:56 (Literal.String)>
     │  ├╴<Context Xml.dqstring at 56-63 (2 children)>
     │  │  ├╴<Token 'urgent' at 56:62 (Literal.String)>
     │  │  ╰╴<Token '"' at 62:63 (Literal.String)>
     │  ╰╴<Token '>' at 63:64 (Delimiter)>
     ├╴<Context Xml.tag at 64-200 (24 children)>
     │  ├╴<Token '\n  ' at 64:67 (Text)>
     │  ├╴<Token '<' at 67:68 (Delimiter)>
     │  ├╴<Token 'to' at 68:70 (Name.Tag)>
     │  ├╴<Token '>' at 70:71 (Delimiter)>
     │  ├╴<Context Xml.tag at 71-80 (4 children)>
     │  │  ├╴<Token 'Tove' at 71:75 (Text)>
     │  │  ├╴<Token '</' at 75:77 (Delimiter)>
     │  │  ├╴<Token 'to' at 77:79 (Name.Tag)>
     │  │  ╰╴<Token '>' at 79:80 (Delimiter)>
     │  ├╴<Token '\n  ' at 80:83 (Text)>
     │  ├╴<Token '<' at 83:84 (Delimiter)>
     │  ├╴<Token 'from' at 84:88 (Name.Tag)>
     │  ├╴<Token '>' at 88:89 (Delimiter)>
     │  ├╴<Context Xml.tag at 89-108 (5 children)>
     │  │  ├╴<Token 'Jani' at 89:93 (Text)>
     │  │  ├╴<Token '&eacute;' at 93:101 (Escape.Entity)>
     │  │  ├╴<Token '</' at 101:103 (Delimiter)>
     │  │  ├╴<Token 'from' at 103:107 (Name.Tag)>
     │  │  ╰╴<Token '>' at 107:108 (Delimiter)>
     │  ├╴<Token '\n  ' at 108:111 (Text)>
     │  ├╴<Token '<' at 111:112 (Delimiter)>
     │  ├╴<Token 'heading' at 112:119 (Name.Tag)>
     │  ├╴<Token '>' at 119:120 (Delimiter)>
     │  ├╴<Context Xml.tag at 120-138 (4 children)>
     │  │  ├╴<Token 'Reminder' at 120:128 (Text)>
     │  │  ├╴<Token '</' at 128:130 (Delimiter)>
     │  │  ├╴<Token 'heading' at 130:137 (Name.Tag)>
     │  │  ╰╴<Token '>' at 137:138 (Delimiter)>
     │  ├╴<Token '\n  ' at 138:141 (Text)>
     │  ├╴<Token '<' at 141:142 (Delimiter)>
     │  ├╴<Token 'body' at 142:146 (Name.Tag)>
     │  ├╴<Token '>' at 146:147 (Delimiter)>
     │  ├╴<Context Xml.tag at 147-192 (9 children)>
     │  │  ├╴<Token "Don't " at 147:153 (Text)>
     │  │  ├╴<Token '<' at 153:154 (Delimiter)>
     │  │  ├╴<Token 'em' at 154:156 (Name.Tag)>
     │  │  ├╴<Token '>' at 156:157 (Delimiter)>
     │  │  ├╴<Context Xml.tag at 157-171 (4 children)>
     │  │  │  ├╴<Token 'forget me' at 157:166 (Text)>
     │  │  │  ├╴<Token '</' at 166:168 (Delimiter)>
     │  │  │  ├╴<Token 'em' at 168:170 (Name.Tag)>
     │  │  │  ╰╴<Token '>' at 170:171 (Delimiter)>
     │  │  ├╴<Token ' this weekend!' at 171:185 (Text)>
     │  │  ├╴<Token '</' at 185:187 (Delimiter)>
     │  │  ├╴<Token 'body' at 187:191 (Name.Tag)>
     │  │  ╰╴<Token '>' at 191:192 (Delimiter)>
     │  ├╴<Token '\n' at 192:193 (Text)>
     │  ├╴<Token '</' at 193:195 (Delimiter)>
     │  ├╴<Token 'note' at 195:199 (Name.Tag)>
     │  ╰╴<Token '>' at 199:200 (Delimiter)>
     ╰╴<Token '\n' at 200:201 (Text)>


