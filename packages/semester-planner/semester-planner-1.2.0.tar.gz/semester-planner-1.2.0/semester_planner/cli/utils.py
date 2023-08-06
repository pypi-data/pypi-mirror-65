import argparse
import os


def _process_args(args: argparse.Namespace):
    if args.semester is None and args.command != 'config':
        for file in os.listdir(os.getcwd()):
            if os.path.isfile(file):
                file_name, ext = os.path.splitext(file)
                if 'semester' in file_name and ext == '.json':
                    args.semester = os.path.join(os.getcwd(), file)
                    break
        else:
            raise FileNotFoundError("Cannot find semester configuration file")


def _setup_todoist_argparse(subparsers: argparse._SubParsersAction):
    todoist_parser = subparsers.add_parser('todoist')
    todoist_parser.add_argument(
        '-t', '--token',
        help='Todoist token.'
    )
    todoist_parser.add_argument(
        '-r', '--root-project',
        help='root project to setup.',
        required=False
    )
    todoist_parser.add_argument(
        '-le', '--lectures',
        help='setup lectures at Todoist.',
        action='store_true'
    )
    todoist_parser.add_argument(
        '-la', '--labs',
        help='setup labs at Todoist.',
        action='store_true'
    )
    todoist_parser.add_argument(
        '-pr', '--practical',
        help='setup practical at Todoist.',
        action='store_true'
    )
    todoist_parser.add_argument(
        '-a', '--all',
        help='setup all at Todoist.',
        action='store_true'
    )
    todoist_parser.add_argument(
        '-o', '--override',
        help='override existing projects.',
        action='store_true'
    )


def _setup_config_argparse(subparsers: argparse._SubParsersAction):
    config_parser = subparsers.add_parser('config')

    config_subparsers = config_parser.add_subparsers(dest='config_section')

    config_todoist_parser = config_subparsers.add_parser('todoist')
    config_todoist_parser.add_argument(
        '-t', '--token',
        help='Todoist token.',
        required=False
    )
    config_todoist_parser.add_argument(
        '-r', '--root',
        help='root project to setup.',
        required=False
    )

    config_parser.add_argument(
        '-l', '--list',
        help='list configurations.',
        action='store_true'
    )


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s', '--semester',
        help='file with semester configurations',
        required=False
    )

    subparsers = parser.add_subparsers(dest='command')
    _setup_todoist_argparse(subparsers)
    _setup_config_argparse(subparsers)

    args = parser.parse_args()
    _process_args(args)
    return args
