"""Parser class tests."""

import pytest
import logging

import sttp


logging.getLogger('sttp').setLevel('DEBUG')


def test_instantiates_parser_obj():
    """Parser constructor makes Parser object."""

    assert isinstance(sttp.Parser(template='m> foo'), sttp.Parser)


def test_parse_raises_leftoverinput_when_input_left_over():
    """Parser raises LeftoverInputError if input remains when template done."""

    parser = sttp.Parser(template='m> foo\nm> bar\n')
    with pytest.raises(sttp.errors.LeftoverInputError):
        parser.parse('foo\nbar\nbaz\n')


def test_parse_raises_nomoreinput_input_when_expected_but_no_more_input():
    """Parser raises NoMoreInputError if input consumed but more template remains."""

    parser = sttp.Parser(template='m> foo\nm> bar\n')
    with pytest.raises(sttp.errors.NoMoreInputError):
        parser.parse('foo\n')


def test_parse_returns_none_when_no_subst_cap_no_list_implied():
    """Parser returns None when no subst no captures and no list context implied."""

    parser = sttp.Parser(template='m> foo\n')
    assert parser.parse('foo\n') is None


def test_parse_returns_none_when_no_subst_no_cap_list_implied():
    """Parser returns None when no subst no captures and list context implied."""

    parser = sttp.Parser(template='m*> foo\n')
    assert parser.parse('foo\n') is None


def test_parse_returns_none_when_no_cap_no_list_implied():
    """Parser returns None when no captures and no list context implied."""

    parser = sttp.Parser(template='m> {{ re("\\S+") }}\n')
    assert parser.parse('foo\n') is None


def test_parse_returns_none_when_no_cap_list_implied():
    """Parser returns None when no captures and list context implied."""

    parser = sttp.Parser(template='m*> {{ re("\\S+") }}\n')
    assert parser.parse('foo\n') is None


def test_parse_match_multimodifier_returns_list_when_matching():
    """Parser returns a list for a match with multiple match modifiers."""

    parser = sttp.Parser(template='m*> {{ data = word }}\n')
    assert isinstance(parser.parse('foo\nfoo\n'), list)
    parser = sttp.Parser(template='m+> {{ data = word }}\n')
    assert isinstance(parser.parse('foo\n'), list)
    parser = sttp.Parser(template='m?> {{ data = word }}\n')
    assert isinstance(parser.parse('foo\n'), list)
    parser = sttp.Parser(template='m{1}> {{ data = word }}\n')
    assert isinstance(parser.parse('foo\n'), list)
    parser = sttp.Parser(template='m{3}> {{ data = word }}\n')
    assert isinstance(parser.parse('foo\nfoo\nfoo\n'), list)


def test_parse_match_single_returns_dict_when_matching():
    """Parser returns a dict for a match with no multiple match modifier."""

    parser = sttp.Parser(template='m> {{ data = word }}\n')
    assert isinstance(parser.parse('foo\n'), dict)


def test_parse_raises_when_mixed_type_modifiers_used():
    """Parser raises RunError when multiple matches with modifiers imply different return types used."""

    parser = sttp.Parser(template='m> {{ data1 = word }}\nm*> {{ data2 = word }}\n')
    with pytest.raises(sttp.errors.RunError):
        parser.parse('foo\nbar\n')
    parser = sttp.Parser(template='m{1,2}> {{ data1 = word }}\nm> {{ data2 = word }}\n')
    with pytest.raises(sttp.errors.RunError):
        parser.parse('bar\nfoo\nbaz\n')


def test_parse_match_starmodifier_matches_noneormany():
    """Parser match star modifier matches zero or more times."""

    parser = sttp.Parser(template='m*> foo\nm?> xxx\n')
    parser.parse('xxx\n')
    parser.parse('foo\nxxx\n')
    parser.parse('foo\nfoo\nxxx\n')
    parser.parse('foo\nfoo\nfoo\nxxx\n')


def test_parse_match_plusmodifier_matches_oneormany():
    """Parser match plus modifier matches one or more times."""

    parser = sttp.Parser(template='m+> foo\nm?> xxx\n')
    with pytest.raises(sttp.errors.ParseFailedError) as ex:
        parser.parse('xxx\n')
    assert 'line 1 (template line 1): no match' in str(ex)
    parser.parse('foo\nxxx\n')
    parser.parse('foo\nfoo\nxxx\n')
    parser.parse('foo\nfoo\nfoo\nxxx\n')


def test_parse_match_qmmodifier_matches_noneorone():
    """Parser match QM modifier matches zero or one times."""

    parser = sttp.Parser(template='m?> foo\nm?> xxx\n')
    parser.parse('xxx\n')
    parser.parse('foo\nxxx\n')
    with pytest.raises(sttp.errors.LeftoverInputError) as ex:
        parser.parse('foo\nfoo\nxxx\n')
    assert 'line 2: template finished' in str(ex)


def test_parse_raises_if_bad_subst():
    """Parser raises if the substitution does not parse / is invalid."""

    with pytest.raises(sttp.errors.BadTemplateError) as ex:
        sttp.Parser(template='m+> {{ wibble 9_ data1 nonsense = word }}\n')
    assert 'template line 1: substitution error' in str(ex)


