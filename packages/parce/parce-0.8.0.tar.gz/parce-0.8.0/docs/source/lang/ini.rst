ini
===

.. automodule:: parce.lang.ini
    :members:
    :undoc-members:
    :show-inheritance:

Example:
--------

Root lexicon ``Ini.root`` and text:

.. code-block:: ini

    ; last modified 1 April 2001 by John Doe
    [owner]
    name=John Doe
    organization=Acme Widgets Inc.
    
    [database]
    ; use IP address in case network name resolution is not working
    server=192.0.2.62
    port=143
    file="payroll.dat"

Result tree::

    <Context Ini.root at 0-215 (23 children)>
     ├╴<Token ';' at 0:1 (Comment)>
     ├╴<Context Ini.comment at 1-40 (1 child)>
     │  ╰╴<Token ' last modified 1 April 2001 '... at 1:40 (Comment)>
     ├╴<Token '[' at 41:42 (Delimiter.Section)>
     ├╴<Context Ini.section at 42-48 (2 children)>
     │  ├╴<Token 'owner' at 42:47 (Name.Namespace.Section)>
     │  ╰╴<Token ']' at 47:48 (Delimiter.Section)>
     ├╴<Context Ini.key at 49-53 (1 child)>
     │  ╰╴<Token 'name' at 49:53 (Name.Identifier)>
     ├╴<Token '=' at 53:54 (Delimiter.Operator.Assignment)>
     ├╴<Context Ini.value at 54-62 (1 child)>
     │  ╰╴<Token 'John Doe' at 54:62 (Literal.Value)>
     ├╴<Context Ini.key at 63-75 (1 child)>
     │  ╰╴<Token 'organization' at 63:75 (Name.Identifier)>
     ├╴<Token '=' at 75:76 (Delimiter.Operator.Assignment)>
     ├╴<Context Ini.value at 76-93 (1 child)>
     │  ╰╴<Token 'Acme Widgets Inc.' at 76:93 (Literal.Value)>
     ├╴<Token '[' at 95:96 (Delimiter.Section)>
     ├╴<Context Ini.section at 96-105 (2 children)>
     │  ├╴<Token 'database' at 96:104 (Name.Namespace.Section)>
     │  ╰╴<Token ']' at 104:105 (Delimiter.Section)>
     ├╴<Token ';' at 106:107 (Comment)>
     ├╴<Context Ini.comment at 107-169 (1 child)>
     │  ╰╴<Token ' use IP address in case netw'... at 107:169 (Comment)>
     ├╴<Context Ini.key at 170-176 (1 child)>
     │  ╰╴<Token 'server' at 170:176 (Name.Identifier)>
     ├╴<Token '=' at 176:177 (Delimiter.Operator.Assignment)>
     ├╴<Context Ini.value at 177-187 (1 child)>
     │  ╰╴<Token '192.0.2.62' at 177:187 (Literal.Value)>
     ├╴<Context Ini.key at 188-192 (1 child)>
     │  ╰╴<Token 'port' at 188:192 (Name.Identifier)>
     ├╴<Token '=' at 192:193 (Delimiter.Operator.Assignment)>
     ├╴<Context Ini.value at 193-196 (1 child)>
     │  ╰╴<Token '143' at 193:196 (Literal.Value)>
     ├╴<Context Ini.key at 197-201 (1 child)>
     │  ╰╴<Token 'file' at 197:201 (Name.Identifier)>
     ├╴<Token '=' at 201:202 (Delimiter.Operator.Assignment)>
     ╰╴<Context Ini.value at 202-215 (1 child)>
        ╰╴<Token '"payroll.dat"' at 202:215 (Literal.Value)>


