"""
This modules reads .ini configuration file and returns a nested dictionnary structure.

"""

try:
    from ConfigParser import SafeConfigParser as ConfigParser
except ImportError:
    from configparser import ConfigParser
from collections import OrderedDict

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import ast

from . import py3


def from_path(path, *args, **kwargs):
    """Reads file from path and returns configuration """
    with open(path) as fp:
        config = from_fp(fp, *args, **kwargs)
    return config


def from_string(string, *args, **kwargs):
    fp = StringIO()
    fp.write(string)
    fp.seek(0)
    return from_fp(fp, *args, **kwargs)


def from_fp(fp, *args, **kwargs):
    config = ConfigParser()
    if py3:
        read_file = config.read_file
    else:
        read_file = config.readfp
    read_file(fp, *args, **kwargs)
    return process_config(config)


def process_config(config):
    section_names = sorted(config.sections())

    def items():
        for section_name in section_names:
            yield section_name, {
                opt_name: opt_value
                for opt_name, opt_value in process_section(config, section_name)
            }

    return OrderedDict(items())


def process_section(conf, section_name, **kwargs):
    for optname, value in conf.items(section_name):
        yield process_item(optname, value, **kwargs)


def process_item(optname, value, sep="\n"):
    if sep in value:
        return optname, [process_string(x.strip()) for x in value.split(sep)]
    return optname, process_string(value)


def process_string(s):
    try:
        return ast.literal_eval(s)
    except Exception:
        return s
