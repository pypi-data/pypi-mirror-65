"""Contains interfaces for package tools executor."""
import os
import shutil
import site
from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import IO
from punish.style import AbstractStyle
from termcolor import colored

NEW_LINE: str = "\n"


def _write_to_file(path: str, content: str, mode: str = "a") -> None:
    with open(path, mode) as file:  # type: IO[str]
        file.write(content)


@dataclass
class User(AbstractStyle):
    name: str
    email: str


class Package(AbstractStyle):
    @abstractmethod
    def init(self) -> None:
        pass


class MainPackage(Package):
    def __init__(self, name: str, user: User) -> None:
        self._name: str = name
        self._user: User = user

    def init(self) -> None:
        os.mkdir(self._name)
        _write_to_file(
            path=os.path.join(self._name, "__init__.py"),
            content=(
                f'"""Package contains a set of interfaces to operate `{self._name}` application.""" {NEW_LINE * 2}'
                f'__author__: str = "{self._user.name}"{NEW_LINE}__email__: str ='
                f' "{self._user.email}"{NEW_LINE}__version__: str = "0.0.0"{NEW_LINE}'
            ),
        )

    def make_as_tool(self) -> None:
        _write_to_file(
            path=os.path.join(self._name, "__main__.py"),
            content=(
                f'"""Represents executable entrypoint for `{self._name}` application."""'
                f'{NEW_LINE * 2}def main() -> None:{NEW_LINE}    """Runs `{self._name}` command line tool."""'
                f'{NEW_LINE * 2}    pass{NEW_LINE}'
                f'if __name__ == "__main__":{NEW_LINE}    pass{NEW_LINE}'
            ),
        )


class Tests(Package):
    def __init__(self, name: str) -> None:
        self._name: str = name
        self._tests: str = self.__class__.__name__.lower()

    def init(self) -> None:
        os.mkdir(self._tests)
        _write_to_file(
            path=os.path.join(self._tests, "__init__.py"),
            content=f'"""Package contains a set of interfaces to test `{self._name}` application."""{NEW_LINE}',
        )

    def make_helpers(self) -> None:
        _write_to_file(
            path=os.path.join(self._tests, "markers.py"),
            content=(
                f"import _pytest.mark{NEW_LINE}import pytest{NEW_LINE * 2}"
                f"unit: _pytest.mark.MarkDecorator = pytest.mark.unit{NEW_LINE}"
            ),
        )
        _write_to_file(
            path=os.path.join(self._tests, "conftest.py"),
            content=(
                f"from _pytest.config.argparsing import Parser{NEW_LINE}"
                f"from _pytest.fixtures import SubRequest{NEW_LINE}import pytest{NEW_LINE}"
            ),
        )
        _write_to_file(
            path=os.path.join(self._tests, "test_sample.py"),
            content=f"import pytest{NEW_LINE * 3}" f"def test_me() -> None:{NEW_LINE}    assert True{NEW_LINE}",
        )


class Static(Enum):
    ICON: str = "icon.png"
    GITIGNORE: str = ".gitignore"
    FLAKE: str = ".flake8"
    PYDOC: str = ".pydocstyle"
    PYLINT: str = ".pylintrc"
    MYPY: str = "mypy.ini"
    BLACK: str = "pyproject.toml"
    PYPIRC: str = ".pypirc"
    TRAVIS: str = ".travis.yml"
    REQUIREMENTS: str = "requirements.txt"
    DEV_REQUIREMENTS: str = "requirements-dev.txt"
    PYTEST: str = "pytest.ini"
    README: str = "README.md"
    LICENSE: str = "LICENSE.md"
    ANALYSER: str = "analyse-source-code.sh"
    SETUP: str = "setup.py"


class Project(AbstractStyle):
    SITE: str = os.path.join(site.getsitepackages()[0], os.path.dirname(__file__))

    def __init__(self, name: str, user: User) -> None:
        self._package: MainPackage = MainPackage(name, user)
        self._tests: Tests = Tests(name)

    def construct_package(self) -> None:
        self._package.init()
        self._package.make_as_tool()

    def construct_tests(self) -> None:
        self._tests.init()
        self._tests.make_helpers()

    def construct_meta(self) -> None:
        for file in Static:  # type: Static
            shutil.copyfile(os.path.join(self.SITE, file.value), file.value)


def easypan() -> None:
    """Runs `pypan` command line tool."""
    project = Project(
        name=input(colored(">>> Please name your application (e.g bomber): ", "green")).lower(),
        user=User(
            name=input(colored(">>> Please enter your username (e.g John Udot): ", "green")),
            email=input(colored(">>> Please enter your email (e.g user@gmail.com): ", "green")),
        ),
    )
    project.construct_package()
    project.construct_tests()
    project.construct_meta()


if __name__ == "__main__":
    easypan()
