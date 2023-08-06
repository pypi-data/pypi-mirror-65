# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['renutil']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.0,<5.0.0',
 'click>=7.1.1,<8.0.0',
 'jsonpickle>=1.3,<2.0',
 'logzero>=1.5.0,<2.0.0',
 'lxml>=4.5.0,<5.0.0',
 'requests>=2.23.0,<3.0.0',
 'semantic_version>=2.8.4,<3.0.0',
 'tqdm>=4.45.0,<5.0.0']

entry_points = \
{'console_scripts': ['renutil = renutil.renutil:cli']}

setup_kwargs = {
    'name': 'renutil',
    'version': '1.6.0',
    'description': "A toolkit for managing Ren'Py instances via the command line",
    'long_description': "# renUtil\nA toolkit for managing Ren'Py instances via the command line.\n\nrenUtil can install, update, launch and remove instances of Ren'Py. The instances are completely independent from each other. It automatically sets up and configures RAPT so new instances are instantly ready to deploy to many different platforms. Best of all, renUtil automatically configures Ren'Py in such a way that you can run it headless, making it well suited for build servers and continuous integration pipelines.\n\n## Installation\nrenUtil can be installed via pip:\n```bash\n$ pip install renutil\n```\n\nPlease note that renUtil requires Python 3 and will not provide backwards compatibility for Python 2 for the foreseeable future.\n\nSince the Android SDK installation process requires `pygame_sdl2`, this will have to be compiled and installed during the Ren'Py installation process. This process depends on SDL2 headers being installed on the system, which have to be installed through external means.\n\n### macOS\n```bash\nbrew install sdl2 sdl2_image sdl2_mixer sdl2_ttf\n```\n\n### Linux\n```bash\nsudo apt install libsdl2-dev\n```\n\n## Usage\n```bash\nusage: renutil [-h]\n               {list,ls,install,i,uninstall,u,remove,r,rm,launch,l,cleanup,clean,c}\n               ...\n\nA toolkit for managing Ren'Py instances via the command line.\n\npositional arguments:\n  {list,ls,install,i,uninstall,u,remove,r,rm,launch,l,cleanup,clean,c}\n    list (ls)           List Ren'Py versions.\n    install (i)         Install a version of Ren'Py.\n    uninstall (u, remove, r, rm)\n                        Uninstall an installed version of Ren'Py.\n    launch (l)          Launch an installed version of Ren'Py.\n    cleanup (clean, c)  Clean temporary files of the specified Ren'Py version.\n\noptional arguments:\n  -h, --help            show this help message and exit\n```\n\n# Disclaimer\nrenUtil is a hobby project and not in any way affiliated with Ren'Py. This means that there is no way I can guarantee that it will work at all, or continue to work once it does. Commands are mostly relayed to the Ren'Py CLI, so any issues with distribution building or startup are likely the fault of Ren'Py and not mine. renUtil is not likely to break on subsequent updates of Ren'Py, but it is not guaranteed that any available version will work correctly. Use this at your own discretion.\n",
    'author': 'CobaltCore',
    'author_email': 'cobaltcore@yandex.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kobaltcore/renutil',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
