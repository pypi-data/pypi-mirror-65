import argparse

from dodo_commands import (CommandError, DecoratorScope, Dodo,
                           remove_trailing_dashes)
from dodo_commands.framework.global_config import (global_config_get,
                                                   load_global_config_parser)

from dodo_docker_commands.decorators.docker import invert_path


def _args():
    Dodo.parser.description = 'Runs nps'
    Dodo.parser.add_argument('--cat', action="store_true")
    Dodo.parser.add_argument('--edit', action="store_true")
    Dodo.parser.add_argument('nps_args', nargs=argparse.REMAINDER)

    args = Dodo.parse_args()
    args.cwd = Dodo.get_config('/NODE/cwd')
    args.nps = Dodo.get_config('/NODE/nps', 'nps')

    global_config = load_global_config_parser()
    args.editor = global_config_get(global_config, "settings", "editor")

    # Raise an error if something is not right
    if False:
        raise CommandError('Oops')

    return args


# Use safe=False if the script makes changes other than through Dodo.run
if Dodo.is_main(__name__, safe=True):
    args = _args()

    if args.cat:
        Dodo.run(['cat', "package-scripts.js"], cwd=args.cwd)
    elif args.edit:
        with DecoratorScope("docker", remove=True):
            Dodo.run([args.editor, "package-scripts.js"],
                     cwd=invert_path(args.cwd))
    else:
        Dodo.run([args.nps, *remove_trailing_dashes(args.nps_args)],
                 cwd=args.cwd)
