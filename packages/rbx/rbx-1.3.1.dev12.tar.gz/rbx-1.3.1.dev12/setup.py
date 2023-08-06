# Copyright 2020 Rockabox Media Limited
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

from setuptools import find_namespace_packages, setup

setup(
    name='rbx',
    version='1.3.1.dev12',
    license='Apache 2.0',
    description='Scoota Platform utilities',
    long_description='A collection of common tools for the Scoota Platform services.',
    url='http://scoota.com/',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet',
    ],
    author='The Scoota Engineering Team',
    author_email='engineering@scoota.com',
    python_requires='>=3.6',
    install_requires=[
        'arrow>=0.15',
        'Click<8',
        'colorama',
        'PyYAML>=5.1.2',
    ],
    extras_require={
        'geo': [
            'googlemaps==4.2.0',
        ],
        'storage': [
            'google-cloud-storage==1.23',
        ],
        'tests': [
            'Flask==1.1.1',
            'googlemaps==4.2.0',
            'google-cloud-storage==1.23',
        ],
    },
    entry_points={
        'console_scripts': [
            'geocode = rbx.geo.cli:geocode [geo]',
            'reverse_geocode = rbx.geo.cli:reverse_geocode [geo]',
            'unpack = rbx.geo.cli:unpack [geo]',
        ],
    },
    packages=find_namespace_packages(include=['rbx.*']),
    zip_safe=True
)
