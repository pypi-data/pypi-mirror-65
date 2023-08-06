# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jse']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['jse = jse.jse:main']}

setup_kwargs = {
    'name': 'jse',
    'version': '0.0.5',
    'description': 'quickly edit json files from the command line',
    'long_description': '# jse - JSON Editor [![Build Status](https://travis-ci.org/bjubes/jse.svg?branch=master)](https://travis-ci.org/bjubes/jse)\n\n\nquickly edit json files from the command line\n\njse is pragmatic and terse. It lets you edit json fast, without needing to care about quotes, types, exact indexes, or any of the stuff that makes json a pain.\n## Usage\n```\n$ jse <file> <mode> <key> <value>\n```\n#### TLDR Version\nedit an existing key: ``` -e --edit```\n```\n$ jse config.json --edit app.version 0.3.3\n```\nadd a new element: ``` -a --add```\n```\n$ jse todo.json --add list.shopping {task:eggs,done:false}\n```\ndelete a value: ``` -d --delete```\n```\n$ jse problems.json --delete problems[99]\n```\nfull [examples with json files](#examples) below\n\n## Installing\n\ncomming soon - pip install :)\n\n### Running from Source\nrequiremets:\n- python 3\n\nsteps:\n\n1. clone the repository\n2. make it executable `chmod +x jse.py`\n3. put in on the path `ln -s /path/to/jse.py ~/.local/bin/jse`\n\njse has no package dependencies (it literally just edits json), but does use pytest for tests.\n\n\n## Examples\nlets start with a json file\n```json\n# example.json\n{\n    "users": [\n        {"name": "alice", "age": 21, "admin": false},\n        {"name": "bob", "age": 57, "admin": true},\n        {"name": "charlie", "age": 37, "admin": false}\n    ]\n}\n```\n\nWe want to delete the user alice using jse. All we need to do is specify `-d` or `--delete` mode and the path to her `user` object\n```\n$ jse example.json -d users[0]\n```\nwe can use both index or dot notation\n```\n$ jse example.json -d users.0\n```\n```json\n# example.json\n{\n    "users": [\n        {"name": "bob", "age": 57, "admin": true},\n        {"name": "charlie", "age": 37, "admin": false}\n    ]\n}\n```\nnow lets make charlie an admin. To edit an existing field we use the edit command with `-e` or `--edit`. Edit takes a key to change and its new value.\n```\n$ jse example.json -e users.1.admin true\n```\n```json\n# example.json\n{\n    "users": [\n        {"name": "bob", "age": 57, "admin": true},\n        {"name": "charlie", "age": 37, "admin": true}\n    ]\n}\n```\njse is smart enough to infer datatypes from the command line. it can also accept complex nested objects and arrays in a terse, quote-free format. Lets add a new nested field to the file with `--add` or `-a`\n```\n$ jse example.json -a highscore [{score:32.5,user:bob,metadata:{ip:192.168.1.102,client:firefox}}]\n```\n```json\n{\n    "users": [\n        {"name": "bob", "age": 57, "admin": true},\n        {"name": "charlie", "age": 37, "admin": true}\n    ],\n    "highscore": [\n        {\n            "score": "32.5",\n            "user": "bob",\n            "metadata": {\n                "ip": "192.168.1.102",\n                "client": "firefox"\n            }\n        }\n    ]\n}\n```\njse also understands lists, so we can add new elements to a one without needing an explicit index. It will infer we are trying to append from `--add` instead of changing the list to an object (`--edit`)\n```\n$ jse example.json -a highscore {"score":52,"user": "charlie"}\n```\n```json\n{\n    "users": [\n        {"name": "bob", "age": 57, "admin": true},\n        {"name": "charlie", "age": 37, "admin": true}\n    ],\n    "highscore": [\n        {\n            "score": "32.5",\n            "user": "bob",\n            "metadata": {\n                "ip": "192.168.1.102",\n                "client": "firefox"\n            }\n        },\n        {\n            "score": 52.0,\n            "user": "charlie"\n        }\n    ]\n}\n```\nerror messages are also meant to be informative, because no one wants a KeyError\n```\n$ jse example.json -a users.0.name "not bob"\n\'name\' already has a value. Use --edit to modify it\n```\n```\n$ jse example.json -d users[2]\nThere is no element with index 2. The largest index is 1\n```\n\nYou can also delete mulitple keys using -d, by passing them seperately\n```\n$ jse example.json -d users.0.age users.1.age\n```\n```json\n{\n    "users": [\n        {\n            "name": "bob",\n            "admin": true,\n        },\n        {\n            "name": "charlie",\n            "admin": true\n        }\n    ]\n    ...\n}\n```\n',
    'author': 'Brian Jubelirer',
    'author_email': 'brian2386@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bjubes/jse',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
