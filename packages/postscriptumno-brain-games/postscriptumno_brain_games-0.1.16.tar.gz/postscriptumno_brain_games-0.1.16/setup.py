# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brain_games', 'brain_games.games']

package_data = \
{'': ['*'],
 'brain_games': ['scripts/brain_calc.py',
                 'scripts/brain_calc.py',
                 'scripts/brain_calc.py',
                 'scripts/brain_calc.py',
                 'scripts/brain_calc.py',
                 'scripts/brain_calc.py',
                 'scripts/brain_even.py',
                 'scripts/brain_even.py',
                 'scripts/brain_even.py',
                 'scripts/brain_even.py',
                 'scripts/brain_even.py',
                 'scripts/brain_even.py',
                 'scripts/brain_games.py',
                 'scripts/brain_games.py',
                 'scripts/brain_games.py',
                 'scripts/brain_games.py',
                 'scripts/brain_games.py',
                 'scripts/brain_games.py',
                 'scripts/brain_gcd.py',
                 'scripts/brain_gcd.py',
                 'scripts/brain_gcd.py',
                 'scripts/brain_gcd.py',
                 'scripts/brain_gcd.py',
                 'scripts/brain_gcd.py',
                 'scripts/brain_prime.py',
                 'scripts/brain_prime.py',
                 'scripts/brain_prime.py',
                 'scripts/brain_prime.py',
                 'scripts/brain_prime.py',
                 'scripts/brain_prime.py',
                 'scripts/brain_progression.py',
                 'scripts/brain_progression.py',
                 'scripts/brain_progression.py',
                 'scripts/brain_progression.py',
                 'scripts/brain_progression.py',
                 'scripts/brain_progression.py']}

install_requires = \
['prompt>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['brain-calc = brain_games.scripts.brain_calc:main',
                     'brain-even = brain_games.scripts.brain_even:main',
                     'brain-games = brain_games.scripts.brain_games:main',
                     'brain-gcd = brain_games.scripts.brain_gcd:main',
                     'brain-prime = brain_games.scripts.brain_prime:main',
                     'brain-progression = '
                     'brain_games.scripts.brain_progression:main']}

setup_kwargs = {
    'name': 'postscriptumno-brain-games',
    'version': '0.1.16',
    'description': 'Brain games project',
    'long_description': '# python-project-lvl1\n\n[![Maintainability](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/maintainability)](https://codeclimate.com/github/codeclimate/codeclimate/maintainability)\n[![Test Coverage](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/test_coverage)](https://codeclimate.com/github/codeclimate/codeclimate/test_coverage)\n[![Build Status](https://travis-ci.org/postscriptumno/python-project-lvl1.svg?branch=master)](https://travis-ci.org/postscriptumno/python-project-lvl1)\n\n## Installing command\n\npip3 install --index-url <https://test.pypi.org/simple> --extra-index-url <https://pypi.org/simple> postscriptumno-brain-games\n\n### Brain-even\n\n[![asciicast](https://asciinema.org/a/XTWAUeLM5LwAr50LzE0nPhQrv.svg)](https://asciinema.org/a/XTWAUeLM5LwAr50LzE0nPhQrv)\n\n### Brain-calc\n\n[![asciicast](https://asciinema.org/a/TC4VwapXY6QXU4JhePMjsrie1.svg)](https://asciinema.org/a/TC4VwapXY6QXU4JhePMjsrie1)\n\n### Brain-progression\n\n[![asciicast](https://asciinema.org/a/dDOOgbLGx6bG1thsVgqZRbHlY.svg)](https://asciinema.org/a/dDOOgbLGx6bG1thsVgqZRbHlY)\n\n### Brain-gcd\n\n[![asciicast](https://asciinema.org/a/NgR2pi5QplmaTSUGOFw6mgble.svg)](https://asciinema.org/a/NgR2pi5QplmaTSUGOFw6mgble)\n\n### Brain-prime\n\n[![asciicast](https://asciinema.org/a/0RUGPdJhJObEYpKowc0O2bK4m.svg)](https://asciinema.org/a/0RUGPdJhJObEYpKowc0O2bK4m)\n',
    'author': 'postscriptumno',
    'author_email': 'postscriptum.no@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/postscriptumno/python-project-lvl1',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
