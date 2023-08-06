import argparse
import logging
import sys

from . import command, procfile, __version__


logger = logging.getLogger(__package__)


def add_query_parser(parent):
    parser = parent.add_parser('query')
    parser.add_argument(
        '-f', '--file-list',
        default='stat,cmdline',
        type=lambda s: s.split(','),
        help=f'''
            PID proc files to read. By default: %(default)s.
            Available: {','.join(procfile.registry.keys())}.
        ''',
    )
    parser.add_argument(
        '-d', '--delimiter',
        help='Join query result using given delimiter',
    )
    parser.add_argument(
        '-i', '--indent',
        type=int,
        help='Format result JSON using given indent number',
    )
    parser.add_argument(
        'query',
        nargs='?',
        help='''
            JSONPath expression, for example this query returns
            PIDs for process subtree including the given root's:

            $..children[?(@.stat.pid == 2610)]..pid
        '''
    )
    parser.set_defaults(output_file=sys.stdout)


def add_record_parser(parent):
    parser = parent.add_parser('record')
    parser.add_argument(
        '-f', '--file-list',
        default='stat,cmdline',
        type=lambda s: s.split(','),
        help=f'''
            PID proc files to read. By default: %(default)s.
            Available: {','.join(procfile.registry.keys())}.
        ''',
    )
    parser.add_argument(
        '-e', '--environment',
        action='append',
        type=lambda s: s.split('=', 1),
        help='Commands to evaluate in the shell and template the query, like VAR=date',
    )
    parser.add_argument(
        '-i', '--interval',
        type=float,
        default='10',
        help='Interval in second between each recording, %(default)s by default.',
    )
    parser.add_argument(
        '-r', '--recnum',
        type=int,
        help='''
            Number of recordings to take at --interval seconds apart.
            If not specified, recordings will be taken indefinitely.
        ''',
    )
    parser.add_argument(
        '-v', '--reevalnum',
        type=int,
        help='''
            Number of recordings after which environment must be re-evaluate.
            It's useful when you expect it to change in while recordings are
            taken.
        ''',
    )
    parser.add_argument(
        '-d', '--database-file',
        required=True,
        help='Path to the recording database file',
    )
    parser.add_argument(
        'query',
        nargs='?',
        help='''
            JSONPath expression, for example this query returns
            a node including its subtree for given PID:

            $..children[?(@.stat.pid == 2610)]
        '''
    )


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version=__version__)

    parent = parser.add_subparsers(dest='command')
    [fn(parent) for fn in (add_query_parser, add_record_parser)]

    return parser


def main():
    logging.basicConfig(level=logging.WARNING)

    parser = build_parser()
    kwargs = vars(parser.parse_args())
    # "required" keyword argument to add_subparsers() was added in py37
    if not kwargs.get('command'):
        parser.error('the following arguments are required: command')

    try:
        getattr(command, kwargs.pop('command'))(**kwargs)
    except KeyboardInterrupt:
        pass
    except command.CommandError as ex:
        logger.error(ex)
