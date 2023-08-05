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
 'requests>=2.23.0,<3.0.0',
 'tabulate>=0.8.7,<0.9.0']

entry_points = \
{'console_scripts': ['matrixctl = matrixctl.application:main']}

setup_kwargs = {
    'name': 'matrixctl',
    'version': '0.1.2',
    'description': 'Controls a synapse oci-container instance via ansible',
    'long_description': '![GitHub](https://img.shields.io/github/license/MichaelSasser/matrixctl?style=flat-square)\n\n# MatrixCtl\n\nMatrixCtl is a python program to control, manage, provision and deploy our\nmatrix homeserver. I had a bunch of shell scripts doing that. Two weeks\nafter using them I couldn\'t remember the order in which I have to use the\narguments. It was a pain. So I decided I hack something together fast.\n\nIt is not the most elegant piece of software I wrote, but it should do the\ntrick for now. I will continue to port the rest of the scripts. Maybe\nit is also useful for someone else.\n\n```\n# matrixctl\nusage: matrixctl [-h] [--version] [-d] {adduser,list-users,deluser,deploy,update,maintainance} ...\n\npositional arguments:\n  {adduser,list-users,deluser,deploy,update,maintainance}\n    adduser             Add a user\n    list-users          Lists users\n    deluser             Deletes a user\n    deploy              Provision and deploy\n    update              Updates the ansible repo\n    maintainance        Run Maintainance tasks\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --version             show program\'s version number and exit\n  -d, --debug           Enables debugging mode.\n```\n\n## Configuration File\n\nTo use this program you need to have this config file in\n"/etc/matrixctl/config" or in "~/.config/matrixctl/config".\n\n```toml\n[ANSIBLE]\n# The absolute path to the fully configured matrix-docker-ansible-deploy\n# playbook.\n\nMatrixDockerAnsibleDeployPath="/absolut/path/to/matrix-docker-ansible-deploy"\n\n[SERVER]\n# If you have your own playbook, to provision your matrix server, you can\n# fill out the server section. matrixctl will run it before the\n# matrix-docker-ansible-deploy playbook.\n\n# AnsibleCfg="/absolut/path/to/ansible.cfg"\n# AnsiblePlaybook="/absolut/path/to/site.yml"\n# AnsibleTags="MyTag,MyOtherTag"\n\n[API]\n# If your matrix server is deployed, you may want to fill out the API section.\n# It enables matrixctl to run more and faster commands. You can deploy and\n# provision your Server without this section. You also can cerate a user with\n# "matrixctl adduser --ansible YourUsername" and add your privileges after\n# that.\n\n# Domain="domain.tld"\n# Token="MyMatrixToken"\n```\n\n## License\nCopyright &copy; 2020 Michael Sasser <Info@MichaelSasser.org>.\nReleased under the GPLv3 license.\n',
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
