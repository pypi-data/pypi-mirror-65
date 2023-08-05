# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vodscrepe']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.8.2,<5.0.0',
 'lxml>=4.4.2,<5.0.0',
 'requests>=2.23.0,<3.0.0',
 'tqdm>=4.41.1,<5.0.0']

entry_points = \
{'console_scripts': ['vodscrepe = bin/vodscrepe']}

setup_kwargs = {
    'name': 'vodscrepe',
    'version': '1.0.0',
    'description': 'https://vods.co/ vod scraper',
    'long_description': '# `vodscrepe`\n\n[![](https://img.shields.io/pypi/v/vodscrepe.svg?style=flat)](https://pypi.org/pypi/vodscrepe/)\n[![](https://img.shields.io/pypi/dw/vodscrepe.svg?style=flat)](https://pypi.org/pypi/vodscrepe/)\n[![](https://img.shields.io/pypi/pyversions/vodscrepe.svg?style=flat)](https://pypi.org/pypi/vodscrepe/)\n[![](https://img.shields.io/pypi/format/vodscrepe.svg?style=flat)](https://pypi.org/pypi/vodscrepe/)\n[![](https://img.shields.io/pypi/l/vodscrepe.svg?style=flat)](https://github.com/dawsonbooth/vodscrepe/blob/master/LICENSE)\n\n# Description\n\nThis PyPI package is best described as a tool for scraping the [vods.co](https://vods.co/) website. Currently, the package only supports Super Smash Bros. Melee vods.\n\n# Installation\n\nWith [Python](https://www.python.org/downloads/) installed, simply run the following command to add the package to your project.\n\n```bash\npip install vodscrepe\n```\n\n# Usage\n\nThe following is an example usage of the package, which is also included in the repo as `example.py`:\n\n```python\nfrom tqdm import tqdm\n\nfrom vodscrepe import Scraper, formatted_title\n\ns = Scraper(\'melee\')\n\ntry:\n    for vod in s.scrape(show_progress=True):\n        if vod is not None:\n            tqdm.write(formatted_title(vod))\nexcept KeyboardInterrupt:\n    tqdm.write("Scraping terminated.")\n```\n\nThis example lists information about the vods from the most recent to the last page in the following fashion:\n\n```bash\npython example.py > sets.txt\n```\n\nThen, the `sets.txt` file becomes populated with vod information...\n\n```txt\n[\'2020-03-15\'] CEO Dreamland 2020 - Colbol (Fox) vs Hungrybox (Jigglypuff) - Grand Finals - Bo5\n[\'2020-03-15\'] CEO Dreamland 2020 - Colbol (Fox) vs n0ne (Captain Falcon) - Losers Finals - Bo5\n[\'2020-03-15\'] CEO Dreamland 2020 - Colbol (Fox) vs Gahtzu (Captain Falcon) - Losers Semis - Bo5\n[\'2020-03-15\'] CEO Dreamland 2020 - Hungrybox (Jigglypuff) vs n0ne (Captain Falcon) - Winners Finals - Bo5\n[\'2020-03-15\'] CEO Dreamland 2020 - Panda (FL) (Fox) vs Gahtzu (Captain Falcon) - Losers Quarters - Bo5\n[\'2020-03-15\'] CEO Dreamland 2020 - Colbol (Fox) vs Chef Rach (Captain Falcon) - Losers Quarters - Bo5\n[\'2020-03-15\'] CEO Dreamland 2020 - n0ne (Captain Falcon) vs Panda (FL) (Fox) - Winners Semis - Bo5\n[\'2020-03-15\'] CEO Dreamland 2020 - Colbol (Fox) vs Hungrybox (Jigglypuff) - Winners Semis - Bo5\n[\'2020-03-15\'] CEO Dreamland 2020 - Krudo (Sheik) vs Gahtzu (Captain Falcon) - Losers Top 8 - Bo5\n[\'2020-03-15\'] CEO Dreamland 2020 - blankshooter744 (Fox) vs Chef Rach (Captain Falcon) - Losers Round 5 - Bo5\n[\'2020-03-15\'] CEO Dreamland 2020 - Leighton (Jigglypuff) vs Prof (Marth) - Losers Round 5 - Bo5\n[\'2020-03-15\'] CEO Dreamland 2020 - Sinbad (Sheik) vs Krudo (Sheik) - Losers Round 5 - Bo5\n[\'2020-03-15\'] CEO Dreamland 2020 - Wevans (Samus) vs Gahtzu (Captain Falcon) - Losers Round 5 - Bo5\n[\'2020-03-15\'] CEO Dreamland 2020 - Sinbad (Sheik) vs Dom (FL) (Marth) - Losers Round 4 - Bo5\n[\'2020-03-15\'] CEO Dreamland 2020 - Colbol (Fox) vs Gahtzu (Captain Falcon) - Winners Quarters - Bo5\nScraping terminated.\n```\n\n...while the terminal details the progress:\n\n```bash\nAll vods:   0%|                                              | 0/331 [00:07<?, ?pages/s]\nPage 0:  25%|██████████████                                  | 15/60 [00:07<00:12,  3.07vods/s]\n```\n\n# License\n\nThis software is released under the terms of [MIT license](LICENSE).\n',
    'author': 'Dawson Booth',
    'author_email': 'pypi@dawsonbooth.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dawsonbooth/vodscrepe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
