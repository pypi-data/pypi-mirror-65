# ##############################################################################
#  EnerPy (setup.py)
#  Copyright (C) 2020 Daniel Sullivan <daniel.sullivan@state.mn.us>
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
# ##############################################################################

from os import environ, path

from setuptools import setup

if environ.get('CI_COMMIT_TAG'):
    version = environ['CI_COMMIT_TAG']
elif environ.get('CI_JOB_ID'):
    version = environ['CI_JOB_ID']
else:
    try:
        import git

        version = '0.0.1~{:010x}'.format(git.Repo(search_parent_directories=True).head.object.hexsha)
    except:
        import random

        version = '0.0.0~{:010x}'.format(random.randrange(16 ** 10))

print(f'VERSION: {version}')
here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='EnerPy',
    version=version,
    packages=['enerpy'],
    url='https://gitlab.com/mpca-adau/enerpy',
    license='Lesser General Public License V3',
    author='Daniel Sullivan',
    author_email='daniel.sullivan@state.mn.us',
    description='Python Wrapper for the Energy Information Administration (EIA) API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['requests',
                      'logger-mixin',
                      'pandas'],
    python_requires='>3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Libraries'
    ]
)
