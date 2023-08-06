# Commands
Extra small zero-dependency management commands library for python apps

# Installation
`pip3 install commands`

# Example
```python
import os

from management_commands import Command, main


class Ls(Command):
    def add_arguments(self, parser):
        parser.add_argument('-1', action='store_true', dest='onecol')
        parser.add_argument('path')

    def handle(self, onecol, path, **kwargs) -> None:
        sep = ', '

        if onecol:
            sep = '\n'

        print(sep.join(os.listdir(path)))


if __name__ == '__main__':
    main(commands=[Ls()])
```
