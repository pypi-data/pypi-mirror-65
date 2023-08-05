from setuptools import setup

setup(
  name = "subgal",
  version = "1.0.1",
  author = "John Baber-Lucero",
  author_email = "pypi@frundle.com",
  description = ("A collection of tools for creating html galleries from photos that have been sorted by sortphotos"),
  license = "GPLv3",
  url = "https://github.com/jbaber/subgal",
  packages = ['subgal'],
  install_requires = ['docopt', 'pillow', 'python-magic',],
  tests_require=['pytest'],
  package_data = {
    'subgal': ['templates/main_index.html', 'templates/individual_index_template.html'],
  },
  entry_points = {
    'console_scripts': ['subgal=subgal.subgal:main'],
  }
)
