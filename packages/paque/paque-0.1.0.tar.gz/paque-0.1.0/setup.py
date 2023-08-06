# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['paque']

package_data = \
{'': ['*']}

install_requires = \
['cleo>=0.8.0,<0.9.0', 'colorlog>=4.1.0,<5.0.0', 'pyyaml>=5.3,<6.0']

entry_points = \
{'console_scripts': ['paque = paque.paque:main']}

setup_kwargs = {
    'name': 'paque',
    'version': '0.1.0',
    'description': 'paque simplifies running simple workflows you want to run. It offers a few features of `make`, but removing most of its power',
    'long_description': '# Paque `¯\\_(ツ)_/¯`\n\n<!-- markdown-toc start - Don\'t edit this section. Run M-x markdown-toc-refresh-toc -->\n\n- [Paque `¯\\_(ツ)_/¯`](#paque-ツ)\n    - [Installation](#installation)\n        - [Tab completion](#tab-completion)\n    - [Why?](#why)\n    - [What?](#what)\n    - [How?](#how)\n    - [FAQ](#faq)\n        - [Why YAML and not FOOML?](#why-yaml-and-not-fooml)\n        - [Is this production ready?](#is-this-production-ready)\n        - [What\'s with the name?](#whats-with-the-name)\n    - [Future development](#future-development)\n\n<!-- markdown-toc end -->\n\nPaque simplifies running simple workflows you want to run. It offers a few\nfeatures of `make`, but removing most of its power. It runs on a `paquefile` or\n`paquefile.yaml` (or just pass the name of the file). You can see a simple\n[example in the root folder](paquefile.yaml).\n\nIt supports Python 3.6.5+ (for no particular reason aside from being my default,\nit should work just fine on any relatively recent Python 3)\n\n## Installation\n\nIt should be enough to run\n\n```bash\npip install paque\n```\n\nand then \n\n```bash\npaque taskname  # If you have a paquefile or paquefile.yaml file\n```\n\n### Tab completion\n\nThis is a reminder to myself to implement tab completion (at lest for ZSH, since\nI have done that before)\n\n## Why?\n\nI had a series of `Dockerfile` I wanted to build sequentially, and run some\ncommands. It wasn\'t a right fit for docker-compose, so I wrote a makefile\n([here](https://github.com/rberenguel/spark_hadoop_kudu/blob/master/makefile)).\nThe result was excellent, BUT if you want to add logging, or any kind of\ninformation you need to start resorting to "makefile hacks" (like passing\nvariables down the dependency stack, or accessing subpaths of requirements...)\nthat didn\'t feel right.\n\nSo, I decided to write this.\n\n## What?\n\nYou define your tasks in a YAML file with specific syntax, of the form:\n\n```yaml\ntaskname:\n  - run: "what it runs"\n  - message: "what it logs"\n  - depends:\n      - task_it_depends_1\n      - task_it_depends_2\n  - sleep: integer\n\notherwise:\n  - run:\n      - "You can run several commands"\n      - "Passing them as an array"\n  - message:\n      - "Likewise for logging"\n      - "Yes."\n```\n\nYou can also use arguments and multiple arguments,\n\n```yaml\ntaskname:\n  - run: "{something} {folder}"\n  - message: "This does {something} on {folder}"\n\nmain:\n  - depends:\n      - taskname folder:/Users/foo/ something:rmdir\n```\n\nFor now you can\'t have spaces in arguments. Sorry.\n\nFor usage, you would just \n\n```bash\npaque taskname\n```\n\n## How?\n\nYAML (following the rules above) is converted into a dictionary of task names\nand [Tasks](paque/task.py) by a [Parser](paque/parser.py). Then a simple\ndepth-first-search [planner](paque/planner.py) finds an execution that satisfies\nall dependencies and transitive dependencies (with arguments) of `taskname`.\nFinally, the plan is passed to an [executor](paque/executor.py) that offloads it\nto the shell (or just logs it).\n\n## FAQ\n\n### Why YAML and not FOOML?\n\nI find YAML pretty readable and writable, as long as you restrict what you can\ndo. Since there is no nesting here, you can\'t shoot yourself in the foot with\nYAML. If you really can\'t stand YAML, you have two options\n\n- Use [dhall](https://github.com/dhall-lang/dhall-lang) and convert from dhall to YAML (_recommended_)\n- Write a [parser](paque/parser.py) for your favourite markup\n\n### Is this production ready?\n\nWell… `¯\\_(ツ)_/¯` I\'m pretty sure there is an issue with argument replacement\nin a corner case, but I can\'t put my finger on which. For simple use cases, this\nshould be safe. Since there is no branching, there is not much that can go wrong\nthough.\n\n### What\'s with the name?\n\nFor one, it\'s `python+make=pake`, but it was taken (I should have checked\nbefore), so left it at `paque`. It\'s also a form of "pa\' qué", an Spanish slang\nfor "para qué". I.e. _what for?_ `¯\\_(ツ)_/¯`\n\n### Contributing\n\nI\'m happy to receive PRs, so don\'t be shy. Also let me know if you used it, that\ncould be fun. As you see from the root folder, you will need to use\n[poetry](https://github.com/python-poetry/poetry)\n\n## Future development\n\nI will keep using it, so any bugs I find will be fixed. Likewise, I will keep\nimproving it, although the current version is "almost enough". Currently on the\n"roadmap" I have:\n\n- Generate a graphviz plot of the plan(s). This was one of the motivations to\n  write my own thingy, after all\n- Better tests: I wrote the ones I have with a combination of TDD and "let\'s\n  test and print". I want less tests of happy paths and more tests of corner\n  cases\n- Custom exceptions, right now it\'s just "raise that"\n- Automatically convert paquefile.dhall into a YAML paquefile (this was supposed\n  to be in this version but I got lazy)\n- Have a nicer CLI (probably using [cleo](https://github.com/sdispater/cleo))\n- Possibly, running tasks in parallel (this is a hard one given how the planner\n  works, so probably won\'t)\n- Conditionals?\n- Fixing the bug that is likely there in argument substitution\n',
    'author': 'Ruben Berenguel',
    'author_email': 'ruben+poetry@mostlymaths.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rberenguel/paque',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
