#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['pytest_check']

package_data = \
{'': ['*']}

package_dir = \
{'': 'src'}

install_requires = \
['pytest>=3.1.1']

extras_require = \
{'test': ['tox']}

entry_points = \
{'pytest11': ['check = pytest_check.plugin']}

setup(name='pytest_check',
      version='0.3.8',
      description='A pytest plugin that allows multiple failures per test.',
      author='Brian Okken',
      author_email='brian+pypi@pythontest.com',
      url='https://github.com/okken/pytest-check',
      packages=packages,
      package_data=package_data,
      package_dir=package_dir,
      install_requires=install_requires,
      extras_require=extras_require,
      entry_points=entry_points,
     )
