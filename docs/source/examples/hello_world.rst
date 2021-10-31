Hello world
===========

There are three progressive examples here, the most noddy possible, something
a little more interesting, and finally a template that doesn't just assure a
match but also captures some data.

Really noddy
------------

Let's take this text input; two lines with "hello" on the first line and
"world" on the second:

::

   hello
   world

We can parse it like this:

   >>> import sttp
   >>> in_template = '''m> hello
   ... m> world
   ... '''
   >>> in_text = '''hello
   ... world
   ... '''
   >>> parser     = sttp.Parser(template = in_template)
   >>> out_struct = parser.parse(in_text)
   >>> assert out_struct == None

All it does in effect is validate that the input text is as stated, i.e. two
lines with "hello" on the first line, "world" on the second and nothing else.
If the input deviates then an exception will be raised.

More interesting
----------------

This example parses a text file with any number of lines, all beginning with
"hello" but where the second word may vary. Below the sample input is:

::

   hello world
   hello galaxy
   hello universe

The template used is a one liner:

::

   m*> hello {{ word }}

Here's the full working example:

   >>> import sttp
   >>> in_template = '''m*> hello {{ word }}'''
   >>> in_text = '''hello world
   ... hello galaxy
   ... hello universe
   ... '''
   >>> parser     = sttp.Parser(template = in_template)
   >>> out_struct = parser.parse(in_text)
   >>> assert out_struct == None

The :code:`m*` instead of :code:`m` means match zero or more times, so if
you give it an empty input, the above will still parse successfully. If it
was :code:`m+` then this would require at least one line that matched, just
like the regex modifiers.

Capturing data
--------------

Let's expand the previous example to capture the words:

   >>> import sttp
   >>> in_template = '''m+> hello {{ hello = word }}'''
   >>> in_text = '''hello world
   ... hello galaxy
   ... hello universe
   ... '''
   >>> parser     = sttp.Parser(template = in_template)
   >>> out_struct = parser.parse(in_text)
   >>> assert out_struct == [
   ...     {'hello': 'world'},
   ...     {'hello': 'galaxy'},
   ...     {'hello': 'universe'}
   ... ]

When a list result is implied (as with :code:`m+` and :code:`m*`) the list
elements will be a :code:`dict` so that any number of named values can be
derived per line. If your template was
:code:`m+> {{ hello = word }} {{ world = word }}` then "goodbye galaxy"
would parse as :code:`{'hello': 'goodbye', 'world': 'galaxy'}`:

   >>> import sttp
   >>> in_template = '''m+> {{ hello = word }} {{ world = word }}'''
   >>> in_text     = '''goodbye galaxy'''
   >>> parser     = sttp.Parser(template = in_template)
   >>> out_struct = parser.parse(in_text)
   >>> assert out_struct == [{'hello': 'goodbye', 'world': 'galaxy'}]
