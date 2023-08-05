#!/usr/bin/env python
import os
from setuptools import setup


version = '0.0.2'


def read(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read().strip()


setup(name='talqual',
      version=version,
      description=('TAL Chameleon (static site generator)'),
      long_description='\n\n'.join((read('README.rst'), read('CHANGES.txt'))),
      classifiers=[
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Intended Audience :: Developers',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Development Status :: 1 - Planning',
          'Topic :: Internet :: WWW/HTTP',
      ],
      author='Aleix Llusà Serra',
      author_email='timbaler@timbaler.cat',
      url='https://gitlab.com/timbaler/talqual/',
      license='GPLv3+',
      packages=['talqual'],
      entry_points="""
          [console_scripts]
          talqual=talqual.cli:cli
      """,
      python_requires='>=3.5.3',
      install_requires=[
          'anytree<2.7.0',
          'chameleon',
          'click',
          'pyyaml',
          ],
      extras_require={
        'test': [
            'sphinx',
            'pytest',
            'pytest-html',
            'pytest-cov',
            'pytest-flake8',
            'pytest-mock',
            'pytest-selenium',
            'flake8-isort',
            'transcrypt',
        ],
      },
      include_package_data=True
      )
