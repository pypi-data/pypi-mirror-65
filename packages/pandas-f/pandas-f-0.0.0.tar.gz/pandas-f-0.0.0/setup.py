#!python

# Copyright 2020 Vladimir Berkutov
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages


setup(
    name='pandas-f',
    version='',
    packages=find_packages(),
    url='http://github.com/dair-targ/pandas_f',
    license='Apache 2.0',
    author='Vladimir Berkutov',
    author_email='vladimir.berkutov@gmail.com',
    description='pandas extension that adds a flatmap',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Typing :: Typed',
    ],
    python_requires='>=3.6',
    install_requires=[
        'pandas',
    ],

    test_suite='nose.collector',
    setup_requires=[
        'setuptools',
        'wheel',
        'nose>=1.0',
    ],
)
