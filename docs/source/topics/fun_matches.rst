.. _fun-matches:

Function matches
================

Match functions are like :ref:`matches<std-matches>` but take parameters.
For example the most obvious of these is :code:`re(regex)` which simply
incorporates the regular expression you specify. Another though is
:code:`fixedwidth(width)`, so :code:`fixedwidth(7)` for example will incorporate
a regular expression :code:`.{7}` and post process the result to strip any leading
and trailing white space, which is usually what you want for getting the
contents of a fixed width column.

Making your own match function
------------------------------

There isn't a lot more to learn to make a match function, once you know about
:ref:`making matches<std-matches>`. You can add custom matche functions like
this:

   >>> import re
   >>> import sttp
   >>> @sttp.ext.register()
   ... class MyWordNumMatchFun(sttp.ext.match_fun.MatchFun):
   ...     name = 'word_num'
   ...     cast = int
   ...     def __init__(self, word):
   ...         self.regex = re.escape(word) + r'\d+'
   ...     def post_proc(self, string):
   ...         return super().post_proc(re.search(r'\d+', string).group(0))

This matches any word with a number conjoined, and the number is returned.

Now you can use it like so:

   >>> in_template = '''m> {{ wibble = word_num("foo") }}'''
   >>> in_text     = '''foo123'''
   >>> assert sttp.Parser(template = in_template).parse(in_text) == {'wibble': 123}

The regular expression formed by :code:`word_num("foo")` is :code:`foo\d+` so anything
like :code:`"foo123"` or :code:`"foo1"` will match and :code:`123` and :code:`1`
returned respectively. Anything not beginning with "foo" will not of course match.
