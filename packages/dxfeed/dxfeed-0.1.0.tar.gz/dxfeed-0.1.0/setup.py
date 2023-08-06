# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dxfeed',
 'dxfeed.core',
 'dxfeed.core.listeners',
 'dxfeed.core.pxd_include',
 'dxfeed.core.utils']

package_data = \
{'': ['*'],
 'dxfeed': ['dxfeed-c-api/*',
            'dxfeed-c-api/include/*',
            'dxfeed-c-api/include/pthreads/*',
            'dxfeed-c-api/src/*']}

install_requires = \
['pandas>=0.25.1,<0.26.0']

setup_kwargs = {
    'name': 'dxfeed',
    'version': '0.1.0',
    'description': 'DXFeed Python API via C API',
    'long_description': "# dxfeed package\n\nThis package provides access to [dxFeed](https://www.dxfeed.com/) streaming data.\nThe library is build as a thin wrapper over [dxFeed C-API library](https://github.com/dxFeed/dxfeed-c-api).\nWe use [Cython](https://cython.org/) in this project as it combines flexibility, reliability and\nusability in writing C extensions.\n\nThis package already contains basic C-API functions related to creating connections, subscriptions etc.\nMoreover default listeners (functions responsible for event processing) are ready to use. The user is also able to\nwrite his own custom listener in Cython\n\n## Installation\n\n**Requirements:** python >3.6, cython, pandas\n\n```python\npip3 install cython pandas\n```\n\nInstall package itself with PyPI\n\n```python\npip3 install dxfeed\n```\n\nor with tar.gz artifact\n\n```python\npip3 install dxfeed-x.x.x.tar.gz\n``` \n\n---\n**NOTE**\n\nMacOS is not supported yet\n\n---\n\n## Basic usage\n\nAll the functions in C API have similar ones in Python with the same name. Not all arguments are\nsupported by now, this work is in progress.\n\n**Import dxfeed library**:\n\n```python\nimport dxfeed as dx\n``` \n\n**Create connection**:\n\n```python\ncon = dx.dxf_create_connection(address='demo.dxfeed.com:7300')\n```\n\n**Create one or several subscriptions of certain event types**:\n```python\nsub1 = dx.dxf_create_subscription(con, 'Trade')\nsub2 = dx.dxf_create_subscription(con, 'Quote')\n```\n'Trade', 'Quote', 'Summary', 'Profile', 'Order', 'TimeAndSale', 'Candle', 'TradeETH', 'SpreadOrder',\n'Greeks', 'TheoPrice', 'Underlying', 'Series', 'Configuration' event types are supported.\n\n**Add tickers you want to get data for**:\n```python\ndx.dxf_add_symbols(sub1, ['AAPL', 'MSFT'])\ndx.dxf_add_symbols(sub2, ['AAPL', 'C'])\n```\n\n**Attach listeners**:\n```python\ndx.dxf_attach_listener(sub1)\ndx.dxf_attach_listener(sub2)\n```\n\n`dxfeed` has default listeners for each event type, but you are able to write \nyour custom one. You can find how to do it at `example/Custom listener example.ipynb`.\n\n**Look at the data**:\n```python\nsub1.get_data()\nsub2.get_data()\n```\nThe data is stored in Subscription class. You can also turn dict to pandas DataFrame simply calling\n`sub1.to_dataframe()`.\n\n**Detach the listener, if you want to stop recieving data**:\n```python\ndx.dxf_detach_listener(sub1)\ndx.dxf_detach_listener(sub2)\n```\n\n**Finally, close your connection**:\n```python\ndx.dxf_close_connection(con)\n```\n",
    'author': 'Ivan Mishalkin',
    'author_email': 'ivan.mishalkin@devexperts.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
