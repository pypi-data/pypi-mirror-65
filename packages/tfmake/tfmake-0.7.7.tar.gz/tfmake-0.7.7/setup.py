# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tfmake', 'tfmake.custom']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'pathlib>=1.0.1,<2.0.0', 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['tfmake = tfmake.cli:main']}

setup_kwargs = {
    'name': 'tfmake',
    'version': '0.7.7',
    'description': 'Python based Makefile wrapper for terraform projects',
    'long_description': '# tfmake\n\nThis is a Python based wrapper around an opionated `Makefile` I use for `terraform` projects. \n\nYou still need `make`, though. The main advantage is that you don\'t have to copy the `Makefile`. \n\n## DISCLAIMER\nThis module includes a highly opinionated `Makefile` implementation. It\'s working very well for us, but your requirements might be different.\n\n## Install\n\n```\n$ pip install tfmake\n```\n\n## Usage\n> Here\'s the help for the wrapper\n```\n$ tfmake --help\nUsage: tfmake [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --version  Show the version and exit.\n  --help     Show this message and exit.\n\nCommands:\n  aws\n  azure\n```\n\n## Providers\nCurrently, `tfmake` supports two providers: `aws` and `azure`. The default provider is `aws`. Depending on the selected provider, a different, provider specific, `Makefile` is used to wrap `terraform`. Here, the provider is selected by using the right command.\n\nSee \'examples\' for some ... examples.\n\nEach provider leads to a specific `Makefile`. For example: `provider==azure` leads to using `Makefile.azure`.\n\n## Provider Authentication\nThe used `Makefile` will _not_ handle authentication. It just assumes you\'re using an authenticated context.\n\nFor, `aws`, I use [`aws-vault`](https://github.com/99designs/aws-vault). For `azure`, I use the [`azure-cli`](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest).\n\n> Here\'s the help for the (bundled) Makefile\n```\n$ tfmake help\nThe AWS Edition\n\nUsage: make <TARGET> (env=<ENVIRONMENT>) (args=<TERRAFORM ARGUMENTS>)\n\nWhere:\n\t- ENVIRONMENT is one of [\'dev\',\'tst\',\'acc\',\'prd\']\n\t- TARGET is one:\nupdate                          Update terraform modules and providers\nselect                          Select and initialize terraform workspace (aka \'stage\')\nshow                            Show current terraform workspace\nplan                            Generate and show an execution plan\napply                           Builds or changes infrastructure\ndestroy                         Destroy Terraform-managed infrastructure\nrefresh                         Refresh terraform state\n\nNote:\n\n- parameter \'env\' is only required when selecting an environment\n- parameter \'args\' can be used to pass terraform understandable arguments. Example: "make apply args=\'-input=false -no-color -auto-approve\'"\n```\n\n> Use `tfmake azure help` to see the `azure` edition ...\n\n## Final Notes\n\nBy default, before any a `terraform` command is executed, you will be asked to confirm the usage of the current environment.\n\n```\n$ tfmake azure apply\n\nUsing workspace \'prd\' on \'My_fancy_Azure_Production_subscription\'.\n\nPress [ENTER] to continue or [CTRL-C] to stop.\n```\n\nPlease notice that the prompt shows the selected `terraform` workspace and the alias/name of the provider account.\n\n> Use `TFMAKE_AGREE=whatever` to auto confirm that prompt ...\n\n## Example\n\n> Initialise \'dev\' environment\n```\n$ aws-vault exec foobar -- tfmake select env=dev\n```\n\n> Plan changes\n```\n$ aws-vault exec foobar -- tfmake plan\n```\n\n> Apply changes\n```\n$ aws-vault exec foobar -- tfmake apply\n```\n\n> Apply changes using the `azure` provider\n```\n$ az login\n# (optionaly set subscription)\n$ az account set --subscription=YOUR_SUBSCRIPTION_ID_HERE\n$ tfmake azure apply\n```\n\n> Apply changes ... automagically\n```\n$ aws-vault exec foobar -- tfmake apply args=\'-no-color -auto-approve\'\n```\n\n**Note**: the `args` parameter can be used for arbitrary Terraform arguments.\n\n~ the end',
    'author': 'Pascal Prins',
    'author_email': 'pascal.prins@foobar-it.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/paprins/tfmake',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*',
}


setup(**setup_kwargs)
