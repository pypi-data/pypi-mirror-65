from typing import List
import argparse

from management_commands.command import Command


def main(
        commands: List[Command],
        **kwargs,
) -> None:
    parser = argparse.ArgumentParser(**kwargs)
    subparsers = parser.add_subparsers(title='commands')

    for command_obj in commands:
        command_obj.add_subparser(subparsers)

    args = vars(parser.parse_args())

    if '___handler' not in args:
        parser.print_usage()
        parser.exit(1)

    handler = args.pop('___handler')
    handler(**args)
