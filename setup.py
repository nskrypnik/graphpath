import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = []

setup(name='graphpath',
      version='0.1',
      license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
      description='Simple program for graph traversing',
      author="Niko Skrypnik",
      keywords='test graph traversal',
      packages=find_packages(where="."),
      package_dir = {'': '.'},
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      entry_points="""
      [console_scripts]
      graphpath = graphpath.graph_cli:main
      graphpathw = graphpath.gui:main
      """
      )
