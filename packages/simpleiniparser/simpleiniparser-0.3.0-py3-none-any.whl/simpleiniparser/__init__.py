import sys

py3 = sys.version_info[0] == 3
from .simple_iniconfig_parser import from_string, from_fp, from_path
