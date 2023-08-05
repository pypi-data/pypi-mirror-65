css
===

.. automodule:: parce.lang.css
    :members:
    :undoc-members:
    :show-inheritance:

Example:
--------

Root lexicon ``Css.root`` and text:

.. code-block:: css

    h1.main {
        color: red;
        background: grey url(bla.png);
    }

Result tree::

    <Context Css.root at 0-62 (2 children)>
     ├╴<Context Css.prelude at 0-9 (2 children)>
     │  ├╴<Context Css.selector at 0-7 (3 children)>
     │  │  ├╴<Context Css.element_selector at 0-2 (1 child)>
     │  │  │  ╰╴<Token 'h1' at 0:2 (Name.Tag)>
     │  │  ├╴<Token '.' at 2:3 (Keyword)>
     │  │  ╰╴<Context Css.class_selector at 3-7 (1 child)>
     │  │     ╰╴<Token 'main' at 3:7 (Name.Class)>
     │  ╰╴<Token '{' at 8:9 (Delimiter)>
     ╰╴<Context Css.rule at 14-62 (3 children)>
        ├╴<Context Css.declaration at 14-25 (4 children)>
        │  ├╴<Context Css.property at 14-19 (1 child)>
        │  │  ╰╴<Token 'color' at 14:19 (Name.Property)>
        │  ├╴<Token ':' at 19:20 (Delimiter)>
        │  ├╴<Context Css.identifier at 21-24 (1 child)>
        │  │  ╰╴<Token 'red' at 21:24 (Literal.Color)>
        │  ╰╴<Token ';' at 24:25 (Delimiter)>
        ├╴<Context Css.declaration at 30-60 (7 children)>
        │  ├╴<Context Css.property at 30-40 (1 child)>
        │  │  ╰╴<Token 'background' at 30:40 (Name.Property)>
        │  ├╴<Token ':' at 40:41 (Delimiter)>
        │  ├╴<Context Css.identifier at 42-46 (1 child)>
        │  │  ╰╴<Token 'grey' at 42:46 (Literal.Color)>
        │  ├╴<Token 'url' at 47:50 (Name)>
        │  ├╴<Token '(' at 50:51 (Delimiter)>
        │  ├╴<Context Css.url_function at 51-59 (2 children)>
        │  │  ├╴<Token 'bla.png' at 51:58 (Literal.Url)>
        │  │  ╰╴<Token ')' at 58:59 (Delimiter)>
        │  ╰╴<Token ';' at 59:60 (Delimiter)>
        ╰╴<Token '}' at 61:62 (Delimiter)>


