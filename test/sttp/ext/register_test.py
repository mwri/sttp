"""Registration tests module."""

import logging
import pytest

import sttp


logging.getLogger('sttp').setLevel('DEBUG')


@pytest.fixture
def cleanup():
    """Fixture to clean up registered matches and match functions."""

    yield

    if sttp.ext.match.Match.lookup('mymatch') is not None:
        del sttp.ext.match.Match._reg['mymatch']
    if sttp.ext.match_fun.MatchFun.lookup('mymatchfun') is not None:
        del sttp.ext.match_fun.MatchFun._reg['mymatchfun']


def test_register_registers_match_class(cleanup):
    """Check register registers new match."""

    assert sttp.ext.match.Match.lookup('mymatch') is None

    @sttp.ext.register()
    class MyMatch(sttp.ext.match.Match):
        name = 'mymatch'
        regex = r'(foo|bar|baz|bat)'

    assert sttp.ext.match.Match.lookup('mymatch') == MyMatch


def test_register_raises_if_match_name_clashes(cleanup):
    """Check register raises if match name already in use."""

    assert sttp.ext.match.Match.lookup('mymatch') is None

    @sttp.ext.register()
    class MyMatch(sttp.ext.match.Match):
        name = 'mymatch'
        regex = r'(foo|bar|baz|bat)'

    assert sttp.ext.match.Match.lookup('mymatch') == MyMatch

    with pytest.raises(sttp.errors.RegistrationNamingClashError):

        @sttp.ext.register()
        class MySecondMatch(sttp.ext.match.Match):
            name = 'mymatch'
            regex = r'(foo|bar|baz|bat)'


def test_register_registers_match_fun_class(cleanup):
    """Check register registers new match function."""

    assert sttp.ext.match_fun.MatchFun.lookup('mymatchfun') is None

    @sttp.ext.register()
    class MyMatchFun(sttp.ext.match_fun.MatchFun):
        name = 'mymatchfun'

        def __init__(self, regex):
            self.regex = r'(foo|bar|baz|bat)'

    assert sttp.ext.match_fun.MatchFun.lookup('mymatchfun') == MyMatchFun


def test_register_raises_if_match_fun_name_clashes(cleanup):
    """Check register raises if match function name already in use."""

    assert sttp.ext.match_fun.MatchFun.lookup('mymatchfun') is None

    @sttp.ext.register()
    class MyMatchFun(sttp.ext.match_fun.MatchFun):
        name = 'mymatchfun'

        def __init__(self, regex):
            self.regex = r'(foo|bar|baz|bat)'

    assert sttp.ext.match_fun.MatchFun.lookup('mymatchfun') == MyMatchFun

    with pytest.raises(sttp.errors.RegistrationNamingClashError):

        @sttp.ext.register()
        class MySecondMatchFun(sttp.ext.match_fun.MatchFun):
            name = 'mymatchfun'

            def __init__(self, regex):
                self.regex = r'(foo|bar|baz|bat)'
