#! /usr/bin/env python
#
# Copyright (C) 2019 boleti-p
# License: BSD-3-Clause

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="svlearn",
    version="0.0.3.dev7",
    author="bvoleti-p",
    author_email="",
    description="Utils for ML",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    # packages=setuptools.find_packages(),
	packages=['svlearn'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
	# py_modules=["utils"],
	install_requires=[
		'markdown',
		'numpy',
		'pandas',
		'sklearn',
		'scipy',
		'matplotlib',
		'seaborn',
		'statsmodels',
		'keras',
		'IPython',
		'missingno',
		'category_encoders',
		'tensorflow'
	],
)