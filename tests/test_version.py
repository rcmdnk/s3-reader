from pathlib import Path

import pytest
from git import Repo
from git.exc import InvalidGitRepositoryError

from s3_reader import __version__


def test_version():
    try:
        import tomllib
    except ModuleNotFoundError:
        import tomli as tomllib

    with open(Path(__file__).parents[1] / "pyproject.toml", "rb") as f:
        version = tomllib.load(f)["project"]["version"]
    assert version == __version__


def test_tag():
    try:
        repo = Repo(Path(__file__).parents[1])
    except InvalidGitRepositoryError:
        pytest.skip("Not a git repo.")
    latest_tag = repo.tags[-1]
    assert latest_tag.name == "v" + __version__
