#!/usr/bin/env python
# =.- coding: utf-8 -.-

import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / 'README.md').read_text()

with open('requirements.txt') as fp:
    install_requires = fp.read()

setup(
    name='vizinet',
    version='1.0.0',
    description='Official VIZINET module.',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/vizinet',
    author='Luke Weber',
    author_email='lukedottec@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    # TODO:  packages=find_packages(exclude=('tests',)),
    # packages=['src'],
    # include_package_data=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'realpython=reader.__main__:main',
        ]
    }
)
