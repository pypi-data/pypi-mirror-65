from argparse import ArgumentParser

from dodo_commands import CommandError, Dodo
from dodo_commands.framework.util import maybe_list_to_list


def _args():
    parser = ArgumentParser(description='Runs node')
    parser.add_argument('--inspect', action='store_true')
    parser.add_argument('--inspect-brk', action='store_true')
    parser.add_argument('--shell', action='store_true')

    args = Dodo.parse_args(parser)
    args.pwd = Dodo.get_config('/NODE/pwd')
    args.node = Dodo.get_config('/NODE/node', 'node')
    args.entrypoint = Dodo.get_config('/NODE/entrypoint', 'index.js')

    # Raise an error if something is not right
    if False:
        raise CommandError('Oops')

    return args


# Use safe=False if the script makes changes other than through Dodo.run
if Dodo.is_main(__name__, safe=True):
    args = _args()

    inspect = "inspect" if args.inspect else "inspect-brk" if args.inspect_brk else None

    extra_args = ['--%s=0.0.0.0:9229' %
                  inspect, '--no-lazy'] if inspect else []

    node_exe_args = maybe_list_to_list(args.node)
    entrypoint_args = ([]
                       if args.shell else maybe_list_to_list(args.entrypoint))

    Dodo.run([*node_exe_args, *extra_args, *entrypoint_args], cwd=args.pwd)
