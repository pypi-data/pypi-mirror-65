"""
Test the helper functions in makefile2dot.
"""
from makefile2dot import _line_emitter, _dependency_emitter, _trio


def test_empty():
    '''
    Empty line should just return empty.
    '''
    assert list(_line_emitter([''])) == ['']


def test_multiple_empty():
    '''
    Consecutive empty lines should all just be returned empty.
    '''
    assert list(_line_emitter(['', ''])) == ['', '']


def test_normal():
    '''
    Normal lines should just be returned verbatim.
    '''
    assert list(_line_emitter(['a', 'b'])) == ['a', 'b']


def test_multiline():
    '''
    Append any lines that follow a terminating backslash.
    '''
    assert list(_line_emitter(['a\\', 'b', 'c'])) == ['ab', 'c']


def test_dep_emit_empty():
    '''
    Empty line has no dependencies.
    '''
    assert list(_dependency_emitter(_line_emitter(['']))) == []


def test_dep_emit_singledep():
    '''
    A word following by a colon is a dependency.
    '''
    line = ['macro', 'out:dep1\\', ' dep2', '\tcommand']
    expected = [('out', 'dep1 dep2')]
    assert list(_dependency_emitter(_line_emitter(line))) == expected


def test_dep_emit_multidep():
    '''
    Multiple dependencies should still work out fine.
    '''
    line = ['macro', 'out:dep1\\', ' dep2', '\tcommand', 'out2:dep3\\',
            ' dep4', '\tcommand2']
    expected = [('out', 'dep1 dep2'), ('out2', 'dep3 dep4')]
    assert list(_dependency_emitter(_line_emitter(line))) == expected


def test_dep_emit_nodeps():
    '''
    Should still return the target.
    '''
    line = ['default:', '', '']
    assert list(_dependency_emitter(_line_emitter(line))) == [('default', '')]


def test_dot_emitter():
    '''
    Makefile outputs a dot graph.
    '''
    line = ['macro', 'out:dep1\\', ' dep2', '\tcommand', '', 'out2:dep3\\',
            ' dep4', '\tcommand2']
    expected = ['\t"out"\n', '\t"dep1" -> "out"\n', '\t"dep2" -> "out"\n',
                '\t"out2"\n', '\t"dep3" -> "out2"\n', '\t"dep4" -> "out2"\n']
    assert list(_trio(line)) == expected


def test_dot_emitter_2():
    '''
    Single node draws a very simple dot graph.
    '''
    line = ['default:', '\techo']
    expected = ['\t"default"\n']
    assert list(_trio(line)) == expected
