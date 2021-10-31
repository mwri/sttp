Hello tables
============

The final :ref:`hello world<hello world>` example resulted in a table, but
here's a more obvious looking table:

::

   Num   Server               Uptime
   1     wibble.domain.com    1d 5h
   2     zap.domain.com       100d 1h
   3     foobar.domain.com    3d 10h

Noddy solution
--------------

This can be parsed very easily using no more features than the
:ref:`hello world<hello world>` examples, like this:

   >>> import sttp
   >>>
   >>> in_template = '''m> Num   Server               Uptime
   ... m*> {{ num = integer }}{{ ws }}{{ server = non_ws }}{{ ws }}{{ uptime = string }}
   ... '''
   >>>
   >>> in_text = '''Num   Server               Uptime
   ... 1     wibble.domain.com    1d 5h
   ... 2     zap.domain.com       100d 1h
   ... 3     foobar.domain.com    3d 10h
   ... '''
   >>>
   >>> parser     = sttp.Parser(template = in_template)
   >>> out_struct = parser.parse(in_text)
   >>>
   >>> assert out_struct == [
   ...     {'num': 1, 'server': 'wibble.domain.com', 'uptime': '1d 5h'},
   ...     {'num': 2, 'server': 'zap.domain.com',    'uptime': '100d 1h'},
   ...     {'num': 3, 'server': 'foobar.domain.com', 'uptime': '3d 10h'},
   ... ]

The "num" field has been converted from text to an integer numeric value
because of the use of the `integer` match term. You could if you wanted to
implement a :ref:`custom matches<custom-matches>` for the uptime field which
converted that into seconds, or a `time delta object <https://docs.python.org/3/library/datetime.html#datetime.timedelta>`_,
and the server field could be presented as a
`IPv4Address or IPv6Address object <https://docs.python.org/3/library/datetime.html#datetime.timedelta>`_.
See :ref:`custom matches<custom-matches>` for more information about this.

This table is particularly easy to parse mainly because it's clear there is
no white space in any of the field values except the last one. If there is
white space there are plenty of other options though.

Fixed width solution
--------------------

Here is a solution using the :code:`fixedwidth()` match function:

    >>> import sttp
    >>> in_template = '''m> Num   Server               Uptime
    ... m*> {{ int num = fixedwidth(6) }}{{ server = fixedwidth(21) }}{{ uptime = string }}
    ... '''
    >>> in_text = '''Num   Server               Uptime
    ... 1     wibble.domain.com    1d 5h
    ... 2     zap.domain.com       100d 1h
    ... 3     foobar.domain.com    3d 10h
    ... '''
    >>> parser     = sttp.Parser(template = in_template)
    >>> out_struct = parser.parse(in_text)
    >>> assert out_struct == [
    ...     {'num': 1, 'server': 'wibble.domain.com', 'uptime': '1d 5h'},
    ...     {'num': 2, 'server': 'zap.domain.com',    'uptime': '100d 1h'},
    ...     {'num': 3, 'server': 'foobar.domain.com', 'uptime': '3d 10h'},
    ... ]

Another feature is used here, because the fixedwidth match function returns a
string, not an integer, the :code:`num` variable is given a :code:`int` type
and this overrides any match or match function type, casting the return value.
If this is not a possible cast there will be a run time error of course.

Tables with extra data
----------------------

What if the input data looks like this:

::

   Num   Server               Uptime
   1     wibble.domain.com    1d 5h
   2     zap.domain.com       100d 1h
   3     foobar.domain.com    3d 10h
   Total: 3

If you add :code:`m> Total: {{ integer }}` to the end of the template, then
this will parse fine, but what if you want to capture the :code:`3`? The
:code:`m*>` implies a list, but the :code:`m>` implies a dict, so if you
make the last template line :code:`m> Total: {{ total = integer }}` the
template will not compile as it can't integrate these data types without
advice.

There are two things you can do to resolve this. The first way will result in
this parse:

::

   [
       {'num': 1, 'server': 'wibble.domain.com', 'uptime': '1d 5h'},
       {'num': 2, 'server': 'zap.domain.com',    'uptime': '100d 1h'},
       {'num': 3, 'server': 'foobar.domain.com', 'uptime': '3d 10h'},
       {'total': 3},
   ]

The second, which personally I must prefer, as it doesn't create a list with
a mixed schema, results in this:

::

   {
       'total': 3,
       'servers': [
           {'num': 1, 'server': 'wibble.domain.com', 'uptime': '1d 5h'},
           {'num': 2, 'server': 'zap.domain.com',    'uptime': '100d 1h'},
           {'num': 3, 'server': 'foobar.domain.com', 'uptime': '3d 10h'},
       ],
   }

To achieve the first solution, pass :code:`allow_mixed_lists = True` to your
:code:`sttp.Parser` constructor, like this:

    >>> import sttp
    >>> in_template = '''m> Num   Server               Uptime
    ... m*> {{ int num = fixedwidth(6) }}{{ server = fixedwidth(21) }}{{ uptime = string }}
    ... m> Total: {{ total = integer }}
    ... '''
    >>> in_text = '''Num   Server               Uptime
    ... 1     wibble.domain.com    1d 5h
    ... 2     zap.domain.com       100d 1h
    ... 3     foobar.domain.com    3d 10h
    ... Total: 3
    ... '''
    >>> parser     = sttp.Parser(template = in_template, allow_mixed_lists = True)
    >>> out_struct = parser.parse(in_text)
    >>> assert out_struct == [
    ...     {'num': 1, 'server': 'wibble.domain.com', 'uptime': '1d 5h'},
    ...     {'num': 2, 'server': 'zap.domain.com',    'uptime': '100d 1h'},
    ...     {'num': 3, 'server': 'foobar.domain.com', 'uptime': '3d 10h'},
    ...     {'total': 3},
    ... ]

The second solution, you have to give it a hint that the list of servers has
to be stored as a dict value, which you do by making the template this:

::

   m> Num   Server               Uptime
   m*(servers)> {{ int num = fixedwidth(6) }}{{ server = fixedwidth(21) }}{{ uptime = string }}
   m> Total: {{ total = integer }}

Like this:

    >>> import sttp
    >>> in_template = '''m> Num   Server               Uptime
    ... m*(servers)> {{ int num = fixedwidth(6) }}{{ server = fixedwidth(21) }}{{ uptime = string }}
    ... m> Total: {{ total = integer }}
    ... '''
    >>> in_text = '''Num   Server               Uptime
    ... 1     wibble.domain.com    1d 5h
    ... 2     zap.domain.com       100d 1h
    ... 3     foobar.domain.com    3d 10h
    ... Total: 3
    ... '''
    >>> parser     = sttp.Parser(template = in_template, allow_mixed_lists = True)
    >>> out_struct = parser.parse(in_text)
    >>> assert out_struct == {
    ...     'total': 3,
    ...     'servers': [
    ...         {'num': 1, 'server': 'wibble.domain.com', 'uptime': '1d 5h'},
    ...         {'num': 2, 'server': 'zap.domain.com',    'uptime': '100d 1h'},
    ...         {'num': 3, 'server': 'foobar.domain.com', 'uptime': '3d 10h'},
    ...     ],
    ... }
