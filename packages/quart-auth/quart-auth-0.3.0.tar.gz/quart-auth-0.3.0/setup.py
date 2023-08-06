# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['quart_auth']

package_data = \
{'': ['*']}

install_requires = \
['quart>=0.11']

setup_kwargs = {
    'name': 'quart-auth',
    'version': '0.3.0',
    'description': 'A Quart extension to provide secure cookie authentication',
    'long_description': 'Quart-Auth\n==========\n\n|Build Status| |docs| |pypi| |python| |license|\n\nQuart-Auth is an extension for `Quart\n<https://gitlab.com/pgjones/quart>`_ to provide for secure cookie\nauthentication (session management). It allows for a session to be\nlogged in, authenticated and logged out.\n\nUsage\n-----\n\nTo use Quart-Auth with a Quart app you have to create an AuthManager and\ninitialise it with the application,\n\n.. code-block:: python\n\n    app = Quart(__name__)\n    AuthManager(app)\n\nor via the factory pattern,\n\n.. code-block:: python\n\n    auth_manager = AuthManager()\n\n    def create_app():\n        app = Quart(__name__)\n        auth_manager.init_app(app)\n        return app\n\nIn addition you will need to configure Quart-Auth, which defaults to\nthe most secure. At a minimum you will need to set secret key,\n\n.. code-block:: python\n\n    app.secret_key = "secret key"  # Do not use this key\n\nwhich you can generate via,\n\n.. code-block:: python\n\n    >>> import secrets\n    >>> secrets.token_urlsafe(16)\n\nTou may also need to disable secure cookies to use in development, see\nconfiguration below.\n\nWith AuthManager initialised you can use the ``login_required``\nfunction to decorate routes that should only be accessed by\nauthenticated users,\n\n.. code-block:: python\n\n    from quart_auth import login_required\n\n    @app.route("/")\n    @login_required\n    async def restricted_route():\n        ...\n\nYou can also use the ``login_user``, and ``logout_user`` functions to\nstart and end sessions for a specific ``AuthenticatedUser`` instance,\n\n.. code-block:: python\n\n    from quart_auth import AuthUser, login_user, logout_user\n\n    @app.route("/login")\n    async def login():\n        # Check Credentials here, e.g. username & password.\n        ...\n        # We\'ll assume the user has an identifying ID equal to 2\n        login_user(AuthUser(2))\n        ...\n\n    @app.route("/logout")\n    async def logout():\n        logout_user()\n        ...\n\nThe user (authenticated or not) is available via the global\n``current_user`` including within templates,\n\n.. code-block:: python\n\n    from quart import render_template_string\n    from quart_auth import current_user\n\n    @app.route("/")\n    async def user():\n        return await render_template_string("{{ current_user.is_authenticated }}")\n\nContributing\n------------\n\nQuart-Auth is developed on `GitLab\n<https://gitlab.com/pgjones/quart-auth>`_. You are very welcome to\nopen `issues <https://gitlab.com/pgjones/quart-auth/issues>`_ or\npropose `merge requests\n<https://gitlab.com/pgjones/quart-auth/merge_requests>`_.\n\nTesting\n~~~~~~~\n\nThe best way to test Quart-Auth is with Tox,\n\n.. code-block:: console\n\n    $ pip install tox\n    $ tox\n\nthis will check the code style and run the tests.\n\nHelp\n----\n\nThis README is the best place to start, after that try opening an\n`issue <https://gitlab.com/pgjones/quart-auth/issues>`_.\n\n\n.. |Build Status| image:: https://gitlab.com/pgjones/quart-auth/badges/master/pipeline.svg\n   :target: https://gitlab.com/pgjones/quart-auth/commits/master\n\n.. |docs| image:: https://img.shields.io/badge/docs-passing-brightgreen.svg\n   :target: https://pgjones.gitlab.io/quart-auth/\n\n.. |pypi| image:: https://img.shields.io/pypi/v/quart-auth.svg\n   :target: https://pypi.python.org/pypi/Quart-Auth/\n\n.. |python| image:: https://img.shields.io/pypi/pyversions/quart-auth.svg\n   :target: https://pypi.python.org/pypi/Quart-Auth/\n\n.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg\n   :target: https://gitlab.com/pgjones/quart-auth/blob/master/LICENSE\n',
    'author': 'pgjones',
    'author_email': 'philip.graham.jones@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/pgjones/quart-auth/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
