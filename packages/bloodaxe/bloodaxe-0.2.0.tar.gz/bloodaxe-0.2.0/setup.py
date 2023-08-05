# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['bloodaxe']
install_requires = \
['httpx>=0.12.1,<0.13.0',
 'jinja2>=2.11.1,<3.0.0',
 'tabulate>=0.8.7,<0.9.0',
 'toml>=0.10.0,<0.11.0',
 'typer[all]>=0.1.0,<0.2.0']

entry_points = \
{'console_scripts': ['bloodaxe = bloodaxe:app']}

setup_kwargs = {
    'name': 'bloodaxe',
    'version': '0.2.0',
    'description': 'bloodaxe is the nice way to testing and metrifying api flows.',
    'long_description': '[![CircleCI](https://circleci.com/gh/rfunix/bloodaxe.svg?style=svg)](https://circleci.com/gh/rfunix/bloodaxe)\n\n\n![bloodaxe logo](/images/logo.png)\n\n`bloodaxe` is the nice way to testing and metrifying api flows.\n\n![GIF demo](images/demo.gif)\n\n**Usage**\n---\n\n```\nUsage: bloodaxe.py [OPTIONS] CONFIG_FILE\n\nOptions:\n  --install-completion  Install completion for the current shell.\n  --show-completion     Show completion for the current shell, to copy it or\n                        customize the installation.\n\n  --help                Show this message and exit.\n```\n`$ bloodaxe example.toml`\n\n**Installation Options**\n---\n\nInstall with [`pip`](https://pypi.org/project/bloodaxe/)\n\n`$ pip install bloodaxe`\n\n`$ bloodaxe`\n\n**Flow configuration examples**\n---\n```toml\n[configs]\nnumber_of_concurrent_flows = 10 # Number of concurrent coroutines flows\nduration = 60 # Stressing duration\n\n[[api]] # Api context\nname = "user_api"\nbase_url = "http://127.0.0.1:8080" # Base url at the moment, is the unique parameter in api section.\n[api.envvars] # Environment variables for given api\nclient_id = "CLIENT_ID" # Envvars names\nclient_secret = "CLIENT_SECRET"\n\n[[api]]\nname = "any_api"\nbase_url = "http://127.0.0.1:1010"\n\n[[request]] # Request context\nname = "get_token" \nurl = "{{ user_api.base_url }}/token/" # Use user_api context to get the base_url\nmethod = "POST"\ntimeout = 60 # The bloodaxe default timeout value is 10 secs, but it\'s possible override the default value\nsave_result = true # Save request result in request name context, default value is false\n[request.data] # Request data section\nclient_id = "{{ user_api.client_id }}" # templating syntax is allowed in request.data\nclient_secret = "{{ user_api.client_secret }}"\n[request.headers] # Request header section\nContent-Type = \'application/x-www-form-urlencoded\'\n\n[[request]]\nname = "get_user"\nurl = "{{ user_api.base_url }}/users/1"\nmethod = "GET"\ntimeout = 60\nsave_result = true\n[request.headers]\nAuthorization = "{{ get_token.access_token}}" # templating syntax is allowed in request.headers\n\n[[request]]\nname ="get_user_with_params"\nurl = "{{ user_api.base_url }}/users/"\nmethod = "GET"\ntimeout = 60\nsave_result = false\n[request.params] # Request params section\nname = "{{ get_user.name }}" # templating syntax is allowed in request.params/querystring\n[request.headers]\nAuthorization = "{{ get_token.access_token}}"\n\n[[request]]\nname = "create_new_user"\nurl = "{{  user_api.base_url }}/users/"\nmethod = "POST"\n[request.data]\nfirstname = "{{ get_user.firstname }} test"\nlastname = "{{ get_user.Lastname }} test"\nstatus = "{{ get_user.status }} test"\n[request.headers]\nAuthorization = "{{ get_token.access_token}}"\n[request.response_check] # response_check feature checking response data and status_code\nstatus_code = 201\n[request.response_check.data]\nfirstname = "{{ get_user.firstname }} test" # templating syntax is allowed in response data checks\nlastname = "{{ get_user.Lastname }} test"\nstatus = "{{ get_user.status }} test"\n\n[[request]]\nname = "create_new_user_with_from_file"\nurl = "{{  user_api.base_url }}/users/"\nmethod = "PATCH"\n[request.data]\nfrom_file = "user.json" # from_file help you configure request.data\n[request.headers]\nAuthorization = "{{ get_token.access_token}}"\n```\n\n**Backlog**\n---\nhttps://github.com/rfunix/bloodaxe/projects/1\n',
    'author': 'rfunix',
    'author_email': 'rafinha.unix@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
