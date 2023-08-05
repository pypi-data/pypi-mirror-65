# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ingraph', 'ingraph.cli', 'ingraph.engine']

package_data = \
{'': ['*'], 'ingraph': ['aws/*']}

install_requires = \
['click>=7.1.1,<8.0.0',
 'more-itertools>=8.2.0,<9.0.0',
 'mypy>=0.770,<0.771',
 'networkx>=2.4,<3.0',
 'parso>=0.6.2,<0.7.0',
 'ruamel.yaml>=0.16.10,<0.17.0']

entry_points = \
{'console_scripts': ['ig = ingraph.cli:main']}

setup_kwargs = {
    'name': 'ingraph',
    'version': '0.1.1',
    'description': 'InGraph is an Infrastructure Graph DSL for AWS CloudFormation.',
    'long_description': '<p align="center"> \n  <img src="https://lifa.dev/img/ingraph/ingraph.png" alt="InGraph"/>\n</p>\n\n# [InGraph][website] &middot; [![Version][badge-version]][version] [![License][badge-license]][license]\n\n> InGraph ain\'t template generator :stuck_out_tongue_winking_eye:\n\nInGraph is a Declarative Infrastructure Graph DSL for AWS\nCloudFormation.\n\n-   **Declarative**: Never again abstract away from CloudFormation.\n    Simply declare your infrastructure components, without the hassle of\n    YAML, and preserve the strict semantic of the AWS CloudFormation\n    language. Veterans, build on top of your knowledge. Beginners, learn\n    CloudFormation effectively.\n\n-   **Composable**: Create encapsulated components with their assets and\n    dependencies, then share or compose them to build more complex\n    infrastructures. From simple nodes to your whole graph, everything\n    is a deployable infrastructure unit.\n\n-   **Integrated**: Leverage the evergrowing Python ecosystem. Benefit\n    from static type checking, take advantage of autocompletion in your\n    editor, or even consume open infrastructure components via the\n    Python Package Index, among others.\n\n[Learn how to use InGraph in your own project][overview].\n\n## Installation\n\nInGraph requires [Python 3.8][python] or newer. Feel free to use your\nfavorite tool or [`pip`][pip] to install the\n[`ingraph` package][version].\n\n```\npython3.8 -m pip install --user ingraph\n```\n\nVerify your installation by invoking the `ig` command. You should see\na welcome screen.\n\n## Example\n\nWe have several examples on the [website][website]. Here is the first\none to whet your appetite.\n\n```\nig cfn -i example.py -r HelloWorld -o example.yaml\n```\n\n![InGraph Example](https://lifa.dev/img/ingraph/example.png)\n\nThis example creates a simple AWS Lambda function that returns a\n"Hello, World!" message.\n\nYou\'ll notice that CloudFormation parameters, along with their types and\ndefault values are simple constructor parameters, or that CloudFormation\noutputs are class attributes, or even that CloudFormation resource names\nare derived from variable names. It\'s only a taste of\n[what is in store][overview] for you.\n\n## Contributing\n\nThe primary purpose of this project is to continue to evolve the core of\nInGraph. We are grateful to the community for any contribution. You may,\nfor example, proof-read the documentation, submit bugs and fixes,\nprovide improvements, discuss new axes of evolution, or spread the word\naround you.\n\n## Thanks\n\nWe want to thank and express our gratitude to [Ben Kehoe][ben]. Without\nhis guidance and support, this project wouldn\'t have been possible.\n\n## License\n\nUnless otherwise stated, the source code of the project is released\nunder the [GNU Affero General Public License Version 3][agplv3]. Please\nnote, however, that all public interfaces subject to be embedded within\nthe source code of your infrastructure are released under the [Apache\nLicense Version 2][apachev2]. Refer to the header of each file or to the\nLICENSE file present in the parent directory where appropriate.\n\n[badge-version]: https://img.shields.io/badge/version-0.1.1-blue?style=flat-square\n[version]: https://pypi.org/project/ingraph/0.1.1/\n[badge-license]: https://img.shields.io/badge/license-AGPL3%2FApache2-blue?style=flat-square\n[license]: https://github.com/lifadev/ingraph#license\n[website]: https://lifa.dev/ingraph\n[agplv3]: https://www.gnu.org/licenses/agpl-3.0.txt\n[apachev2]: http://www.apache.org/licenses/LICENSE-2.0.txt\n[overview]: https://lifa.dev/docs/ingraph/overview\n[example]: https://raw.githubusercontent.com/lifadev/ingraph/master/example.png\n[python]: https://www.python.org/downloads/\n[pip]: https://pip.pypa.io/en/stable/\n[ben]: https://twitter.com/ben11kehoe\n',
    'author': 'lifa.dev',
    'author_email': 'croak@lifa.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://lifa.dev/ingraph',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
