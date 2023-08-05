# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spotifier']

package_data = \
{'': ['*']}

install_requires = \
['mypy_extensions>=0.4.3,<0.5.0', 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'spotifier',
    'version': '0.1.0',
    'description': 'A Spotify Web API Library for Modern Python',
    'long_description': '# Spotifier\n\n:notes: A Spotify Web API Library for Modern Python\n\n## Notice\n\nI do not recommend using this package as it is not yet ready for use.\n\n## Feature\n\n- All functions supports type hint (Up to the level of TypedDict!)\n- Reproduce API documentation with code as much as possible (You can handle errors w/o wasting requests!)\n\n## Install\n\n```sh\npip install git+https://github.com/skmatz/spotifier.git\n```\n\n## Quick Start\n\n```python\nimport os\nimport webbrowser  # to open URL in browser\n\nfrom spotifier import Spotify\nfrom spotifier.oauth import SpotifyAuthorizationCode\n\n\noauth = SpotifyAuthorizationCode(\n    client_id=os.environ["SPOTIFY_CLIENT_ID"],\n    client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],\n    redirect_uri=os.environ["SPOTIFY_REDIRECT_URI"],\n)\n\nwebbrowser.open(oauth.get_authorize_url())\nurl = input("Input redirected URL: ")\n\ncode = oauth.parse_response_code(url)\noauth.set_token(code)\n\nclient = Spotify(oauth)\n\nprint(client.get_current_users_profile()["display_name"])  # your Spotify nickname\n```\n\n## Supported API\n\n- [x] Authorization Code Flow\n- [ ] Client Credentials Flow\n',
    'author': 'Shunta Komatsu',
    'author_email': 'shuntak217@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/skmatz/spotifier',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
