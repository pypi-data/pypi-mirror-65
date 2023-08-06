# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wechatpy',
 'wechatpy.client',
 'wechatpy.client.api',
 'wechatpy.client.api.merchant',
 'wechatpy.crypto',
 'wechatpy.pay',
 'wechatpy.pay.api',
 'wechatpy.session',
 'wechatpy.work',
 'wechatpy.work.client',
 'wechatpy.work.client.api']

package_data = \
{'': ['*']}

install_requires = \
['optionaldict>=0.1.0',
 'python-dateutil>=2.5.2',
 'requests>=2.4.3',
 'xmltodict>=0.11.0']

extras_require = \
{'cryptography': ['cryptography>=2.8,<3.0'],
 'pycrypto': ['pycryptodome>=3.9,<4.0']}

setup_kwargs = {
    'name': 'wechatpy',
    'version': '2.0.0a1',
    'description': 'WeChat SDK for Python',
    'long_description': "      ___       __   _______   ________  ___  ___  ________  _________  ________  ___    ___\n     |\\  \\     |\\  \\|\\  ___ \\ |\\   ____\\|\\  \\|\\  \\|\\   __  \\|\\___   ___\\\\   __  \\|\\  \\  /  /|\n     \\ \\  \\    \\ \\  \\ \\   __/|\\ \\  \\___|\\ \\  \\\\\\  \\ \\  \\|\\  \\|___ \\  \\_\\ \\  \\|\\  \\ \\  \\/  / /\n      \\ \\  \\  __\\ \\  \\ \\  \\_|/_\\ \\  \\    \\ \\   __  \\ \\   __  \\   \\ \\  \\ \\ \\   ____\\ \\    / /\n       \\ \\  \\|\\__\\_\\  \\ \\  \\_|\\ \\ \\  \\____\\ \\  \\ \\  \\ \\  \\ \\  \\   \\ \\  \\ \\ \\  \\___|\\/  /  /\n        \\ \\____________\\ \\_______\\ \\_______\\ \\__\\ \\__\\ \\__\\ \\__\\   \\ \\__\\ \\ \\__\\ __/  / /\n         \\|____________|\\|_______|\\|_______|\\|__|\\|__|\\|__|\\|__|    \\|__|  \\|__||\\___/ /\n                                                                                \\|___|/\n\n[![GitHub Actions](https://github.com/wechatpy/wechatpy/workflows/CI/badge.svg)](https://github.com/wechatpy/wechatpy/actions?query=workflow%3ACI)\n[![codecov.io](https://codecov.io/github/wechatpy/wechatpy/coverage.svg?branch=master)](https://codecov.io/github/wechatpy/wechatpy?branch=master)\n[![Documentation Status](https://readthedocs.org/projects/wechatpy/badge/?version=master)](http://docs.wechatpy.org/zh_CN/master/?badge=master)\n[![PyPI](https://img.shields.io/pypi/v/wechatpy.svg)](https://pypi.org/project/wechatpy)\n[![Downloads](https://pepy.tech/badge/wechatpy)](https://pepy.tech/project/wechatpy)\n[![Reviewed by Hound](https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg)](https://houndci.com)\n\n微信(WeChat) 公众平台第三方 Python SDK。\n\nv1.x:   [【阅读文档】](https://wechatpy.readthedocs.org/zh_CN/stable/) [【快速入门】](https://wechatpy.readthedocs.org/zh_CN/stable/quickstart.html)\nmaster: [【阅读文档】](https://wechatpy.readthedocs.org/zh_CN/master/) [【快速入门】](https://wechatpy.readthedocs.org/zh_CN/master/quickstart.html)\n\n[![Join the chat at https://gitter.im/messense/wechatpy](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/messense/wechatpy?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)\n\n## 功能特性\n\n1. 普通公众平台被动响应和主动调用 API\n2. 企业微信 API\n3. 微信支付 API\n4. 第三方平台代公众号调用接口 API\n5. 小程序云开发 API\n\n## 安装\n\n推荐使用 pip 进行安装:\n\n```bash\npip install wechatpy\n# with cryptography (推荐）\npip install 'wechatpy[cryptography]'\n# with pycryptodome\npip install 'wechatpy[pycrypto]'\n```\n\n升级版本：\n\n    pip install -U wechatpy\n\n\n## 使用示例\n\n使用示例参见 [examples](examples/)\n\n## 贡献代码\n\n请阅读 [贡献代码指南](.github/CONTRIBUTING.md)\n\n## 支持项目\n\n如果觉得本项目对您有帮助，请考虑[捐赠支持项目开发](http://docs.wechatpy.org/zh_CN/master/sponsor.html)\n\n## 问题反馈\n\n我们主要使用 [GitHub issues](https://github.com/wechatpy/wechatpy/issues) 进行问题追踪和反馈。\n\nQQ 群：176596300\n\n![wechatpy QQ 群](https://raw.githubusercontent.com/wechatpy/wechatpy/master/docs/_static/images/qq-group.png)\n\n\n## License\n\nThis work is released under the MIT license. A copy of the license is provided in the [LICENSE](./LICENSE) file.\n",
    'author': 'messense',
    'author_email': 'messense@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wechatpy/wechatpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
