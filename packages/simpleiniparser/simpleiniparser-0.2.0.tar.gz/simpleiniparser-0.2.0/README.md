Does the boring stuff for you as long as you behave like a conscenting adult.

```python

  >>> config = """
  ... [SECTION]
  ... intvalue=2
  ... floatvalue=7.8
  ... stringvalue=some_value
  ... cr_list = item1
  ...           item2
  ... boolean=False
  ... comma_list_s='abc','def'
  ... comma_list_i=1,2,3
  ... comma_list_f=1.0,2.5,3
  ... """
  ...

  >>> from simpleiniparser.simple_iniconfig_parser import from_string
  >>> config = from_string(config)

  >>> config['SECTION']['floatvalue']
  7.8
  >>> config['SECTION']['cr_list']
  ['item1', 'item2']

"""

```
