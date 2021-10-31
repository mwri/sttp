"""Check README examples work."""

import logging

from sttp.subst import parser, handler


logging.getLogger('sttp').setLevel('DEBUG')


def test_constructor_returns_parser():
    """Subst parser constructor returns parser object."""

    assert isinstance(parser.Parser(), parser.Parser)


def test_parse_match_returns_handler():
    """Parser.parse for match without capture returns handler object."""

    assert isinstance(parser.Parser().parse('integer'), handler.SubstHandler)


def test_parse_assignment_returns_handler():
    """Parser.parse for assignment returns handler object."""

    assert isinstance(parser.Parser().parse('foo = integer'), handler.SubstHandler)


def test_parse_handler_var_name_none_if_no_capture():
    """Parse handler var_name is `None` if no capture."""

    assert parser.Parser().parse('integer').var_name is None


def test_parse_handler_var_name_set_if_assignment():
    """Parse handler var_name is set to the variable/capture name if assignment specified."""

    assert parser.Parser().parse('foo = integer').var_name == 'foo'
    assert parser.Parser().parse('bar = integer').var_name == 'bar'


def test_parse_handler_cast_none_if_no_cast():
    """Parse handler cast is `None` if no cast."""

    assert parser.Parser().parse('foo = integer').cast is None


def test_parse_handler_cast_type_if_cast():
    """Parse handler cast is a type if cast specified."""

    assert parser.Parser().parse('str foo = integer').cast == str
    assert parser.Parser().parse('int foo = integer').cast == int
    assert parser.Parser().parse('float foo = integer').cast == float


def test_parse_handler_match_name_set_if_bareword_match():
    """Parse handler match_name is set to string name if match is a bare word."""

    assert parser.Parser().parse('foo = integer').match_name == 'integer'
    assert parser.Parser().parse('foo = wibble').match_name == 'wibble'
    assert parser.Parser().parse('foo = foobar').match_name == 'foobar'


def test_parse_handler_fun_name_set_if_function_match():
    """Parse handler fun_name is set to string name if match is a function."""

    assert parser.Parser().parse('foo = re()').fun_name == 're'
    assert parser.Parser().parse('foo = dibble()').fun_name == 'dibble'
    assert parser.Parser().parse('foo = doo()').fun_name == 'doo'


def test_parse_handler_fun_args_set_emptylist_if_function_match_noargs():
    """Parse handler fun_args is set to empty list if match is a function without args."""

    assert parser.Parser().parse('foo = re()').fun_args == []
    assert parser.Parser().parse('foo = dibble()').fun_args == []


def test_parse_handler_fun_args_listofargs_if_function_match_withargs():
    """Parse handler fun_args is set to list of args if match is a function with args."""

    assert parser.Parser().parse('foo = re(".*")').fun_args == ['.*']
    assert parser.Parser().parse('foo = dibble(4, "wibble", 3.1415)').fun_args == [4, 'wibble', 3.1415]


def test_parse_handler_pipes():
    """Parse handler pipes."""

    assert parser.Parser().parse('foo = string | rstrip()').pipes == [{'fun_name': 'rstrip', 'fun_args': []}]
    assert parser.Parser().parse('foo = string | rstrip() | lstrip()').pipes == [
        {'fun_name': 'rstrip', 'fun_args': []},
        {'fun_name': 'lstrip', 'fun_args': []},
    ]
