"""
.. include:: ../../README.md
"""

import pkg_resources


__version__ = pkg_resources.get_distribution("{{cookiecutter.package_name}}").version
