# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiohttp_cache']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6,<4.0', 'aioredis>=1.3,<2.0', 'envparse>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'aiohttp-cache',
    'version': '2.0.2',
    'description': 'A cache system for aiohttp server',
    'long_description': '# Aiohttp-cache\n\n![aiohttp-cache logo](https://raw.githubusercontent.com/cr0hn/aiohttp-cache/master/aiohttp-cache-128x128.png)\n\n\n# What\'s aiohttp-cache\n\n`aiohttp-cache` is a plugin for aiohttp.web server that allow to use a\ncache system to improve the performance of your site.\n\n# How to use it\n\n## With in-memory backend\n\n```python\nimport asyncio\n\nfrom aiohttp import web\n\nfrom aiohttp_cache import (  # noqa\n    setup_cache,\n    cache,\n)\n\nPAYLOAD = {"hello": "aiohttp_cache"}\nWAIT_TIME = 2\n\n\n@cache()\nasync def some_long_running_view(request: web.Request) -> web.Response:\n    await asyncio.sleep(WAIT_TIME)\n    payload = await request.json()\n    return web.json_response(payload)\n\n\napp = web.Application()\nsetup_cache(app)\napp.router.add_post("/", some_long_running_view)\n\nweb.run_app(app)\n```\n\n## With redis backend\n\n**Note**: redis should be available at\n `$CACHE_URL` env variable or`redis://localhost:6379/0`\n\n```python\nimport asyncio\n\nimport yarl\nfrom aiohttp import web\nfrom envparse import env\n\nfrom aiohttp_cache import (  # noqa\n    setup_cache,\n    cache,\n    RedisConfig,\n)\n\nPAYLOAD = {"hello": "aiohttp_cache"}\nWAIT_TIME = 2\n\n\n@cache()\nasync def some_long_running_view(request: web.Request) -> web.Response:\n    await asyncio.sleep(WAIT_TIME)\n    payload = await request.json()\n    return web.json_response(payload)\n\n\napp = web.Application()\nurl = yarl.URL(env.str("CACHE_URL", default="redis://localhost:6379/0"))\nsetup_cache(\n    app,\n    cache_type="redis",\n    backend_config=RedisConfig(\n        db=int(url.path[1:]), host=url.host, port=url.port\n    ),\n)\n\napp.router.add_post("/", some_long_running_view)\n\nweb.run_app(app)\n```\n\n## Example with a custom cache key\n\nLet\'s say you would like to cache the requests just by the method and\njson payload, then you can setup this as per the follwing example.\n\n**Note** default key_pattern is:\n\n```python\nDEFAULT_KEY_PATTERN = (\n    AvailableKeys.method,\n    AvailableKeys.host,\n    AvailableKeys.path,\n    AvailableKeys.postdata,\n    AvailableKeys.ctype,\n)\n```\n\n```python\nimport asyncio\n\nfrom aiohttp import web\n\nfrom aiohttp_cache import setup_cache, cache, AvailableKeys  # noqa\n\nPAYLOAD = {"hello": "aiohttp_cache"}\nWAIT_TIME = 2\n\n\n@cache()\nasync def some_long_running_view(request: web.Request) -> web.Response:\n    await asyncio.sleep(WAIT_TIME)\n    payload = await request.json()\n    return web.json_response(payload)\n\n\ncustom_cache_key = (AvailableKeys.method, AvailableKeys.json)\n\napp = web.Application()\nsetup_cache(app, key_pattern=custom_cache_key)\napp.router.add_post("/", some_long_running_view)\n\nweb.run_app(app)\n```\n\n# License\n\nThis project is released under BSD license. Feel free\n\n# Source Code\n\nThe latest developer version is available in a github repository:\n<https://github.com/cr0hn/aiohttp-cache>\n\n# Development environment\n\n1.  docker-compose run tests\n',
    'author': 'Daniel Garcia (cr0hn)',
    'author_email': 'cr0hn@cr0hn.com',
    'maintainer': 'Daniel Garcia (cr0hn)',
    'maintainer_email': 'cr0hn@cr0hn.com',
    'url': 'https://github.com/cr0hn/aiohttp-cache',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
