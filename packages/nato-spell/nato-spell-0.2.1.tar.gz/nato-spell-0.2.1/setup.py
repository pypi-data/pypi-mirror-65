# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['nato_spell']
entry_points = \
{'console_scripts': ['nato-spell = nato_spell:main',
                     'nato_spell = nato_spell:main']}

setup_kwargs = {
    'name': 'nato-spell',
    'version': '0.2.1',
    'description': 'Spelling engine for the NATO phonetic alphabet',
    'long_description': "# nato-spell\n\n**nato-spell** is a Python package that can be used to spell a string / file with the well-known NATO phonetic alphabet.\n\n## Installation\n\nSystem requirements:\n  - **aplay** (ALSA command line player - it may already be installed on your computer)\n  - **python >= 3**\n\n\nUse [pip](https://pip.pypa.io/en/stable/) or pipx to install `nato-spell`.\n\n```bash\npip install nato-spell\n```\n\n## Usage\n\nMinimal example\n```\nnato-spell SPELLME \n```\n\nSpelling from stdin\n```\necho SPELLME | nato-spell - \n```\n\nIncrease the delay between characters (unit is seconds, default is 0)\n```\nnato-spell SPELLME --char-delay=1\n```\n\nUse a different sound directory\n```\nnato-spell SPELLME --sound-dir=/home/me/my-sound-dir\n```\n\nAnd finally, an example, where we use them all together.\n```\necho SPELLME | nato-spell - --sound-dir=/home/me/my-sound-dir --char-delay=1\n```\n\n## Sound assets \n\nThese sounds were published by Tim Kahn and hosted on freesound.org\n - Tim Kahn ( https://freesound.org/people/tim.kahn/ )\n\nThank you Amy Gedgaudas and Tim Kahn for all these sounds.\n\nThey're licensed under:\nhttp://creativecommons.org/licenses/by/3.0/\n\n\n## Contributing\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)\n",
    'author': 'Xavier Francisco',
    'author_email': 'xavier.n.francisco@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Qu4tro/nato-spell/',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
