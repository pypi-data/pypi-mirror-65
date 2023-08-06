from argparse import REMAINDER

from dodo_commands import Dodo, remove_trailing_dashes


def _args():
    Dodo.parser.add_argument('script')
    Dodo.parser.add_argument('script_args', nargs=REMAINDER)
    args = Dodo.parse_args()
    args.python = Dodo.get_config('/PYTHON/python')
    args.cwd = Dodo.get_config('/PYTHON/cwd')
    return args


if Dodo.is_main(__name__):
    args = _args()
    Dodo.run([
        args.python,
        args.script,
    ] + remove_trailing_dashes(args.script_args),
             cwd=args.cwd)
