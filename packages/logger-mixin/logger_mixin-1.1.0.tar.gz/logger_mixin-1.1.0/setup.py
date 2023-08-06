#  logger-mixin setup.py (Last Modified 3/10/20, 10:36 AM)
#  Copyright (C) 2020 Daniel Sullivan (daniel.sullivan@state.mn.us
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
import os
from os import path

from setuptools import setup

if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
elif os.environ.get('CI_JOB_ID'):
    version = os.environ['CI_JOB_ID']
else:
    try:
        import git

        version = '0.0.1~{:010x}'.format(git.Repo(search_parent_directories=True).head.object.hexsha)
    except:
        import random

        version = '0.0.0~{:010x}'.format(random.randrange(16 ** 10))

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='logger_mixin',
    version=version,
    packages=['logger_mixin'],
    url='https://gitlab.com/ds-mpca/logger-mixin',
    license='Lesser General Public License V3',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Daniel Sullivan',
    author_email='daniel.sullivan@state.mn.us',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)'
    ]
)
