# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gigaleaf', 'gigaleaf.linkedfiles']

package_data = \
{'': ['*'], 'gigaleaf': ['resources/*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['gigaleaf_askpass = gigaleaf.askpass:askpass']}

setup_kwargs = {
    'name': 'gigaleaf',
    'version': '0.1.2',
    'description': 'An opinionated package for integrating Gigantum and Overleaf Projects',
    'long_description': '# gigaleaf\n[![CircleCI](https://circleci.com/gh/gigantum/gigaleaf/tree/master.svg?style=svg)](https://circleci.com/gh/gigantum/gigaleaf/tree/master)\n\nAn opinionated library to link Gigantum Projects to Overleaf Projects. This tool automatically manages git repositories\nto link the outputs from a Gigantum Project to an Overleaf Project, letting you build a completely reproducible \nworkflow from analysis to publication.\n\n**NOTE: This library is an early alpha proof of concept and subject to change!**\n\n**NOTE: This library uses the Overleaf git bridge and is only included in paid Overleaf accounts. The Overleaf project\nowner must have a paid account, but collaborators do not.**\n\n### Installation\ngigaleaf may be installed using pip.\n\n```bash\npip install gigaleaf\n```\n\n### Usage\n\ngigaleaf is currently designed to work inside Jupyter Notebooks running in Gigantum. The high-level API is pretty simple. The general workflow is:\n\n* Create an Overleaf Project\n  \n* Get the git share URL from Overleaf\n  * Click on "Git" under the sync options\n    \n    ![Git Share Link](./imgs/git_link.png)\n    \n  * Copy the URL only (not the entire git command) from the modal that is shown\n    \n    ![Git Share Link](./imgs/git_link_modal.png)\n\n* Create an instance of gigaleaf\n\n  ```python\n  from gigaleaf import Gigaleaf\n  \n  gl = Gigaleaf()\n  ```\n  \n  This will start the configuration process where you enter the Overleaf URL along with\n  the email and password you use to log into Overleaf. These will be stored in a file locally that is "untracked" in \n  Gigantum and therefore will not sync or be shared. Other users will be prompted for _their_ Overleaf credentials if\n  they run your notebook. To be able to access your Overleaf project and run `gigaleaf` commands, they must also have \n  access to your Overleaf project. \n  \n* Link an output file\n\n  ```python\n  gl.link_image(\'output/fig1.png\')\n  ```\n  \n  Here, you pass the relative path in Gigantum to the that file you want to link. Currently image and csv files are\n  supported. Any time this file changes and you sync, it will automatically be updated in your Overleaf project! \n  **You only need to call this once per file that you wish to track. Calling it again will update settings (e.g.\n  a figure caption)**\n  \n* Sync Projects\n\n  ```python\n  gl.sync()\n  ```\n  \n  This will pull changes from Overleaf, apply all gigaleaf managed changes, and then push back to Overleaf. Once files\n  are linked, you typically will only be calling `.sync()`. It\'s safe to call `.sync()` multiple times, in particular\n  at the end of a notebook when you\'d want to update Overleaf with your latest results.\n\n### Advanced Usage\n\ngigaleaf also provides Latex subfiles that you can use into your Overleaf Project that make adding and updating content\nfrom Gigantum trivial. To take full advantage of this, the link methods have optional arguments:\n\n`.link_image()` \n\n* caption: A caption that will be added to the image. If omitted, not caption is inserted.\n* label: A label to add to the figure for referencing inside your Overleaf document.\n* width: A string to set width of the image. The default is "0.5\\\\textwidth".\n* alignment: A string to set the position of the image using the `adjustbox` package. The default is \'center\'.\n\n`.link_csv()` \n\n* caption: A caption that will be added to the table. If omitted, not caption is inserted.\n* label: A label to add to the table for referencing inside your Overleaf document.\n\nTo use the subfiles generated you need to make a few modifications to your `main.tex` preamble. You may need to modify\nthis depending on your exact project configuration:\n\n```latex\n% gigaleaf setup\n\\usepackage[export]{adjustbox} % Needed if linking image files\n\\usepackage{graphicx} % Needed if linking image files\n\\graphicspath{{gigantum/data/}{../data/}} % Needed if linking image files\n\\usepackage{csvsimple} % Needed if linking csv files\n\\usepackage{float} % Needed if linking csv files\n\\restylefloat{table} % Needed if linking csv files\n\\usepackage{subfiles} % Best loaded last in the preamble\n% gigaleaf setup\n```\n\nOnce configured, you can simply import the subfiles as they are created in your project. They will be named in a way\nthat matches the files they are linked to:\n\n```latex\n\\subfile{gigantum/subfiles/fig1_png}\n```\n\nIn this example, this subfile would render the image `fig1.png` that we linked above.\n\n\n### Contributing\n\nThis project is packaged using [poetry](https://python-poetry.org/). To develop, install packages with:\n\n```bash\npoetry install\n```\n\nWhen working, be sure to sign-off all of your commits.\n\nIf trying to install in a Gigantum Project from source for testing, poetry needs to not try to create a virtualenv\nand should install as the user. This can be done by setting the following options:\n\n```bash\npoetry config virtualenvs.create false\nexport PIP_USER=yes\n```\n',
    'author': 'Dean Kleissas',
    'author_email': 'dean@gigantum.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gigantum/gigaleaf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
