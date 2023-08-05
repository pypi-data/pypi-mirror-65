# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['subgrab', 'subgrab.providers', 'subgrab.utils']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'lxml>=4.5.0,<5.0.0',
 'requests>=2.23.0,<3.0.0',
 'typing>=3.7.4,<4.0.0']

entry_points = \
{'console_scripts': ['subgrab = subgrab.cli:main']}

setup_kwargs = {
    'name': 'subgrab',
    'version': '1.0.3',
    'description': 'Automated subtitles fetching',
    'long_description': '# SubGrab - Command-line Subtitles Downloader:\n\n[![Downloads](http://pepy.tech/badge/subgrab)](http://pepy.tech/count/subgrab)\n\nA utility which provides an ease for automating media i.e., Movies, TV-Series subtitle scraping from multiple providers.\n\n# Index:\n\n* [Installation](https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber#installation)\n* [Preview](https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber#preview)\n* [Requirements](https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber#requirements)\n* [Supported Sites](https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber#providers-supported)\n* [Preview](https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber#preview)\n* [Usage](https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber#usage)\n* [Examples](https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber#examples)\n* [Features](https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber#features)\n* [Changelog](https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber#changelog)\n* [Features Upcoming](https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber#todo)\n\n# Status/Version:\n\n* Current Version: 1.0.2\n\n# Installation:\n\n`pip install subgrab`\n\n# Preview:\n\n[![asciicast](https://asciinema.org/a/316877.svg)](https://asciinema.org/a/316877)\n\n# Providers Supported:\n\nFollowing sites can be used for subtitle downloading:\n\n<center>\n\n|           Supported Sites            |\n| :----------------------------------: |\n|           SUBSCENE `(-m)`            |\n| ALLSUBDB `(default for directories)` |\n\n</center>\n\n# Usage:\n\n```\nUsage:\n\nsubgrab [-h] [-d directory path] [-m Name of the movie/season] [-s Silent Mode]\n                   [-c Number of Subtitles to be downloaded] [-l Custom language]\n\nOptions:\n\n  -h, --help            Show this help message and exit.\n\n  -d DIR, --dir DIR     Specify directory to work in.\n\n  -m MOVIE_NAME [MOVIE_NAME ...], --movie-name MOVIE_NAME [MOVIE_NAME ...]\n                        Provide Movie Name.\n\n  -s, --silent          Silent mode.\n\n  -c COUNT, --count COUNT\n                        Number of subtitles to be downloaded.\n\n  -l LANG, --lang LANG  Change language.\n```\n\n# Examples:\n\n```python\nsubgrab                             # To run in current working directory.\n\nsubgrab -m Doctor Strange           # For custom movie subtitle download.\n\nsubgrab -m Doctor Strange -s        # Silent mode (No prompts i.e., title selection [if not found]).\n\nsubgrab -d "DIRECTORY_PATH"         # For specific directory.\n\nsubgrab -m The Intern 2015 -s -l AR # Language specified (First two characters of the language).\n\nsubgrab -m The Intern 2015 -c 3 -s  # Download 3 subtitles for the movie.\n```\n\n# Changelog:\n\n* [Changelog](https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber/blob/master/changelog.rst)\n\n# Note:\n\n* (For Windows) To use it from the context menu, paste subtitle.bat file in "shell:sendto" (By typing this in RUN).\n  Taken from Manojmj subtitles script.\n\n# Features:\n\n* Two Mode (CLI and Silent inside individual media downloading [-m]) - CLI mode is executed when the title (provided i.e. media name) is not recognized by the site. Mostly when year is not provied (when two or more media names collide). Silent mode is usually executed when year is provided in the argument. Optional, you can also specify silent mode argument - which forces to download subtitles without title selection prompt. The media argument (-m) followed by the silent mode (-s) argument forces silent mode.\n\n* Subtitles count argument added which allows you to download multiple subtitles for an individual media. This is useful when the exact match is not found and you can download multiple srt files and check them if they are in sync with the media file (integrated in v0.12).\n\n* Added multiple languages support (v0.12).\n\n* Allows you to download subtitles for movies by specifying movie name and year (optional).\n\n* Allows you to download subtitles for media files in a specified directory.\n\n* Cross-platform (Tested on Linux and Windows).\n\n* Logs generation on script execution (v0.15)\n\n* Added Support for the SubDb (v0.16), now first preference for downloading subtitles is SubDB in downloading subtitles from a directory.\n\n* Initial release (v1.0.0)\n\n# TODO:\n\n* [x] Adding support for more languages.\n* [x] Adding flags.\n* [x] Support for AllSubDB .\n* [ ] Support for OpenSubtitles, YifySubtitles.\n* [ ] Auto-Sync subtitle naming with the media file when downloaded from subscene.\n* [ ] A GUI box which creates a dialogue box (consisting of tick and cross), which waits for the user to check if the subtitle downloaded is synchronized with media file or not - if clicked cross, downloads another subtitle (Process gets repeated unless, correctly synchronized).\n* [ ] Watch-folder feature (runs as a service). # Useful for movies automatically downloaded on servers.\n* [ ] Argument handling (Replace Argsparse with Click).\n* [ ] Using Tabulate for monitoring directory subtitle downloading progress. Three Columns [#, Movie_Folder, Status].\n* [ ] Better Logging.\n* [ ] Download subtitles for movies contained in a directory of X year.\n* [x] Adding silent mode for downloading subtitles.\n* [x] Adding CLI mode for manually downloading subtitles.\n* [x] Implement Logging.\n* [x] Implementation for seasons episodes.\n* [x] Different search algorithms implementation for precise results.\n* [x] Improving CLI Mode by displaying the menu according to the site.\n* [ ] Multiple subtitle language support also associated with the count variable.\n\n```\nFor example:\n>>> subgrab -m Doctor Strange -s -l AR, EN, SP -c 3\nshould download 3 subtitles for each language specified\n```\n\n* [ ] An option to print list of movies which has subtitles.\n* [ ] Creating options in context menu.\n* [ ] Display menu which enables to download subtitles for selected directories. (Supporting ranges)\n\n```\nFor Examples:\n(0) Movie 1\n(1) Movie 2\n.\n.\n(10) Movie 10\n------------------------------------------------------------------------------------------------------\n(Interactive Prompt)\n> 1-3, 6,7,10\n\nwill download subtitles for the directories specified.\n```\n',
    'author': 'Rafay Ghafoor',
    'author_email': 'rafayghafoor@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
