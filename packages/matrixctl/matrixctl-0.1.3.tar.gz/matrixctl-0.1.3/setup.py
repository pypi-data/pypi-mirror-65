# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['matrixctl']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.0,<4.0.0',
 'argcomplete>=1.11.1,<2.0.0',
 'coloredlogs>=14.0,<15.0',
 'paramiko>=2.7.1,<3.0.0',
 'requests>=2.23.0,<3.0.0',
 'tabulate>=0.8.7,<0.9.0']

entry_points = \
{'console_scripts': ['matrixctl = matrixctl.application:main']}

setup_kwargs = {
    'name': 'matrixctl',
    'version': '0.1.3',
    'description': 'Controls a synapse oci-container instance via ansible',
    'long_description': '![GitHub](https://img.shields.io/github/license/MichaelSasser/matrixctl?style=flat-square)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/matrixctl?style=flat-square)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/matrixctl?style=flat-square)\n![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/michaelsasser/matrixctl?style=flat-square)\n![GitHub Release Date](https://img.shields.io/github/release-date/michaelsasser/matrixctl?style=flat-square)\n![PyPI - Status](https://img.shields.io/pypi/status/matrixctl?style=flat-square)\n![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/michaelsasser/matrixctl?style=flat-square)\n\n# MatrixCtl\n\nMatrixCtl is a python program to control, manage, provision and deploy our\nmatrix homeserver. I had a bunch of shell scripts doing that. Two weeks\nafter using them I couldn\'t remember the order in which I have to use the\narguments or which arguments where needed. It was a pain. So I decided I hack\nsomething together fast.\n\nIt is not the most elegant piece of software I wrote, but it should do the\ntrick. I will continue to port the rest of the scripts and add a few new\nfeatures.\n\nMaybe it is also useful for someone else.\n\n## Branching Model\n\nThis repository uses the\n[git-flow](https://danielkummer.github.io/git-flow-cheatsheet/index.html)\nbranching model by [Vincent Driessen](https://nvie.com/about/).\nIt has two branches with infinite lifetime:\n\n* [master](https://github.com/MichaelSasser/matrixctl/tree/master)\n* [develop](https://github.com/MichaelSasser/matrixctl/tree/develop)\n\nThe master branch gets updated on every release. The develop branch is the\nmerging branch.\n\n## Command line tool\n\nMatrixCtl as a pure commandline tool. You can use it as package, if you like,\nbut breaking changes may be introduced, even in a minor change.\n\n```\n# matrixctl\nusage: matrixctl [-h] [--version] [-d]\n              {adduser,adduser-jitsi,deluser-jitsi,list-users,deluser,deploy,update,maintainance} ...\n\npositional arguments:\n  {adduser,adduser-jitsi,deluser-jitsi,list-users,deluser,deploy,update,maintainance}\n    adduser             Add a new matrix user\n    adduser-jitsi       Add a new jitsi user\n    deluser-jitsi       Deletes a jitsi user\n    list-users          Lists users\n    deluser             Deletes a user\n    deploy              Provision and deploy\n    update              Updates the ansible repo\n    maintainance        Run Maintainance tasks\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --version             show program\'s version number and exit\n  -d, --debug           Enables debugging mode.\n```\n\n## Configuration File\n\nTo use this program you need to have this config file in\n"/etc/matrixctl/config" or in "~/.config/matrixctl/config".\n\n```toml\n[ANSIBLE]\n# The absolute path to the fully configured matrix-docker-ansible-deploy\n# playbook from https://github.com/spantaleev/matrix-docker-ansible-deploy.\n\nMatrixDockerAnsibleDeployPath="/absolut/path/to/matrix-docker-ansible-deploy"\n\n[SERVER]\n# If you have your own playbook, to provision your matrix server, you can\n# fill out this section. MatrixCtl will run this before the\n# matrix-docker-ansible-deploy playbook.\n\n# If you have a special "ansible.cfg" for your playbook, fill in the absolute\n# path to it.\n\n# AnsibleCfg="/absolute/path/to/ansible.cfg"\n\n# Fill in the absolute path to your "site.yml"\n\n# AnsiblePlaybook="/absolute/path/to/site.yml"\n\n# If you use tags to provision or configure your matrix host, you can add them\n# here. Use a comma separated string without spaces.\n\n# AnsibleTags="MyTag,MyOtherTag"\n\n[API]\n# If your matrix server is deployed, you may want to fill out the API section.\n# It enables matrixctl to run more and faster commands. You can deploy and\n# provision your Server without this section. You also can cerate a user with\n# "matrixctl adduser --ansible YourUsername" and add your privileges after\n# that.\n\n# Your domain should be something like "michaelsasser.org" without the\n# "matrix." in the front. MatrixCtl will add that, if needed. An IP-Address\n# is not enough.\n\n# Domain="domain.tld"\n\n# To use the API you need to have an administrator account. Enter your Token\n# here. If you use the riot client you will find it your user settings (click\n# on your username on the upper left corner on your browser) in the\n# "Help & About" tab. If you scroll down click next to "Access-Token:" on\n# "<click to reveal>". It will be marked for you. Copy it in here.\n\n# Token="MyMatrixToken"\n```\n\n## Semantic Versioning\n\n**After release "1.0.0"** this repository will use\n[SemVer](https://semver.org/) for its release\ncycle.\n\n**Before release "1.0.0"** it uses "0.MAJOR.MINOR_or_PATCH".\nThis means, if breaking changes are introduced, it results in a major version\nchange (e.g. "0.1.0" -> "0.2.0"). Minor changes, like new features or patches\nare bumping the last digit (e.g. "0.1.1" -> "0.1.2").\n\n## License\nCopyright &copy; 2020 Michael Sasser <Info@MichaelSasser.org>. Released under\nthe GPLv3 license.\n',
    'author': 'Michael Sasser',
    'author_email': 'Michael@MichaelSasser.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MichaelSasser/matrixctl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
