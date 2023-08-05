#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import sys
from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()


info = sys.version_info

setup(
    name='calc2',
    version='0.0.0.1',
    install_requires=["pandas", "matplotlib", "numpy", "xlwt", "openpyxl","scipy","scikit-learn","filedit", "scipy"],
    description='This is a Electric library for Python.',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Nishizumi',
    author_email='daiman003@yahoo.co.jp',
    url='https://tanaka0079.github.io/libs/python/electrical-python/docs/html/index.html',
    packages=[
        'calc2',
        'calc2.electricity',
    ],  # 提供パッケージ一覧。サブモジュールも忘れずに
    include_package_data=True,
    keywords='electricity',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Natural Language :: English',
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3.8',
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['calc2=calc2.calc2:main'],
    },
    test_suite="calc2-test",
)