def test_parse_runs_piped_function():
    """Parser runs piped function."""

    parser = sttp.Parser(template='m> {{ val = re("\\s*\\S+\\s*") | lstrip() }}\n')
    assert parser.parse(' foo   \n') == {'val': 'foo   '}


def test_parse_runs_piped_functions():
    """Parser runs multiple piped functions."""

    parser = sttp.Parser(template='m> {{ val = re("\\s*\\S+\\s*") | lstrip() | rstrip() }}\n')
    assert parser.parse(' foo   \n') == {'val': 'foo'}


def test_parse_templated_returntype_change_raises():
    """Parser raises and exception if the template data return type changes."""

    in_template = '''m> Num   Server               Uptime
m*> {{ int num = fixedwidth(6) }}{{ server = fixedwidth(21) }}{{ uptime = string }}
m> Total: {{ total = integer }}
'''

    in_text = '''Num   Server               Uptime
1     wibble.domain.com    1d 5h
2     zap.domain.com       100d 1h
3     foobar.domain.com    3d 10h
Total: 3
'''

    with pytest.raises(sttp.errors.RunError) as ex:
        parser = sttp.Parser(template=in_template)
        parser.parse(in_text)
    assert 'output merge type conflict list vs dict' in str(ex)


def test_parse_concats_mixed_list_items_if_allow_mixed_lists():
    """Parser will allow mixed schema lists if allow_mixed_lists is true."""

    in_template = '''m> Num   Server               Uptime
m*> {{ int num = fixedwidth(6) }}{{ server = fixedwidth(21) }}{{ uptime = string }}
m> Total: {{ total = integer }}
'''

    in_text = '''Num   Server               Uptime
1     wibble.domain.com    1d 5h
2     zap.domain.com       100d 1h
3     foobar.domain.com    3d 10h
Total: 3
'''

    parser = sttp.Parser(template=in_template, allow_mixed_lists=True)
    out_struct = parser.parse(in_text)

    assert out_struct == [
        {'num': 1, 'server': 'wibble.domain.com', 'uptime': '1d 5h'},
        {'num': 2, 'server': 'zap.domain.com', 'uptime': '100d 1h'},
        {'num': 3, 'server': 'foobar.domain.com', 'uptime': '3d 10h'},
        {'total': 3},
    ]


def test_match_lines_no_start_end_garbage_by_default():
    """Parser match lines require full and exact match (no garbage start or end) by default."""

    in_template = r'''m> {{ re("\S+\.\S+") }}'''
    parser = sttp.Parser(template=in_template)

    assert parser.parse('foo.bar') == None

    with pytest.raises(sttp.errors.ParseFailedError):
        parser.parse('xx foo.bar')
    with pytest.raises(sttp.errors.ParseFailedError):
        parser.parse('foo.bar yy')


def test_match_lines_no_start_end_garbage_with_not_lax_flag():
    """Parser match lines require full and exact match (no garbage start or end) when !lax flag employed."""

    in_template = r'''m/!lax> {{ re("\S+\.\S+") }}'''
    parser = sttp.Parser(template=in_template)

    assert parser.parse('foo.bar') == None

    with pytest.raises(sttp.errors.ParseFailedError):
        parser.parse('xx foo.bar')
    with pytest.raises(sttp.errors.ParseFailedError):
        parser.parse('foo.bar yy')


def test_match_lines_start_end_garbage_allowed_with_lax_flag():
    """Parser match lines match with leading or trailing garbage when lax flag employed."""

    in_template = r'''m/lax> {{ re("\S+\.\S+") }}'''
    parser = sttp.Parser(template=in_template)

    assert parser.parse('foo.bar') == None
    assert parser.parse('xx foo.bar') == None
    assert parser.parse('foo.bar yy') == None


def test_match_lines_no_start_end_garbage_by_default():
    """Parser match lines require full and exact match (no garbage start or end) by default."""

    in_template = r'''r> \S+\.\S+'''
    parser = sttp.Parser(template=in_template)

    assert parser.parse('foo.bar') == None

    with pytest.raises(sttp.errors.ParseFailedError):
        parser.parse('xx foo.bar')
    with pytest.raises(sttp.errors.ParseFailedError):
        parser.parse('foo.bar yy')


def test_match_lines_no_start_end_garbage_with_not_lax_flag():
    """Parser match lines require full and exact match (no garbage start or end) when !lax flag employed."""

    in_template = r'''r/!lax> \S+\.\S+'''
    parser = sttp.Parser(template=in_template)

    assert parser.parse('foo.bar') == None

    with pytest.raises(sttp.errors.ParseFailedError):
        parser.parse('xx foo.bar')
    with pytest.raises(sttp.errors.ParseFailedError):
        parser.parse('foo.bar yy')


def test_match_lines_start_end_garbage_allowed_with_lax_flag():
    """Parser match lines match with leading or trailing garbage when lax flag employed."""

    in_template = r'''r/lax> \S+\.\S+'''
    parser = sttp.Parser(template=in_template)

    assert parser.parse('foo.bar') == None
    assert parser.parse('xx foo.bar') == None
    assert parser.parse('foo.bar yy') == None
