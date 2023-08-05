"""
Test the helper functions in makefile2dot.
"""
from makefile2dot import _line_emitter, _dependency_emitter, _trio


def test_empty():
    '''
    Line emitter should return empty for empty line input.
    '''
    assert list(_line_emitter([''])) == ['']


def test_multiple_empty():
    '''
    Line emitter should return same number of empties as input.
    '''
    assert list(_line_emitter(['', ''])) == ['', '']


def test_same_list():
    '''
    Should be the same.
    '''
    assert list(_line_emitter(['a', 'b'])) == ['a', 'b']


def test_what():
    '''
    I don't undertand this test but I'm keeping it.
    '''
    assert list(_line_emitter(['a\\', 'b', 'c'])) == ['ab', 'c']


def test_dep_emit():
    '''
    What is this for?
    '''
    assert list(_dependency_emitter(_line_emitter(['']))) == []


def test_this_one():
    '''
    Some day I'll get it.
    '''
    line = ['macro', 'out:dep1\\', ' dep2', '\tcommand']
    expected = [('out', 'dep1 dep2')]
    assert list(_dependency_emitter(_line_emitter(line))) == expected


def test_another_one():
    '''
    Wanting to know.
    '''
    line = ['macro', 'out:dep1\\', ' dep2', '\tcommand', 'out2:dep3\\',
            ' dep4', '\tcommand2']
    expected = [('out', 'dep1 dep2'), ('out2', 'dep3 dep4')]
    assert list(_dependency_emitter(_line_emitter(line))) == expected


def test_more_still():
    '''
    Docstring.
    '''
    line = ['default:', '', '']
    assert list(_dependency_emitter(_line_emitter(line))) == [('default', '')]


def test_another():
    '''
    Docs
    '''
    line = ['macro', 'out:dep1\\', ' dep2', '\tcommand', '', 'out2:dep3\\',
            ' dep4', '\tcommand2']
    expected = ['\t"out"\n', '\t"dep1" -> "out"\n', '\t"dep2" -> "out"\n',
                '\t"out2"\n', '\t"dep3" -> "out2"\n', '\t"dep4" -> "out2"\n']
    assert list(_trio(line)) == expected


def test_ing():
    '''
    Docs
    '''
    line = ['default:', '\techo']
    expected = ['\t"default"\n']
    assert list(_trio(line)) == expected
