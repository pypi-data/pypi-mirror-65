from argparse import REMAINDER

from dodo_commands import Dodo, remove_trailing_dashes


def _args():
    Dodo.parser.add_argument('--cov', action='store_true')
    Dodo.parser.add_argument('pytest_args', nargs=REMAINDER)
    args = Dodo.parse_args()
    args.no_capture = not Dodo.get_config("/PYTEST/capture", True)
    args.reuse_db = Dodo.get_config("/PYTEST/reuse_db", False)
    args.html_report = Dodo.get_config("/PYTEST/html_report", None)
    args.test_file = Dodo.get_config("/PYTEST/test_file", None)
    args.pytest_ini_filename = Dodo.get_config("/PYTEST/pytest_ini", None)
    args.maxfail = Dodo.get_config("/PYTEST/maxfail", None)
    args.pytest = Dodo.get_config("/PYTEST/pytest", "pytest")
    args.coverage_dirs = Dodo.get_config("/PYTEST/coverage_dirs", [])
    args.cwd = Dodo.get_config("/PYTEST/cwd", Dodo.get_config("/ROOT/src_dir"))
    return args


def _cov_args(args):
    cov_args = ["--cov=%s" % x for x in args.coverage_dirs]
    cov_args.extend(['--cov-report', 'html:/opt/pincamp/website/cov_html'])
    cov_args.extend(
        ['--cov-report', 'annotate:/opt/pincamp/website/cov_annotate'])
    return cov_args if args.cov else ['--no-cov'] if args.coverage_dirs else []


if Dodo.is_main(__name__):
    args = _args()

    run_args = [
        *(args.pytest if isinstance(args.pytest, list) else [args.pytest]),
        *([args.test_file] if args.test_file else []),
        *_cov_args(args),
        *(["--capture", "no"] if args.no_capture else []),
        *(["--reuse-db"] if args.reuse_db else []),
        *(["-c", args.pytest_ini_filename]
          if args.pytest_ini_filename else []),
        *(["--maxfail", str(args.maxfail)] if args.maxfail else []),
        *(["--html", args.html_report] if args.html_report else []),
    ]

    Dodo.run(remove_trailing_dashes(run_args), cwd=args.cwd)
