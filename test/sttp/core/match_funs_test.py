"""Core match functions module tests."""

import re
import logging

from sttp import core


logging.getLogger('sttp').setLevel('DEBUG')


def test_re_fun_makes_regex():
    """Check re() core match function makes correct regex."""

    re_fun = core.match_funs.ReCoreMatchFun(r'foo (?P<middle>\S+) baz')

    assert re_fun.regex == r'foo (?P<middle>\S+) baz'


def test_fixedwidth_fun_correct_capture_and_strip():
    """Check re() core match function makes correct regex."""

    fixedwidth_fun = core.match_funs.FixedWidthColumnCoreMatchFun(10)

    assert fixedwidth_fun.post_proc(re.compile(fixedwidth_fun.regex).match('abc       ').group(0)) == 'abc'
    assert fixedwidth_fun.post_proc(re.compile(fixedwidth_fun.regex).match('    abc       ').group(0)) == 'abc'
    assert fixedwidth_fun.post_proc(re.compile(fixedwidth_fun.regex).match(' abc     x ').group(0)) == 'abc     x'
    assert fixedwidth_fun.post_proc(re.compile(fixedwidth_fun.regex).match(' abc    x      ').group(0)) == 'abc    x'
    assert fixedwidth_fun.post_proc(re.compile(fixedwidth_fun.regex).match(' abc      x ').group(0)) == 'abc'


def test_fixedwidth_fun_correct_capture_no_strip():
    """Check re() core match function makes correct regex."""

    fixedwidth_fun = core.match_funs.FixedWidthColumnCoreMatchFun(10, strip=False)

    assert fixedwidth_fun.post_proc(re.compile(fixedwidth_fun.regex).match('abc       ').group(0)) == 'abc       '
    assert fixedwidth_fun.post_proc(re.compile(fixedwidth_fun.regex).match('    abc       ').group(0)) == '    abc   '
    assert fixedwidth_fun.post_proc(re.compile(fixedwidth_fun.regex).match(' abc     x ').group(0)) == ' abc     x'
    assert fixedwidth_fun.post_proc(re.compile(fixedwidth_fun.regex).match(' abc    x      ').group(0)) == ' abc    x '
    assert fixedwidth_fun.post_proc(re.compile(fixedwidth_fun.regex).match(' abc      x ').group(0)) == ' abc      '
