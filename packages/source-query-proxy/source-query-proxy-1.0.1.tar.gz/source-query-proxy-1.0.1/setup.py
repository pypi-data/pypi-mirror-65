# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['source_query_proxy', 'source_query_proxy.source']

package_data = \
{'': ['*']}

install_requires = \
['async-timeout>=3.0,<4.0',
 'asyncio_dgram>=1.0,<2.0',
 'backoff>=1.10,<2.0',
 'click>=7.0,<8.0',
 'pid>=2.2,<4.0',
 'pydantic[dotenv]>=1.4,<2.0',
 'pylru>=1.2.0,<2.0.0',
 'pyroute2>=0.5.10,<0.6.0',
 'python-dotenv>=0.10.3,<0.11.0',
 'pyyaml>=5.2,<6.0',
 'sentry-sdk>=0.14.3,<0.15.0',
 'uvloop==0.14.0']

entry_points = \
{'console_scripts': ['sqproxy = source_query_proxy.cli:sqproxy']}

setup_kwargs = {
    'name': 'source-query-proxy',
    'version': '1.0.1',
    'description': 'Async proxy for Source Engine Query Protocol',
    'long_description': '\nsource-query-proxy\n==================\n\nCredits\n-------\n\nSource Engine messages inspired by **Python-valve**\nhttps://github.com/serverstf/python-valve\n\nPrerequisites\n-------------\n\nPython 3.7 or above\n\nYou can use `pyenv <https://github.com/pyenv/pyenv>`_ to install any version of Python without root privileges\n\nInstalling\n----------\n\n.. code-block:: bash\n\n    pip install source-query-proxy==1.0.1\n\nConfiguring\n-----------\n\nsqproxy search configs in ``/etc/sqproxy/conf.d`` and ``./conf.d`` directories.\nYou should place your config files only in this directories.\n\nFor more info see `examples <examples/conf.d>`_\n\nRun\n---\n\n.. code-block:: bash\n\n    sqproxy run\n\n\nRun with eBPF\n-------------\n\nhttps://github.com/spumer/source-query-proxy-kernel-module/tree/master/src-ebpf\n\n1. Download eBPF script and copy ``src-ebpf`` folder to target working directory\n\n2. Install requirements https://github.com/spumer/source-query-proxy-kernel-module/tree/master/src-ebpf/README.md\n\n3. Enable eBPF in config (see examples/00-globals.yaml)\n\n4. Run\n\n.. code-block:: bash\n\n    sqproxy run\n\n\nDevelopment\n-----------\n\n.. code-block:: bash\n\n    git clone https://github.com/spumer/source-query-proxy.git\n    cd source-query-proxy\n    poetry install\n',
    'author': 'spumer',
    'author_email': 'spumer-tm@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/spumer/source-query-proxy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
