import os
import shutil
import site
from abc import abstractmethod
from enum import Enum
from typing import IO, Generator
from dataclasses import dataclass
from punish.style import AbstractStyle
from termcolor import colored

_SITE_PATH: str = site.getsitepackages()[0]
_new_line: str = "\n"


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
                f'"""Package contains a set of interfaces to operate `{self._name}` application.""" {_new_line * 2}'
                f'__author__: str = "{self._user.name}"{_new_line}__email__: str ='
                f' "{self._user.email}"{_new_line}__version__: str = "0.0.0"{_new_line}'
            ),
        )

    def make_as_tool(self) -> None:
        _write_to_file(
            path=os.path.join(self._name, "__main__.py"),
            content=(
                f'"""Represents executable entrypoint for `{self._name}` application."""'
                f'{_new_line * 2}if __name__ == "__main__":{_new_line}    pass{_new_line}'
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
            content=f'"""Package contains a set of interfaces to test `{self._name}` application."""{_new_line}',
        )

    def make_helpers(self) -> None:
        _write_to_file(
            path=os.path.join(self._tests, "markers.py"),
            content=(
                f"import _pytest.mark{_new_line}import pytest{_new_line * 2}"
                f"unit: _pytest.mark.MarkDecorator = pytest.mark.unit{_new_line}"
            ),
        )
        _write_to_file(
            path=os.path.join(self._tests, "conftest.py"),
            content=(
                f"from _pytest.config.argparsing import Parser{_new_line}"
                f"from _pytest.fixtures import SubRequest{_new_line}import pytest{_new_line}"
            ),
        )
        _write_to_file(
            path=os.path.join(self._tests, "test_sample.py"),
            content=f"import pytest{_new_line * 3}" f"def test_me() -> None:{_new_line}    assert True{_new_line}",
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

    # PYTEST: str = "pytest.ini"
    # README: str = "README.md"
    # LICENSE: str = "LICENSE.md"

    @classmethod
    def copy_all(cls, from_path: str = "./", to_path: str = "./") -> None:
        for file in Static:  # type: Static
            shutil.copyfile(os.path.join(from_path, file.value), os.path.join(to_path, file.value))

    @classmethod
    def requirements(cls) -> Generator["Static", None, None]:
        yield from (cls.REQUIREMENTS, cls.DEV_REQUIREMENTS)

    @classmethod
    def code_analyser(cls) -> Generator["Static", None, None]:
        yield from (cls.FLAKE, cls.PYDOC, cls.PYLINT, cls.MYPY, cls.BLACK, cls.TRAVIS)


class Project(AbstractStyle):
    def __init__(self, name: str, user: User) -> None:
        self._name = name
        self._user = user
        self._package: MainPackage = MainPackage(name, user)
        self._tests: Tests = Tests(name)

    def construct_package(self) -> None:
        self._package.init()
        self._package.make_as_tool()

    def construct_tests(self) -> None:
        self._tests.init()
        self._tests.make_helpers()

    def construct_meta(self) -> None:
        Static.copy_all(from_path=os.path.join(_SITE_PATH, os.path.dirname(__file__)))
        _write_to_file(
            path="AUTHORS.md",
            content=(
                f"Authors{_new_line}======={_new_line}{_new_line}Application is written and maintained by "
                f"**{self._user.name}** ([{self._user.email}]({self._user.email})){_new_line}"
            ),
        )
        _write_to_file(path="CHANGELOG.md", content=f"Versions{_new_line}======={_new_line}")
        _write_to_file(
            path="MANIFEST.in",
            content=(
                f"include *.txt *.ini *.cfg *.rst *.md{_new_line}recursive-include {self._name} "
                f"*.ico *.png *.css *.gif *.jpg *.pt *.txt *.mak *.mako *.js *.html *.xml *.jinja2{_new_line}"
            ),
        )


def main() -> None:
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
    main()
