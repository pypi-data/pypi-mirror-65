"""
Define the needed functions.
"""

from sys import stdin, stdout, stderr
import re


def _line_emitter(input_stream):
    """
    Emit all lines, concatenating anything that ends with a backslash.

    Even comments ending with a training backsash continue on th enext line.
    """
    line_to_emit = ''

    for line in input_stream:
        if line.endswith('\\'):
            line_to_emit += line[:-1]
        else:
            line_to_emit += line
            yield line_to_emit
            line_to_emit = ''


def _dependency_emitter(lines):
    """
    Emit a list of dependencies for each target.

    This means skipping any lines that are:
      1. empty
      2. contain comments
      3. begin with a tab (that means its a recipe)
      4. contain an equal sign (that means its an assignment)
      5. contain a question mark (that is also bad)
    """

    colon = re.compile(':')

    for line in lines:
        # Skip empty lines.
        if not line:
            continue

        # Skip comments.
        if line in ['#']:
            continue

        # Skip assignments.
        if line in ['=']:
            continue

        # Skip recipes.
        if line in ['\t']:
            continue

        # Skip ?.
        if line.find('?') > 0:
            continue

        # Skip targets with no dependencies.
        parts = colon.split(line)
        if len(parts) == 1:
            continue
        elif len(parts) == 2:
            if not parts[1] or parts[1][0] != '=':
                yield tuple(parts)
        else:
            print(stderr, 'more then one ":" not yet implemented ;)\n')
            print(stderr, 'got the following:\n%s' % parts)


def _single_dot_dep_emitter(out_deps_pairs):
    """
    Emit a `dot` language command to draw the dependency in GraphViz.
    """
    whitespace = re.compile('[ \t]+')
    ignore_deps = []
    for outs_str, deps_str in out_deps_pairs:
        if outs_str == ".PHONY":
            ignore_deps.append(deps_str.strip())
            continue

        if outs_str in ignore_deps:
            continue

        for out in whitespace.split(outs_str.strip()):
            yield '\t"%s"\n' % out
            deps = whitespace.split(deps_str.strip())
            for dep in deps:
                if dep:
                    if dep[0] == '#':
                        break
                    yield '\t"%s" -> "%s"\n' % (dep, out)


def _trio(line):
    """
    Compose _single_dot_dep_emitter to _dependency_emitter to _line_emitter.
    """
    return _single_dot_dep_emitter(_dependency_emitter(_line_emitter(line)))


def makefile2dot(**kwargs):
    """
    Visalize a Makefile as a Graphviz graph.
    """

    direction = kwargs.get('direction', "BT")
    if direction not in ["LR", "RL", "BT", "TB"]:
        raise ValueError('direction must be one of "BT", "TB", "LR", RL"')

    shape = kwargs.get('shape', "box")
    if shape not in ["box", "ellipse", "polygon"]:
        raise ValueError('shape must be one on "box", "ellipse", "polygon"')

    stdout.write('digraph G {\n')
    stdout.write('\trankdir="' + direction + '"\n')
    stdout.write('\tnode [shape="' + shape + '"]\n')
    for line in _trio(''.join(stdin).split('\n')):
        stdout.write(line)
    stdout.write('}\n')
