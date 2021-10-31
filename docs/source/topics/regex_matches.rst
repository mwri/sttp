.. _re-matches:

Regex matches
=============

Regex matches are matches which are pure regular expression.

For example, take this input:

::

   Num   Server               Uptime
   1     wibble.domain.com    1d 5h
   2     zap.domain.com       100d 1h
   3     foobar.domain.com    3d 10h

The following template will parse it:

::

   r> ^Num\s+Server\s+Uptime$
   r*> ^\d+\s+\S+\s+(\d+[dhms] ?)+$

The :code:`^` and :code:`$` are optional and as with regular expressions in
general, they match the start and end of the line. Without them a match with
other "junk" beginning and/or end will be permitted.

In full then:

   >>> import sttp
   >>> in_template = '''r> ^Num\s+Server\s+Uptime$
   ... r*> ^\d+\s+\S+\s+(\d+[dhms] ?)+$
   ... '''
   >>> in_text = '''Num   Server               Uptime
   ... 1     wibble.domain.com    1d 5h
   ... 2     zap.domain.com       100d 1h
   ... 3     foobar.domain.com    3d 10h
   ... '''
   >>> parser     = sttp.Parser(template = in_template)
   >>> out_struct = parser.parse(in_text)
   >>> assert out_struct is None

You can capture data too by providing variable names, but it is limited to
capturing entire lines. For example:

    >>> import sttp
    >>> in_template = '''r(hdr)> ^Num\s+Server\s+Uptime$
    ... r*(rows)> ^\d+\s+\S+\s+(\d+[dhms] ?)+$
    ... '''
    >>> in_text = '''Num   Server               Uptime
    ... 1     wibble.domain.com    1d 5h
    ... 2     zap.domain.com       100d 1h
    ... 3     foobar.domain.com    3d 10h
    ... '''
    >>> parser     = sttp.Parser(template = in_template)
    >>> out_struct = parser.parse(in_text)
    >>> assert out_struct == {
    ...     'hdr': 'Num   Server               Uptime',
    ...     'rows': [
    ...         '1     wibble.domain.com    1d 5h',
    ...         '2     zap.domain.com       100d 1h',
    ...         '3     foobar.domain.com    3d 10h',
    ...     ]
    ... }

Here you can see the variable names :code:`hdr` and :code:`rows` are given
using the same format as with matches.

If you want to force a list result you can use the :code:`.` variable name:

   >>> import sttp
   >>> in_template = '''r> ^Num\s+Server\s+Uptime$
   ... r*(.)> ^\d+\s+\S+\s+(\d+[dhms] ?)+$
   ... '''
   >>> in_text = '''Num   Server               Uptime
   ... 1     wibble.domain.com    1d 5h
   ... 2     zap.domain.com       100d 1h
   ... 3     foobar.domain.com    3d 10h
   ... '''
   >>> parser     = sttp.Parser(template = in_template)
   >>> out_struct = parser.parse(in_text)
   >>> assert out_struct == [
   ...     '1     wibble.domain.com    1d 5h',
   ...     '2     zap.domain.com       100d 1h',
   ...     '3     foobar.domain.com    3d 10h',
   ... ]
