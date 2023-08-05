# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['roboto']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0',
 'typing-extensions>=3.7.4,<4.0.0',
 'typing-inspect>=0.5.0,<0.6.0',
 'validators>=0.14.2,<0.15.0']

setup_kwargs = {
    'name': 'roboto-telegram',
    'version': '0.1.1',
    'description': 'A type-hinted async Telegram bot library.',
    'long_description': "Roboto\n======\n\n![](https://github.com/tarcisioe/roboto/workflows/CI/badge.svg)\n[![codecov](https://codecov.io/gh/tarcisioe/roboto/branch/master/graph/badge.svg)](https://codecov.io/gh/tarcisioe/roboto)\n\nA type-hinted async Telegram bot library.\n\nRoboto's API is not perfectly stable nor complete yet. It will be kept a 0.x.0\nuntil the Telegram Bot API is completely implemented, and will be bumped to\n1.0.0 when it is complete.\n\n\nBasic usage\n===========\n\nRoboto is still a low-level bot API, meaning it does not provide much\nabstraction over the Bot API yet (that is planned, though).\n\nCurrently, a basic echo bot with roboto looks like:\n\n```python\nfrom roboto import Token, BotAPI\n\nfrom asyncio import run\n\n\napi_token = Token('your-bot-token')\n\n\nasync def main() -> None:\n    bot = BotAPI(api_token)\n\n    offset = 0\n\n    while True:\n        updates = await bot.get_updates(offset)\n\n        for update in updates:\n            if update.message is not None and update.message.text is not None:\n                await bot.send_message(\n                    update.message.chat.id,\n                    update.message.text,\n                )\n\n        if updates:\n            offset = updates[-1].update_id + 1\n\nrun(main())\n```\n\nBeing statically-typed, Roboto supports easy autocompletion and `mypy` static\nchecking.\n\n\nGoals\n=====\n\nPrinciples\n----------\n\n- Ease of static checking for client code, especially static typing.\n- Forwards compatibility (additions to the bot HTTP API should not break older\n  versions of Roboto easily).\n\nNext milestones\n---------------\n\n- [ ] Full Telegram Bot API implementation.\n- [ ] High-level API (abstraction for command handlers, necessary internal\n      state, etc.).\n- [ ] Support for other async runtimes other than asyncio (especially\n      [`trio`](https://github.com/python-trio/trio)).\n",
    'author': 'Tarcísio Eduardo Moreira Crocomo',
    'author_email': 'tarcisioe@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
