lilypond
========

.. automodule:: parce.lang.lilypond
    :members:
    :undoc-members:
    :show-inheritance:

Example:
--------

Root lexicon ``LilyPond.root`` and text:

.. code-block:: lilypond

    
    \relative c'' {
      \time 7/4
      d2 c4 b2 a | b c4 b( a) g2
    }
    \addlyrics {
      Join us now and share the soft -- ware
    }

Result tree::

    <Context LilyPond.root at 1-115 (8 children)>
     ├╴<Token '\\relative' at 1:10 (Keyword)>
     ├╴<Token 'c' at 11:12 (Name.Pitch)>
     ├╴<Token "''" at 12:14 (Name.Pitch.Octave)>
     ├╴<Token '{' at 15:16 (Delimiter.OpenBrace)>
     ├╴<Context LilyPond.sequential at 19-59 (20 children)>
     │  ├╴<Token '\\time' at 19:24 (Name.Builtin)>
     │  ├╴<Token '7/4' at 25:28 (Literal.Number)>
     │  ├╴<Token 'd' at 31:32 (Name.Pitch)>
     │  ├╴<Token '2' at 32:33 (Literal.Number.Duration)>
     │  ├╴<Token 'c' at 34:35 (Name.Pitch)>
     │  ├╴<Token '4' at 35:36 (Literal.Number.Duration)>
     │  ├╴<Token 'b' at 37:38 (Name.Pitch)>
     │  ├╴<Token '2' at 38:39 (Literal.Number.Duration)>
     │  ├╴<Token 'a' at 40:41 (Name.Pitch)>
     │  ├╴<Token '|' at 42:43 (Delimiter.PipeSymbol)>
     │  ├╴<Token 'b' at 44:45 (Name.Pitch)>
     │  ├╴<Token 'c' at 46:47 (Name.Pitch)>
     │  ├╴<Token '4' at 47:48 (Literal.Number.Duration)>
     │  ├╴<Token 'b' at 49:50 (Name.Pitch)>
     │  ├╴<Token '(' at 50:51 (Delimiter.Spanner.Slur)>
     │  ├╴<Token 'a' at 52:53 (Name.Pitch)>
     │  ├╴<Token ')' at 53:54 (Delimiter.Spanner.Slur)>
     │  ├╴<Token 'g' at 55:56 (Name.Pitch)>
     │  ├╴<Token '2' at 56:57 (Literal.Number.Duration)>
     │  ╰╴<Token '}' at 58:59 (Delimiter.CloseBrace)>
     ├╴<Token '\\addlyrics' at 60:70 (Keyword.Lyric)>
     ├╴<Token '{' at 71:72 (Delimiter.OpenBrace)>
     ╰╴<Context LilyPond.lyricmode at 75-115 (10 children)>
        ├╴<Token 'Join' at 75:79 (Text.Lyric.LyricText)>
        ├╴<Token 'us' at 80:82 (Text.Lyric.LyricText)>
        ├╴<Token 'now' at 83:86 (Text.Lyric.LyricText)>
        ├╴<Token 'and' at 87:90 (Text.Lyric.LyricText)>
        ├╴<Token 'share' at 91:96 (Text.Lyric.LyricText)>
        ├╴<Token 'the' at 97:100 (Text.Lyric.LyricText)>
        ├╴<Token 'soft' at 101:105 (Text.Lyric.LyricText)>
        ├╴<Token '--' at 106:108 (Delimiter.Lyric.LyricHyphen)>
        ├╴<Token 'ware' at 109:113 (Text.Lyric.LyricText)>
        ╰╴<Token '}' at 114:115 (Delimiter.CloseBrace)>


