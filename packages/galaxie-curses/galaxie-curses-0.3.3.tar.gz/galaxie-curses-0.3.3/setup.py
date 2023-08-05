# -*- coding:utf-8 -*-
import os
from setuptools import setup

pre_version = "0.3.3"
if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
else:
    if os.environ.get('CI_JOB_ID'):
        version = os.environ['CI_JOB_ID']
    else:
        version = pre_version

with open('README.md') as f:
    long_description = f.read()

setup(name='galaxie-curses',
      version=version,
      description='Galaxie Curses is a free software ToolKit for the NCurses API',
      long_description=long_description,
      long_description_content_type='text/markdown; charset=UTF-8',
      url='https://gitlab.com/Tuuux/galaxie-curses',
      author='Tuuux',
      author_email='tuxa@rtnp.org',
      license='GNU GENERAL PUBLIC LICENSE Version 3',
      packages=['GLXCurses'],
      zip_safe=False,
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Environment :: Console",
          "Environment :: Console :: Curses",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3 :: Only",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      setup_requires=[
          'green',
          'wheel'
      ],
      tests_require=[
          'pyperclip',
          'wheel'
      ],
      install_requires=[
          'pyperclip',
          'wheel', 'Pillow'
      ])
