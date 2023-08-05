[![PyPI version](https://badge.fury.io/py/easys-ordermanager.svg)](https://badge.fury.io/py/easys-ordermanager)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Lektor.svg)](https://pypi.org/project/easys-ordermanager/)
[![Travis CI build status](https://travis-ci.org/RegioHelden/easys-ordermanager.svg)](https://travis-ci.org/RegioHelden/easys-ordermanager)
[![Coverage Status](https://coveralls.io/repos/github/RegioHelden/easys-ordermanager/badge.svg?branch=add_coveralls)](https://coveralls.io/github/RegioHelden/easys-ordermanager?branch=add_coveralls)

# EasyS order manager API

Compatible with
- Django Rest Framework: 3.8, 3.9, 3.10, 3.11
- Django: 1.11, 2.2 (Not yet for 3.x)
- Python: 3.6, 3.7, 3.8


## Relasing new version
- Update CHANGELOG.md with the new change logs
- Commit your changes
- Install and use [bump2version](https://github.com/c4urself/bump2version) to automatically adjust a new version and create the git tag
E.g bump2version patch|minor|major
- git push and git push --tags to publish the new tag to the remote repository (Github)
- Travis will run the build and will publish to Pypi automatically when tests are not failing
