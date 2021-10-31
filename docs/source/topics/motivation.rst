Motivation
==========

Parsing is often a choice between doing something pragmatic, quick and
dirty and getting the job done, or spending a lot more time doing something
better and more robust. The goal of STTP is to make a robust solution really
easy so you have the best of both worlds.

To give you an quick idea of the parsing problems that can arise with the
simplest of cases, take this made up input (the same input is used in
the :ref:`quick start<quick start>`):

::

    Num   Server               Uptime
    1     wibble.domain.com    1d 5h
    2     zap.domain.com       100d 1h
    3     foobar.domain.com    3d 10h

You can parse this simply like this:

   >>> import re
   >>> in_text = '''Num   Server               Uptime
   ... 1     wibble.domain.com    1d 5h
   ... 2     zap.domain.com       100d 1h
   ... 3     foobar.domain.com    3d 10h
   ... '''
   >>> out_struct = [
   ...     entry.groupdict() for entry in
   ...     [re.match(r'(?P<num>\d+)\s+(?P<server>\S+)\s+(?P<uptime>\d+d \d+h)', line)
   ...         for line in in_text.split('\n')]
   ...     if entry is not None
   ... ]
   >>> assert out_struct == [
   ...     {'num': '1', 'server': 'wibble.domain.com', 'uptime': '1d 5h'},
   ...     {'num': '2', 'server': 'zap.domain.com',    'uptime': '100d 1h'},
   ...     {'num': '3', 'server': 'foobar.domain.com', 'uptime': '3d 10h'}
   ... ], out_struct

This sort of parsing can be a quick and pragmatic way to get what you want
but even this is not nearly as fast to write (and maintain) as using STTP, and
there are pitfalls. For example if the output was completely unexpected, an
error instead of the table for example, then the parse would still succeed! The
result would be an empty array, but that might be perfectly legitimate if it
wasn't for the error. Or, what if there were table entries but with an error
or warning as well. Of course you could check explicitly for errors you know
about, or maybe you can recognise errors generally, but if there is
an unexpected error or the error reporting format changes, you could be back
to getting an empty array with an error check that doesn't see an error any
more. This sort of parsing is not strict, and it can be dangerous.

Naturally you can implement extremely strict parsing which will only tolerate
exactly what you know of the text you are parsing and nothing else. Let's see
what that could look like in this example:

   >>> in_text = '''Num   Server               Uptime
   ... 1     wibble.domain.com    1d 5h
   ... 2     zap.domain.com       100d 1h
   ... 3     foobar.domain.com    3d 10h
   ... '''
   >>> lines = in_text.split('\n')
   >>> if len(lines) == 0:
   ...     raise Exception('input is empty')
   >>> header = lines.pop(0)
   >>> if header != 'Num   Server               Uptime':
   ...     raise Exception('input line 1 was not recognised header: ' + header)
   >>> out_struct = []
   >>> while lines:
   ...     line = lines.pop(0)
   ...     match = re.match(r'(?P<num>\d+)\s+(?P<server>\S+)\s+(?P<uptime>\d+d \d+h)', line)
   ...
   ...     if match:
   ...         out_struct.append(match.groupdict())
   ...     elif line != '' or len(lines) != 0:
   ...         raise Exception('unexpected line parsing table entries: ' + line)
   >>> assert out_struct == [
   ...     {'num': '1', 'server': 'wibble.domain.com', 'uptime': '1d 5h'},
   ...     {'num': '2', 'server': 'zap.domain.com',    'uptime': '100d 1h'},
   ...     {'num': '3', 'server': 'foobar.domain.com', 'uptime': '3d 10h'}
   ... ], out_struct

There's nothing difficult about this, but WOW, 14 lines of code, it's a long
way from that pragmatic one liner, and it would take you a LOT longer to write
it than the STTP template version, where the only interesting bit is the
template:

::

   m> Num   Server               Uptime
   m*> {{ int num = integer }}{{ ws }}{{ server = non_ws }}{{ ws }}{{ uptime = string }}

Fail fast
---------

This "only accept what you know and handle that correctly" is a
`Fail fast <https://en.wikipedia.org/wiki/Fail-fast>`_ approach. Fail fast
advocates that if something unexpected happens it's better to fail immediately
and clearly with all the context of the failure intact, than try to carry on
with possibly invalid results (and no way of knowing it), causing any number
of side effects later, such as an exception not obviously related to the parse
at all, or simply incorrect data, and maybe that data could be put in a
database, and there's probably no chance anyone will easily figure out why
that bit of data is wrong this time next week...

`Fail fast <https://en.wikipedia.org/wiki/Fail-fast>`_ might mean that something
crashes in production that wouldn't have if you had less strict parsing, but
isn't that crash better than corrupting a database without knowing it? A crash
and stack trace at the right time can often provide developers all they need
to know to understand what went wrong, and with good monitoring, efficient
agile toolchains and release processes, a new unit test could have been
written, the bug fixed, and a new revision released to production in minutes!
