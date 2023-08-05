#!/usr/bin/env python3

import codecs
from os import path
from setuptools import setup

pwd = path.abspath(path.dirname(__file__))
with codecs.open(path.join(pwd, 'README.md'), 'r', encoding='utf8') as input:
    long_description = input.read()

version='1.7'
	
setup(
	name='GoldenChild',
	version=version,
	license='MIT',
    long_description=long_description,
	long_description_content_type="text/markdown",
	url='https://github.com/eddo888/GoldenChild',
	download_url='https://github.com/eddo888/GoldenChild/archive/%s.tar.gz'%version,
	author='David Edson',
	author_email='eddo888@tpg.com.au',
	packages=[
		'GoldenChild'
	],
	install_requires=[
		'argcomplete',
		'libxml2-python3',
		'xmltodict',
		'Baubles',
		'Perdy',
		'Argumental',
	],
	scripts=[
		'bin/xget.py',
		'bin/xset.py',
		'bin/validate.py',
	],
)
