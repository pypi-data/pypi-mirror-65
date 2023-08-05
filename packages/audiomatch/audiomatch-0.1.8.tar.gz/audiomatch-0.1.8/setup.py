# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['audiomatch']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['audiomatch = audiomatch.cli:invoke']}

setup_kwargs = {
    'name': 'audiomatch',
    'version': '0.1.8',
    'description': 'A small command-line tool to find similar audio files',
    'long_description': '==========\naudiomatch\n==========\n\n.. image:: https://github.com/unmade/audiomatch/workflows/lint%20and%20test/badge.svg?branch=master\n    :alt: Build Status\n    :target: https://github.com/unmade/audiomatch/blob/master/.github/workflows/lint-and-test.yml\n\n.. image:: https://codecov.io/gh/unmade/audiomatch/branch/master/graph/badge.svg\n    :alt: Coverage Status\n    :target: https://codecov.io/gh/unmade/audiomatch\n\n.. image:: https://img.shields.io/pypi/v/audiomatch.svg\n    :alt: PyPI Package latest release\n    :target: https://pypi.org/project/audiomatch\n\n.. image:: https://img.shields.io/badge/License-MIT-purple.svg\n    :alt: MIT License\n    :target: https://github.com/unmade/apiwrappers/blob/master/LICENSE\n\n\nA small command-line tool to find similar audio files\n\nInstallation\n============\n\nFirst, install the Chromaprint_ fingerprinting library by Lukáš Lalinský. (The library\nitself depends on an FFT library, but it\'s smart enough to use an algorithm from\nsoftware you probably already have installed; see the Chromaprint page for details)\n\nThen you can install this library:\n\n.. code-block:: bash\n\n    pip install audiomatch\n\nYou can avoid installing all this libraries on your computer and run everything in\ndocker:\n\n.. code-block:: bash\n\n    docker run --rm -v "$(pwd)":/tmp fdooch/audiomatch "/tmp/*"\n\nQuickstart\n==========\n\nSuppose, we have a directory with Nirvana songs:\n\n.. code-block:: bash\n\n    $ ls demo\n    All Apologies (In Utero).m4a           Dumb (Unplugged in NYC).m4a\n    All Apologies (Unplugged in NYC).m4a   Pennyroyal Tea (In Utero).m4a\n    Dumb (In Utero).m4a                    Pennyroyal Tea (Solo Acoustic).mp3\n    Dumb (Radio Appearance, 1991).mp3      Pennyroyal Tea (Unplugged in NYC).m4a\n\nLet\'s find out which files sound similar:\n\n.. code-block:: bash\n\n    $ audiomatch --length 300 ./demo\n    These files sound similar:\n\n    ./demo/All Apologies (In Utero).m4a\n    ./demo/All Apologies (Unplugged in NYC).m4a\n\n    ---\n\n    ./demo/Dumb (In Utero).m4a\n    ./demo/Dumb (Unplugged in NYC).m4a\n\n    ---\n\n    ./demo/Pennyroyal Tea (In Utero).m4a\n    ./demo/Pennyroyal Tea (Solo Acoustic).mp3\n    ./demo/Pennyroyal Tea (Unplugged in NYC).m4a\n\n*Note #1: input audio files should be at least 10 seconds long*\n\n*Note #2: in some rare cases false positives are possible*\n\nWhat\'s happening here is that *audiomatch* takes all audio files from the directory and\ncompares them with each other.\n\nYou can also compare file with another file, file and directory, or directory to\ndirectory. If you need to, you can provide glob-style patterns, but don\'t forget to\nquote it, because otherwise shell expanded it for you. For example, let\'s compare all\n``.mp3`` files with ``.m4a`` files:\n\n.. code-block:: bash\n\n    $ audiomatch  "./demo/*.mp3" "./demo/*.m4a"\n    These files sound similar:\n\n    ../demo/Pennyroyal Tea (Solo Acoustic).mp3\n    ../demo/Pennyroyal Tea (Unplugged in NYC).m4a\n\nThis time, *audiomatch* took all files with ``.mp3`` extension and compare them with\nall files with ``.m4a`` extension.\n\nNote, how there is no In Utero version in the output. The reason it is present in the\nprevious output, because it actually similar with Unplugged version and then transitive\nlaw applies: if ``a = b`` and ``b = c``, then ``a = c``.\n\n--length\n--------\n\nThe ``--length`` specifies how many seconds to take for analysis from the song. Default\nvalue is 120 and it is good enough to find exactly the same song, but maybe in different\nquality. However, for a more complicated cases like same song played in different tempo\nthe more input we have the more accurate results are.\n\n--extension\n-----------\n\nBy default, ``audiomatch`` looks for files with ``.m4a``, ``mp3``, ``.caf`` extensions.\nIn theory, audio formats supported by ffmpeg_ also supported by *audiomatch*. You can\ntell to *audiomatch* to look for a specific format by using ``--extension`` flag:\n\n.. code-block:: bash\n\n    $ audiomatch -e .ogg -e .wav ./demo\n    Not enough input files.\n\nIndeed, we tried to compare files with ``.ogg`` and ``.wav`` extension, but there are\nno such files in the demo directory.\n\nMotivation\n==========\n\nI play guitar and do recordings from time to time mainly with Voice Memos on iPhone.\nOver the years, I have hundreds of recordings like that and I though it would be cool\nto find all the similar ones and see how I progress over the years.\n\nThat\'s why I wrote this library.\n\nReferences\n==========\n\n- Chromaprint_ and pyacoustid_ libraries\n- `Example: How to compare fingerprints`_\n- `Example: How to compare shifted fingerprints`_ (note: the code is a little bit weird)\n- `Explanation: How to compare fingerprints`_\n- `Popcount in Python with benchmarks`_\n\n.. _Chromaprint: https://github.com/acoustid/chromaprint\n.. _`Example: How to compare fingerprints`: https://gist.github.com/lalinsky/1132166\n.. _`Example: How to compare shifted fingerprints`: https://medium.com/@shivama205/audio-signals-comparison-23e431ed2207\n.. _`Explanation: How to compare fingerprints`: https://groups.google.com/forum/#!msg/acoustid/Uq_ASjaq3bw/kLreyQgxKmgJ\n.. _ffmpeg: http://ffmpeg.org\n.. _`Popcount in Python with benchmarks`: http://www.valuedlessons.com/2009/01/popcount-in-python-with-benchmarks.html\n.. _`pyacoustid`: https://github.com/beetbox/pyacoustid\n',
    'author': 'Aleksei Maslakov',
    'author_email': 'lesha.maslakov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
