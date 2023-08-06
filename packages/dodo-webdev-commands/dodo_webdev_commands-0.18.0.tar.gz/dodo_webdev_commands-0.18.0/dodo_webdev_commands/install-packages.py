import os
from argparse import ArgumentParser

from dodo_commands import CommandError, Dodo


def _args():
    parser = ArgumentParser()

    parser.add_argument(
        '--pip-requirements',
        dest='requirements_filename',
        help=
        'The pip requirements filename. If you use the value \'default\' then ${/SERVER/pip_requirements} from the configuration is used.'
    )
    parser.add_argument('--node-modules-dir', dest='node_modules_dir')

    args = Dodo.parse_args(parser)

    args.yarn = Dodo.get_config('/NODE/yarn', 'yarn')
    args.pip = Dodo.get_config('/PYTHON/pip', 'pip')

    if args.requirements_filename == 'default':
        args.requirements_filename = Dodo.get_config(
            '/SERVER/pip_requirements')

    if args.node_modules_dir == 'default':
        args.node_modules_dir = Dodo.get_config('/NODE/node_modules_dir')

    return args


if Dodo.is_main(__name__, safe=True):
    args = _args()

    if not args.requirements_filename and not args.node_modules_dir:
        raise CommandError(
            "Either --requirements-filename or --node_modules-dir is mandatory."
        )

    if args.requirements_filename:
        Dodo.run([args.pip, 'install', '-r', args.requirements_filename])
    if args.node_modules_dir:
        Dodo.run([args.yarn, 'install'],
                 cwd=os.path.abspath(os.path.join(args.node_modules_dir,
                                                  '..')))
