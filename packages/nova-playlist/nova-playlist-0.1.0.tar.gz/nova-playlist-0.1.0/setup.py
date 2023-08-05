# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['nova_playlist']
install_requires = \
['beautifulsoup4>=4.8,<5.0', 'pytz']

entry_points = \
{'console_scripts': ['nova = nova_playlist:main']}

setup_kwargs = {
    'name': 'nova-playlist',
    'version': '0.1.0',
    'description': 'Display information about the songs that recently played on Radio Nova',
    'long_description': '# nova-playlist\n\n[Radio Nova][0] plays amazing music at night.\n\nThere could be Fela Kuti, then hip-hop from the 1990s, then Motown, then Tuareg\nmusic, then some minimal electro, then Hungarian folk songs, then David Bowie,\nthen Amazonian cumbia, then a French song that was released last month, then\nSufi devotional music from Punjab, then Nina Simone, then a tune from the\nnorth-east of Brazil. It\'s wild.\n\nAnd if you, like me, live a few time zones west of Paris, you get to\nconveniently enjoy it all in the evening instead of having to be up in the\nmiddle of the night!\n\nOften, I want to know which song is currently playing, so that I can find out\nmore about it and the artist. There is a [page][1] where one can find what\nmusic has aired on the Radio in the past, but it\'s buggy and a bit annoying to\nuse. And even if the page was great to use, it wouldn\'t be as great as using\nthe command line for it! _Ergo_ this little script.\n\n\n## Installation\n\n    pipx install nova-playlist\n\nOr use `pip`.\n\n\n## Usage\n\n    $ nova\n    20:36  Orchestra Baobab - Liiti Liiti\n    20:30  Chico Buarque - Construção\n    20:27  Abner Jay - My Middle Name Is The Blues\n    20:23  Brigitte Fontaine - Le Goudron\n    ...\n\nBy default, the times are in the "US/Eastern" time zone. If you want them in\nanother time zone, you can pass the `-t`/`--timezone` argument:\n\n    $ nova -t Europe/Berlin\n    03:12  Los Camperos De Valles - El Gallo\n    03:09  Karen Dalton - Something On Your Mind\n    03:04  Têtes Raides & Yann Tiersen - Ginette\n    02:59  The Toraia Orchestra Of Algiers - Nar Houbi Techaal\n    ...\n\n\n## Caveat\n\nThis can be somewhat brittle. Sometimes, the data stops being updated on the\nsite. Or the data gets updated, but the timestamps are 11 minutes off from\nwhat\'s playing in the stream. And of course, if they ever change their HTML\nstructure in any way, this could also start failing miserably. But so far, so\ngood!\n\n\n[0]: https://www.nova.fr/radionova/nova-la-nuit\n[1]: https://www.nova.fr/radionova/radio-nova\n',
    'author': 'Rafik Draoui',
    'author_email': 'rafik@rafik.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rafikdraoui/nova-playlist',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
