# Copyright (c) 2011 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

from setuptools import setup, find_packages

import os

base_dir = os.path.join(os.path.dirname(__file__))

setup(
    name='buildout-tox',
    version='1.0dev',
    author='Chris Withers',
    author_email='chris@simplistix.co.uk',
    license='MIT',
    description="zc.buildout recipe to build and test packages in multiple environments.",
    long_description=open(os.path.join(base_dir,'docs','description.txt')).read(),
    url='http://www.simplistix.co.uk/software/python/buildout-tox',
    classifiers=[
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        ],
    packages = find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'zc.buildout>=1.5.0,<2.0',
    ],
    entry_points = {
        },
    extras_require=dict(
           test=[
            'manuel',
            'testfixtures',
            ],
           )
    )
