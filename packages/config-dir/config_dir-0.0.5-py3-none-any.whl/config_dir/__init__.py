__license__ = "Apache License 2.0"
__author__ = "jan grant <config-dir@ioctl.org>"

import os
import pathlib
import yaml


def config_dir(name=None, sub_dir=None):
    home = pathlib.Path.home() / name
    if not home.exists():
        print("Making config dir")
        home.mkdir(0o700)
    if not home.is_dir():
        raise FileExistsError("Expected a directory:", home)

    if sub_dir is None:
        return home

    sub_dir = home / sub_dir
    if not sub_dir.exists():
        print("Making config dir")
        sub_dir.mkdir(0o700)
    if not sub_dir.is_dir():
        raise FileExistsError("Expected a directory:", sub_dir)
    return sub_dir


def load_config(name=None, default={}, sub_dir=None, sub_name="config.yaml", create=True):
    conf = config_dir(name=name, sub_dir=sub_dir) / sub_name
    if not conf.exists():
        config = dict(default)
        if create:
            with os.fdopen(os.open(conf, os.O_CREAT | os.O_WRONLY, 0o600), "w") as f:
                yaml.safe_dump(config, f)
    else:
        with conf.open() as f:
            config = yaml.safe_load(f)
    return config


def load_content(name=None, default=None, sub_dir=None, sub_name="config", create=True):
    conf = config_dir(name=name, sub_dir=sub_dir) / sub_name
    if not conf.exists():
        content = default
        if create:
            with os.fdopen(os.open(conf, os.O_CREAT | os.O_WRONLY, 0o600), "w") as f:
                f.write(content)
    else:
        with conf.open() as f:
            content = f.read()
    return content


def save_config(name=None, config=None, sub_dir=None, sub_name="config.yaml"):
    conf = config_dir(name=name, sub_dir=sub_dir) / sub_name
    with os.fdopen(os.open(conf, os.O_CREAT | os.O_WRONLY, 0o600), "w") as f:
        yaml.safe_dump(config, f)


def save_content(name=None, content=None, sub_dir=None, sub_name="config"):
    conf = config_dir(name=name, sub_dir=sub_dir) / sub_name
    with os.fdopen(os.open(conf, os.O_CREAT | os.O_WRONLY, 0o600), "w") as f:
        f.write(content)
