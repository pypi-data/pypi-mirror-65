# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Config sorting tests
"""

import os
import pytest
import configparser
from portmod.globals import env
from portmod.main import configure_mods
from portmod.repo.config import sort_config
from portmod.tsort import CycleException
from .env import setup_env, tear_down_env


@pytest.fixture(scope="module", autouse=True)
def setup():
    """
    Sets up and tears down the test environment
    """
    dictionary = setup_env("test-config")
    config = dictionary["config"]
    config_ini = dictionary["config_ini"]
    with open(env.PORTMOD_CONFIG, "w") as configfile:
        print(
            f"""
TEST_CONFIG = "{config}"
TEST_CONFIG_INI = "{config_ini}"
""",
            file=configfile,
        )
    yield dictionary
    tear_down_env()


def test_sort_config(setup):
    """
    Tests that sorting the config files works properly
    """
    # Install mods
    configure_mods(["test/test-1.0", "test/test2-1.0"], no_confirm=True)
    testdir = setup["testdir"]

    datavalue1 = '"' + os.path.join(testdir, "local", "mods", "test", "test") + '"'
    datavalue2 = '"' + os.path.join(testdir, "local", "mods", "test", "test2") + '"'
    dataentry1 = f"data={datavalue1}"
    dataentry2 = f"data={datavalue2}"
    fileentry1 = f"file=Foo"
    fileentry2 = f"file=Bar"

    # Check that config is correct
    with open(setup["config"], "r") as configfile:
        lines = list(map(lambda x: x.strip(), configfile.readlines()))
        assert dataentry1 in lines
        assert dataentry2 in lines
        assert lines.index(dataentry1) < lines.index(dataentry2)

        assert fileentry1 in lines
        assert fileentry2 in lines
        assert lines.index(fileentry1) < lines.index(fileentry2)

    ini = configparser.ConfigParser()
    ini.read(setup["config_ini"])
    assert ini["data"]["Install0"] == datavalue1
    assert ini["data"]["Install1"] == datavalue2
    assert ini["TestSection"]["testkey"] == "TestValue"
    assert ini["TestSection"]["testkey2"] == "TestValue2"
    for entry in ini["file"]:
        if ini["file"][entry] == "Foo":
            fooindex = entry
        elif ini["file"][entry] == "Bar":
            barindex = entry
    assert fooindex < barindex

    # Remove mods
    configure_mods(["test/test-1.0", "test/test2-1.0"], no_confirm=True, depclean=True)

    # Check that config is no longer contains their entries
    with open(setup["config"], "r") as configfile:
        assert not configfile.read().strip()

    ini = configparser.ConfigParser()
    ini.read(setup["config_ini"])
    assert not ini["data"]
    assert not ini["file"]
    assert not ini["TestSection"]


def test_user_override(setup):
    """
    Tests that user overrides for config sorting work properly
    """

    testdir = setup["testdir"]
    installpath = os.path.join(testdir, "config", "config", "install.csv")
    filepath = os.path.join(testdir, "config", "config", "files.csv")
    os.makedirs(os.path.dirname(installpath), exist_ok=True)

    datavalue1 = '"' + os.path.join(testdir, "local", "mods", "test", "test") + '"'
    datavalue2 = '"' + os.path.join(testdir, "local", "mods", "test", "test2") + '"'
    dataentry1 = f"data={datavalue1}"
    dataentry2 = f"data={datavalue2}"
    fileentry1 = f"file=Foo"
    fileentry2 = f"file=Baz, With Spaces"

    # Enforce that test overrides test2
    with open(installpath, "w") as file:
        print("test/test, test/test2", file=file)

    with open(filepath, "w") as file:
        print('"Baz, With Spaces", Foo', file=file)

    configure_mods(["test/test-1.0", "test/test2-1.0"], no_confirm=True)

    # Check that config is correct
    with open(setup["config"], "r") as configfile:
        lines = list(map(lambda x: x.strip(), configfile.readlines()))
        assert dataentry1 in lines
        assert dataentry2 in lines
        assert lines.index(dataentry1) > lines.index(dataentry2)

        assert fileentry1 in lines
        assert fileentry2 in lines
        assert lines.index(fileentry1) < lines.index(fileentry2)

    # Enforce that test2 overrides test
    with open(installpath, "w") as file:
        print("test/test2, test/test", file=file)

    with open(filepath, "w") as file:
        print('Foo, "Baz, With Spaces"', file=file)

    configure_mods(["test/test-1.0", "test/test2-1.0"], no_confirm=True)

    # Check that config is correct
    with open(setup["config"], "r") as configfile:
        lines = list(map(lambda x: x.strip(), configfile.readlines()))
        assert dataentry1 in lines
        assert dataentry2 in lines
        assert lines.index(dataentry1) < lines.index(dataentry2)

        assert fileentry1 in lines
        assert fileentry2 in lines
        assert lines.index(fileentry1) > lines.index(fileentry2)


def test_user_cycle(setup):
    """
    Tests that cycles introduced by the user are reported correctly
    """
    testdir = setup["testdir"]
    installpath = os.path.join(testdir, "config", "config", "install.csv")
    os.makedirs(os.path.dirname(installpath), exist_ok=True)

    # Enforce that test overrides test2
    with open(installpath, "w") as file:
        print("test/test, test/test2", file=file)
        print("test/test2, test/test", file=file)

    configure_mods(["test/test-1.0", "test/test2-1.0"], no_confirm=True)
    with pytest.raises(CycleException):
        sort_config()
