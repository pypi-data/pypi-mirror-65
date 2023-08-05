# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deckz']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.1,<3.0.0',
 'PyYAML>=5.3.1,<6.0.0',
 'appdirs>=1.4.3,<2.0.0',
 'click>=7.1.1,<8.0.0',
 'coloredlogs>=14.0,<15.0',
 'pygit2>=1.2.0,<2.0.0']

entry_points = \
{'console_scripts': ['deckz = deckz.__main__:main']}

setup_kwargs = {
    'name': 'deckz',
    'version': '2.2.1',
    'description': 'Tool to handle multiple beamer decks.',
    'long_description': "# `deckz`\n\n[![CI Status](https://img.shields.io/github/workflow/status/m09/deckz/CI?label=CI&style=for-the-badge)](https://github.com/m09/deckz/actions?query=workflow%3ACI)\n[![CD Status](https://img.shields.io/github/workflow/status/m09/deckz/CD?label=CD&style=for-the-badge)](https://github.com/m09/deckz/actions?query=workflow%3ACD)\n[![PyPI Project](https://img.shields.io/pypi/v/deckz?style=for-the-badge)](https://pypi.org/project/deckz/)\n[![Docker Hub Image](https://img.shields.io/docker/v/hugomougard/deckz?label=DOCKER&style=for-the-badge)](https://hub.docker.com/r/hugomougard/deckz)\n\nTool to handle a large number of beamer decks, used by several persons, with shared slides amongst the decks. It is currently not meant to be usable directly by people finding about the package on GitHub. Please open an issue if you want more details or want to discuss this solution.\n\n## Installation\n\nWith `pip`:\n\n    pip install deckz\n\n## Directory Structure\n\n`deckz` works with big assumptions on the directory structure of your presentation repository. Among those assumptions:\n\n- your directory should be a git repository\n- it should contain a `shared` folder for everything that will be shared by all decks during compilation (images, code snippets, etc)\n- it should contain jinja2 LaTeX templates in the `jinja2` directory, with a specific name (`$VERSION.tex.jinja2`) containing a version for reference in configuration, for example: `v1.tex.jinja2`\n- your deck folders should be contained in an organization/company folder. This is meant to avoid repeating the company details all over the place\n- several configuration should be present to customize the decks efficiently (more on that later)\n\n```\nroot (git repository)\n├── global-config.yml\n├── jinja2\n│\xa0\xa0 ├── v1.tex.jinja2\n│\xa0\xa0 └── v2.tex.jinja2\n├── shared\n│\xa0\xa0 ├── img\n│\xa0\xa0 │\xa0\xa0 ├── image1.png\n│\xa0\xa0 │\xa0\xa0 └── image2.jpg\n│\xa0\xa0 ├── code\n│\xa0\xa0 │\xa0\xa0 ├── snippet1.py\n│\xa0\xa0 │\xa0\xa0 └── snippet2.js\n│\xa0\xa0 └── latex\n│\xa0\xa0  \xa0\xa0 ├── module1.tex\n│\xa0\xa0  \xa0\xa0 └── module2.tex\n├── company1\n│\xa0\xa0 ├── company-config.yml\n│\xa0\xa0 └── deck1\n│\xa0\xa0  \xa0\xa0 ├── session-config.yml\n│\xa0\xa0  \xa0\xa0 ├── deck-config.yml\n│\xa0\xa0  \xa0\xa0 ├── targets.yml\n│\xa0\xa0  \xa0\xa0 └── module3.tex\n└── company2\n \xa0\xa0 ├── company-config.yml\n \xa0\xa0 └── deck2\n \xa0\xa0  \xa0\xa0 ├── session-config.yml\n \xa0\xa0  \xa0\xa0 ├── deck-config.yml\n \xa0\xa0  \xa0\xa0 ├── targets.yml\n \xa0\xa0  \xa0\xa0 └── module4.tex\n```\n\n## Configuration\n\n`deckz` uses small configuration files in several places to avoid repetition.\n\n### Configuration merging\n\nThe configuration are merged in this order (a value from a configuration on the bottom overrides a value from a configuration on the top):\n\n- `global-config.yml`\n- `user-config.yml`\n- `company-config.yml`\n- `deck-config.yml`\n- `session-config.yml`\n\n### Using the configuration values in LaTeX files\n\nThe values obtained from the merged configurations can be used in LaTeX after a conversion from snake case to camel case: if the configuration contains the key `trainer_email`, it will be defined as the `\\TrainerEmail` command in LaTeX.\n\n### Details about specific configurations\n\n#### Global configuration\n\nThe global configuration contains the default values that don't fit at a more specific level.\n\nExample:\n\n```\npresentation_size: 10pt\n```\n\n#### User configuration\n\nThe user configuration contains the values that change when the speaker changes. It is located in the XDG compliant config location. It is `$HOME/.config/deckz/user-config.yml` on GNU/Linux for example.\n\nExample:\n\n```\ntrainer_activity: Data Scientist\ntrainer_email: john@doe.me\ntrainer_name: John Doe\ntrainer_specialization: NLP, NLU\ntrainer_training: MSc at UCL\n```\n\n#### Company configuration\n\nThe company configuration contains everything required to brand the presentations according to the represented company.\n\nExample:\n\n```\ncompany_logo: logo_company\ncompany_logo_height: 1cm\ncompany_name: Company\ncompany_website: https://www.company.com\n```\n\n#### Deck configuration\n\nThe deck configuration contains the title and acronym of the talk.\n\nExample:\n\n```\ndeck_acronym: COV19\ndeck_title: Machine Learning and COVID-19\n```\n\n#### Session configuration\n\nThe session configuration contains everything that will change from one session of a specific talk to another one.\n\nExample:\n\n```\nsession_end: 30/04/2020\nsession_start: 27/04/2020\n```\n\n## Usage\n\nSee the `-h` flag of the `deckz` command line tool.\n",
    'author': 'm09',
    'author_email': '142691+m09@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/m09/deckz',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
