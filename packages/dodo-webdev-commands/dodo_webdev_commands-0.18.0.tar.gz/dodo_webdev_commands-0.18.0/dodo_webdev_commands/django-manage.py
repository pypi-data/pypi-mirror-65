import argparse

from dodo_commands import Dodo, remove_trailing_dashes
from dodo_commands.framework.util import maybe_list_to_list


def _args():
    Dodo.parser.description = 'Run a django-manage command.'
    Dodo.parser.add_argument('--name', )
    Dodo.parser.add_argument('manage_args', nargs=argparse.REMAINDER)
    args = Dodo.parse_args()
    args.python = Dodo.get_config("/DJANGO/python")
    args.cwd = Dodo.get_config("/DJANGO/cwd")
    args.manage_py = Dodo.get_config("/DJANGO/manage_py", "manage.py")
    return args


if Dodo.is_main(__name__):
    args = _args()
    if args.name:
        Dodo.get_config('/DOCKER') \
            .setdefault('options', {}) \
            .setdefault('django-manage', {}) \
            .setdefault('name', args.name)

    Dodo.run([
        *maybe_list_to_list(args.python), args.manage_py,
        *remove_trailing_dashes(args.manage_args)
    ],
             cwd=args.cwd)
