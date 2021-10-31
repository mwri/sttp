.. _templating-reference:

Templating reference
====================

Prefixes
--------

These are all the permitted prefix notations:

+--------+-------------------------------------------------------------------+
| Prefix | Description                                                       |
+========+===================================================================+
| m      | :ref:`Match<std-matches>` one line.                               |
+--------+-------------------------------------------------------------------+
| m*     | :ref:`Match<std-matches>` zero or more lines.                     |
+--------+-------------------------------------------------------------------+
| m+     | :ref:`Match<std-matches>` one or more lines                       |
+--------+-------------------------------------------------------------------+
| m?     | :ref:`Match<std-matches>` zero or one lines.                      |
+--------+-------------------------------------------------------------------+
| m{n}   | :ref:`Match<std-matches>` N lines.                                |
+--------+-------------------------------------------------------------------+
| m{n,m} | :ref:`Match<std-matches>` N to M lines.                           |
+--------+-------------------------------------------------------------------+
| r      | :ref:`Regex match<re-matches>` one line.                          |
+--------+-------------------------------------------------------------------+
| r*     | :ref:`Regex match<re-matches>` zero or more lines.                |
+--------+-------------------------------------------------------------------+
| r+     | :ref:`Regex match<re-matches>` one or more lines                  |
+--------+-------------------------------------------------------------------+
| r?     | :ref:`Regex match<re-matches>` zero or one lines.                 |
+--------+-------------------------------------------------------------------+
| r{n}   | :ref:`Regex match<re-matches>` N lines.                           |
+--------+-------------------------------------------------------------------+
| r{n,m} | :ref:`Regex match<re-matches>` N to M lines.                      |
+--------+-------------------------------------------------------------------+

Any of these may be postfixed with :code:`(variable_name)` to stash a list
as a key in a dictionary instead, for example if :code:`m` resulted in a list
:code:`['foo', 'bar']` then :code:`m(wibble)` would change this to
:code:`{'wibble': ['foo', 'bar']}`.

Additionally flags may be prefixed with a slash. The only flag supported is
:code:`lax` which allows garbage before and after the match criteria. So
:code:`m> ble` or :code:`m/!lax> ble` would only match :code:`"ble"`, but
:code:`m/lax> ble` could match :code:`"wibble" or :code:`"ibbles"` as well.

Core matches
------------

These are the built in matches:

+------------+-------+---------------------------------------+
| Name       | Type  | Description                           |
+============+=======+=======================================+
| integer    | int   | An integer.                           |
+------------+-------+---------------------------------------+
| non_ws     | str   | Non white space.                      |
+------------+-------+---------------------------------------+
| word       | str   | A word (in regular expression terms). |
+------------+-------+---------------------------------------+
| ws         | str   | White space                           |
+------------+-------+---------------------------------------+
| string     | str   | Any amount of text.                   |
+------------+-------+---------------------------------------+
| hostname   | str   | An internet fqdn (hostname).          |
+------------+-------+---------------------------------------+
| ipaddr     | str   | An (IP) internet address.             |
+------------+-------+---------------------------------------+
| number     | float | An integer or floating point number.  |
+------------+-------+---------------------------------------+
| common_dt  | str   | A date time.                          |
+------------+-------+---------------------------------------+

See :ref:`custom matches<custom-matches>` if you want to add your own.

Core function matches
---------------------

These are the built in match functions:

+--------------------------+-----------------------------------------------+
| Name(parameters)         | Type  | Description                           |
+==========================+=======+=======================================+
| re(regex)                | str   | A raw regular expression.             |
+--------------------------+-------+---------------------------------------+
| fixedwidth(width, strip) | str   | A fixed width column. Strip (default  |
|                          |       | true) turns white space strip on/off. |
+--------------------------+-------+---------------------------------------+

See :ref:`match functions<fun-matches>` if you want to add your own.

Functions
---------

These are the built in (post processing, non match) functions:

+-------------------------+-----------------------------------------------+
| Name(parameters)        | Type  | Description                           |
+=========================+=======+=======================================+
| rstrip()                | str   | Strip right hand side white space.    |
+-------------------------+-------+---------------------------------------+
| lstrip()                | str   | Strip left hand side white space.     |
+-------------------------+-------+---------------------------------------+
