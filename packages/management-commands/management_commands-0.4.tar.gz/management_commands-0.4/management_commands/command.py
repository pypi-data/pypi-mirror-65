from argparse import ArgumentParser
from typing import Optional

from management_commands.utils import underscore


class Command:
    name: Optional[str] = None

    def get_command_name(self):
        """
        :return: name if specified in `self.name`, else generate from class name
        """
        if self.name is not None:
            return self.name

        return underscore(self.__class__.__name__)

    def add_subparser(self, subparsers):
        parser = subparsers.add_parser(self.get_command_name())
        self.add_arguments(parser=parser)
        parser.set_defaults(___handler=self.handle)

    def add_arguments(self, parser: ArgumentParser):
        pass

    def handle(self, **kwargs) -> None:
        raise NotImplementedError
