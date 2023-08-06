# tiramisu-cmdline-parser

Python3 parser for command-line options and arguments using Tiramisu engine.

# example

Let us start with a simple example

```python
#!/usr/bin/env python3

from tiramisu_cmdline_parser import TiramisuCmdlineParser
from tiramisu import IntOption, StrOption, BoolOption, ChoiceOption, \
                     SymLinkOption, OptionDescription, Config
# build a Config with:
# * a choice for select a sub argument (str, list, int)
choiceoption = ChoiceOption('cmd',
                            'choice the sub argument',
                            ('str', 'list', 'int'),
                            properties=('mandatory',
                                        'positional'))
# * a boolean to pass script in verbosity mode with argument -v --verbosity
booloption = BoolOption('verbosity',
                        'increase output verbosity',
                        default=False)
short_booloption = SymLinkOption('v', booloption)
# * a string option if cmd is 'str'
str_ = StrOption('str',
                 'string option',
                 properties=('mandatory',),
                 requires=[{'option': choiceoption,
                            'expected': 'str',
                            'action': 'disabled',
                            'inverse': True}])
# * a list of strings option if cmd is 'list'
list_ = StrOption('list',
                  'list string option',
                  multi=True,
                  properties=('mandatory',),
                  requires=[{'option': choiceoption,
                             'expected': 'list',
                             'action': 'disabled',
                             'inverse': True}])
# * an integer option if cmd is 'int'
int_ = IntOption('int',
                 'int option',
                 properties=('mandatory',),
                 requires=[{'option': choiceoption,
                            'expected': 'int',
                            'action': 'disabled',
                            'inverse': True}])
# Now build Config
config = Config(OptionDescription('root',
                                  'root',
                                  [choiceoption,
                                   booloption,
                                   short_booloption,
                                   str_,
                                   list_,
                                   int_
                                   ]))
# initialise the parser
config.property.read_write()
parser = TiramisuCmdlineParser(config)
# parse arguments of current script
parser.parse_args()
# now, print the result
print('result:')
config.property.read_only()
for key, value in config.value.dict().items():
    print('- {} ({}): {}'.format(key,
                                 config.option(key).option.doc(),
                                 value))
```

Let's print help:

```bash
[gnunux@localhost tiramisu-parser]$ python3 prog.py str -h
usage: prog.py [-h] [-v] --str STR --list LIST [LIST ...] --int INT
               {str,list,int}

positional arguments:
  {str,list,int}        choice the sub argument

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbosity       increase output verbosity
  --str STR             string option
  --list LIST [LIST ...]
                        list string option
  --int INT             int option
```

The positional argument 'cmd' is mandatory:

```bash
[gnunux@localhost tiramisu-parser]$ python3 prog.py
usage: prog.py [-h] [-v] --str STR --list LIST [LIST ...] --int INT
               {str,list,int}
prog.py: error: the following arguments are required: cmd
```

If 'cmd' is 'str', --str become mandatory:

```bash
[gnunux@localhost tiramisu-parser]$ python3 prog.py str
usage: prog.py [-h] [-v] --str STR --list LIST [LIST ...] --int INT
               {str,list,int}
prog.py: error: the following arguments are required: --str
```

If 'cmd' is 'str', cannot set --int argument:

```bash
[gnunux@localhost tiramisu-parser]$ python3 prog.py str --int 3
usage: prog.py [-h] [-v] --str STR --list LIST [LIST ...] --int INT
               {str,list,int}
prog.py: error: unrecognized arguments: --int
```

With all mandatories arguments:

```bash
[gnunux@localhost tiramisu-parser]$ python3 prog.py str --str value
result:
- cmd (choice the sub argument): str
- verbosity (increase output verbosity): False
- v (increase output verbosity): False
- str (string option): value
```

```bash
[gnunux@localhost tiramisu-parser]$ python3 prog.py int --int 3
result:
- cmd (choice the sub argument): int
- verbosity (increase output verbosity): False
- v (increase output verbosity): False
- int (int option): 3
```

```bash
[gnunux@localhost tiramisu-parser]$ python3 prog.py list --list a b c
result:
- cmd (choice the sub argument): list
- verbosity (increase output verbosity): False
- v (increase output verbosity): False
- list (list string option): ['a', 'b', 'c']
```

Add --verbosity argument:

```bash
[gnunux@localhost tiramisu-parser]$ python3 prog.py list --list a b c -v
result:
- cmd (choice the sub argument): list
- verbosity (increase output verbosity): True
- v (increase output verbosity): True
- list (list string option): ['a', 'b', 'c']
[gnunux@localhost tiramisu-parser]$ python3 prog.py list --list a b c --verbosity
result:
- cmd (choice the sub argument): list
- verbosity (increase output verbosity): True
- v (increase output verbosity): True
- list (list string option): ['a', 'b', 'c']
```
