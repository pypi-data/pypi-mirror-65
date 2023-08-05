try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import tempfile

from unittest import TestCase

from .utils import from_self
from .simple_iniconfig_parser import from_path, from_string, from_fp

sample_source_content = """
[SECTION]
intvalue=2
floatvalue=7.8
stringvalue=some_value
cr_list = item1
          item2
boolean=False
comma_list_s='abc','def'
comma_list_i=1,2,3
comma_list_f=1.0,2.5,3
"""


class TestFactories(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fp = fp = StringIO()
        fp.write(sample_source_content)
        fp.seek(0)
        fd = tempfile.NamedTemporaryFile(prefix="tmp_ldapconf_")
        fd.write(sample_source_content.encode("utf-8"))
        fd.seek(0)
        cls.filepath = fd.name

        cls._fd = fd

    @from_self
    def test_fatory_equaliy(self, filepath, fp):
        config_fp = from_fp(fp)
        config_string = from_string(sample_source_content)
        config_path = from_path(filepath)

        assert config_path == config_fp == config_string

    def test_data_processing_basetypes(self):
        config = from_string(sample_source_content)
        assert list(config.keys()) == ["SECTION"]
        section = config["SECTION"]

        assert section["cr_list"] == ["item1", "item2"]
        assert section["intvalue"] == 2
        assert section["floatvalue"] == 7.8

    def test_comma(self):
        section = from_string(sample_source_content)["SECTION"]
        comma = section["comma_list_s"]
        assert comma == ("abc", "def")
        comma = section["comma_list_i"]
        assert comma == (1, 2, 3)
        comma = section["comma_list_f"]
        assert comma == (1.0, 2.5, 3)

    def test_data_pocessing_lists(self):
        section = from_string(sample_source_content)["SECTION"]

        assert section["cr_list"] == [
            "item1",
            "item2",
        ]
