"""
Utilities
"""

import json


def _parse_arg_val(arg_val):
    if len(arg_val) > 1:
        val = ' '.join(arg_val)
    elif len(arg_val) == 0:
        val = 1
    else:  # len(arg_val) == 1
        try:
            val = int(arg_val[0])
        except ValueError:
            try:
                val = float(arg_val[0])
            except ValueError:
                val = arg_val[0]

    return val


def command_line_args_to_json(cmd_args):
    """
    Convert command line args to JSON.
    >>> command_line_args_to_json(['python', 'main.py', 'model.pkl', '--flag', '--dataset', 'trec', '-u', '1', '-t', '1.23'])
    '{"program": "python", "main": "main.py", "arg2": "model.pkl", "flag": 1, "dataset": "trec", "u": 1, "t": 1.23}'
    """
    d = {}
    if len(cmd_args) < 2:
        raise ValueError('Too few arguments')

    d['program'] = cmd_args[0]
    d['main'] = cmd_args[1]

    # parse positional arguments
    i = 2
    while i < len(cmd_args) and not cmd_args[i].startswith('-'):
        d['arg{}'.format(i)] = cmd_args[i]
        i += 1

    # parse keyword arguments / flags
    arg_name = None
    arg_val = []

    while i < len(cmd_args):
        if cmd_args[i].startswith('-'):
            if arg_name is not None:
                d[arg_name] = _parse_arg_val(arg_val)
                arg_val = []

            arg_name = cmd_args[i].lstrip('-').replace('-', '_')
        else:
            arg_val.append(cmd_args[i])

        i += 1

    d[arg_name] = _parse_arg_val(arg_val)

    return json.dumps(d)


def extractor(fh, pattern):
    """
    Extract named groups from last line that matches some regular expression
    """
    candidate_lines = []
    for line in fh:
        if pattern.match(line):
            candidate_lines.append(line)

    line = candidate_lines[-1]
    match = pattern.match(line)
    groupdict = match.groupdict()

    for k, v in groupdict.items():
        try:
            typed_val = float(v)
            groupdict[k] = typed_val
        except ValueError:
            pass

    return json.dumps(groupdict)
