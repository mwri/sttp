Strict Text Template Parsing (STTP)
===================================

.. toctree::
   :maxdepth: 2

   topics/installation
   topics/quick_start
   topics/motivation
   topics/examples
   topics/templ_ref
   topics/matches
   topics/fun_matches
   topics/regex_matches

Demo
====

The goal of **STTP** so to make strict parsing easy. Imagine taking some
text that you want to parse and simply editing it to mark up where bits
change with regular expressions, and specify where lines can be repeated, then
use that as a template for parsing to get out the data you want. The parse
will succeed if the template matches, and fail if it doesn't. That's the
core of what STTP does.

Here's a sample input to make an example out of:

::

   Num   Server               Uptime
   1     wibble.domain.com    1d 5h
   2     zap.domain.com       100d 1h
   3     foobar.domain.com    3d 10h

The following template will parse it:

::

   m> Num   Server               Uptime
   m*> {{ int num = integer }}{{ ws }}{{ server = non_ws }}{{ ws }}{{ uptime = string }}

The first **m** (for match) prefixed line requires STTP to match the given line
exactly. The second line's prefix is the same except there is an asterix. This
is regular expression style notation and means "match zero or more times". The
rest of the line is composed of bits inside double curley brackets, and each
of those bits amounts to a regular expression, and optionally a variable name
which is used to catalogue the matched data. The result of parsing the above
text with the above template is this:

::

   [
       {'num': 1, 'server': 'wibble.domain.com', 'uptime': '1d 5h'},
       {'num': 2, 'server': 'zap.domain.com',    'uptime': '100d 1h'},
       {'num': 3, 'server': 'foobar.domain.com', 'uptime': '3d 10h'}
   ]

The parsing is done simply like this:

.. code-block:: python

   parser     = sttp.Parser(template = in_template)
   out_struct = parser.parse(in_text)

Here's a full working example showing the whole thing working:

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
   ...     {'num': 3, 'server': 'foobar.domain.com', 'uptime': '3d 10h'}
   ... ]

Notice that the first column is actually an integer, not a string of digits.
This is part of the behaviour of the :code:`integer` match.
