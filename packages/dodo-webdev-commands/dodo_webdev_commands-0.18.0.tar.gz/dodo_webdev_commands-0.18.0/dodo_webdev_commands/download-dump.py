import os
from argparse import ArgumentParser

from dodo_commands import Dodo
from dodo_commands.framework.config import merge_into_config
from dodo_commands.framework.choice_picker import ChoicePicker
from dodo_ssh_agent_commands.utils import add_ssh_agent_args


def _args():
    parser = ArgumentParser()
    parser.add_argument('host')
    args = Dodo.parse_args(parser)
    return args


def _get_timestamp(fn):
    return fn.split('_')[-1]


if Dodo.is_main(__name__, safe=True):
    args = _args()
    project_name = Dodo.get_config('/ROOT/project_name')
    cmd = 'root@{host}:/srv/{projectName}/dumps'.format(
        host=args.host, projectName=project_name)
    dumps_dir = '/srv/%s/dumps' % project_name

    merge_into_config(
        Dodo.get_config('/DOCKER').setdefault('options', {}),
        {Dodo.command_name: add_ssh_agent_args({'is_interactive': False})})

    dump_fns = Dodo.run([
        'ssh',
        'root@%s' % args.host,
        'ls',
        os.path.join(dumps_dir, '*.sql'),
    ],
                        capture=True).split()

    dump_fns = sorted([x for x in dump_fns if x], key=_get_timestamp)

    class Picker(ChoicePicker):
        def print_choices(self, choices):
            for idx, dump_fn in enumerate(choices):
                print("%d: %s" % (idx + 1, dump_fn))

        def question(self):
            return 'Select files to download (e.g. 1,3-4): '

    picker = Picker()
    picker.pick(dump_fns)

    for dump_fn in picker.get_choices():
        Dodo.run(['scp', 'root@%s:%s' % (args.host, dump_fn), dump_fn])
