.. _std-matches:

Matches
=======

Matches are like named regular expressions with type information and post
processing.

When you create a template with something like :code:`m> {{ val = integer }}`
the :code:`integer` has an associated regular expression (:code:`\d+` in this
case), a type (:code:`int`) and (optionally) post processing. In this case
there is no post processing, but a :ref:`custom match<custom-matches>` could be
added which is like :code:`integer` but adds 493 to the parsed value. That sounds
a bit insane, but it could be done...

There are also :ref:`match functions<fun-matches>`, which are just like
the above, but take parameters. For example the most obvious of these is
:code:`re(regex)` which simply incorporates the regular expression you specify.

.. _custom-matches:

Making your own match
---------------------

You can add custom matches like this:

::

   >>> import sttp
   >>> @sttp.ext.register()
   ... class MySpecialMatch(sttp.ext.match.Match):
   ...     name  = 'special'
   ...     regex = r'(?:foo|bar|baz|bat)'

Now you can use it like so:

::

   >>> in_template = '''m> Special "{{ speciality = special }}".'''
   >>> in_text     = '''Special "foo".'''
   >>> assert sttp.Parser(template = in_template).parse(in_text) == {'speciality': 'foo'}

Giving it a type
----------------

There is already a `number` match in the core, but let's look at it's
implementation:

::

   @sttp.ext.register()
   class NumberCoreMatch(sttp.ext.match.Match):
       """Number match (floating point, though a decimal is not required so it will match integers too)."""

       name  = 'number'
       regex = r'\d+(?:\.\d+|)'
       cast  = float

The only news here is the `cast` attribute, which is `str` by default. Here
it is float, and that means the match (string) will be cast as a float, and
any variable you assign will be a `float`, not a string:

   >>> import sttp
   >>> in_template = '''m> Number {{ pi = number }}.'''
   >>> in_text     = '''Number 3.1415.'''
   >>> out_struct  = sttp.Parser(template = in_template).parse(in_text)
   >>> assert isinstance(out_struct['pi'], float)
   >>> assert out_struct['pi'] == 3.1415
   >>> assert not out_struct['pi'] == '3.1415'

Adding post processing
----------------------

It is also possible to post process any matched data. The cast is post
processing of course, but you can do more if you want. To do so you should
implement the `post_proc` method. You should invoke the super class `post_proc`
when you do so, either before or after the sub class (whatever is appropriate)
as it may increase forwards compatibility, and if you do not you will loose
the type cast functionality!

Before you provide a `post_proc` method, consider if the reason is valid.
Could you instead define a custom type class? For example, by default `cast`
is set to `str`, and for matches `integer` and `number` it is set to `int`
and `str` respectively, but you could set it to any class, such as
`StrippedString` defined as follows:

   >>> class StrippedString():
   ...     def __init__(self, string):
   ...         self._string = string.lstrip().rstrip()
   ...     def __str__(self):
   ...         return self._string
   ...     def post_proc(self, string):
   ...         return self._string.lstrip().rstrip()


In full:

.. testsetup:: *

   >>> import sttp
   >>> _ = sttp.ext.unregister_named('special', sttp.ext.match.Match)

::

   >>> import sttp
   >>> @sttp.ext.register()
   ... class MySpecialMatch(sttp.ext.match.Match):
   ...     class StrippedString():
   ...         def __init__(self, string):
   ...             self._string = string.lstrip().rstrip()
   ...         def __str__(self):
   ...             return self._string
   ...         def post_proc(self, string):
   ...             return self._string.lstrip().rstrip()
   ...     name  = 'special'
   ...     regex = r'\s*(?:foo|bar|baz|bat)\s*'
   ...     cast  = StrippedString
   ... 
   >>> in_template = '''m> Special "{{ speciality = special }}".'''
   >>> in_text     = '''Special "   bar ".'''
   >>> out_struct  = sttp.Parser(template = in_template).parse(in_text)
   >>> assert isinstance(out_struct['speciality'], MySpecialMatch.StrippedString)
   >>> assert str(out_struct['speciality']) == 'bar'

The type class need not be within the lexical scope of the match class as it
is here of course, you may do as you please.

I don't say the above is 100% optimal by the way,  it illustrates a use of
`post_proc` override, but you could also do this:

   >>> import sttp
   >>> class MySpecialMatch(sttp.ext.match.Match):
   ...     class StrippedString(str):
   ...         def __new__(cls, string):
   ...             return str.__new__(cls, string.lstrip().rstrip())
   ...     name  = 'special'
   ...     regex = r'\s*(?:foo|bar|baz|bat)\s*'
   ...     cast  = StrippedString

Another example would be date/time values, imagine a case where it is
necessary to interpret two or more different formats of date/time. One
solution is a to set `regex` to something that will match both, set `cast`
to `datetime.datetime` and make `post_proc` interpret the string regex match
result BEFORE calling the super class.

To post process or not to post process
--------------------------------------

Before implementing a `post_proc` method, take a moment to consider if your
use case implies a type, creating a type that adds 1 to an integer is probably
abuse, `AddOneToInteger` isn't really a new type, it is still an `int`
really, so setting `cast` to `int` and overriding `post_proc` to do that
AFTER calling the super class is fairer. For example:

   >>> import sttp
   >>> class IntPlusOne(sttp.core.matches.IntegerCoreMatch):
   ...     """Integer which adds one to the match value."""
   ...     name  = 'integer'
   ...     regex = r'\d+'
   ...     cast  = int
   ...     def post_proc(self, string):
   ...         return super().post_proc(string) + 1

That is a full implementation, though basing your class on the existing
integer match might be a slightly better idea:

   >>> import sttp
   >>> @sttp.ext.register()
   ... class IntPlusOne(sttp.core.matches.IntegerCoreMatch):
   ...     """Integer which adds one to the match value."""
   ...     name = 'int_plus_one'
   ...     def post_proc(self, string):
   ...         return super().post_proc(string) + 1
