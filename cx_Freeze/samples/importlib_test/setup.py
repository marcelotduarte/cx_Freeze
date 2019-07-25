#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen

from cx_Freeze import setup, Executable

buildOptions = dict(packages = ['gevent'], excludes = [], includes = [],
		    zip_include_packages = ["*"], zip_exclude_packages = [],
            build_exe='test_exe',)

examples = [
'https://raw.githubusercontent.com/aio-libs/aiohttp/master/examples/server_simple.py',
'https://raw.githubusercontent.com/aio-libs/aiohttp/master/examples/web_srv.py',
'https://raw.githubusercontent.com/gevent/gevent/master/examples/wsgiserver.py'
]

executables = []
for ex in examples:
	local = ex.split('/')[-1]
	with urlopen(ex) as fp1, open(local, 'w+b') as fp2:
		fp2.write(fp1.read())
	executables.append(Executable(local))

setup(name='test_exe',
      version = '1.0',
      description = 'test_exe',
      options = dict(build_exe = buildOptions),
      executables = executables)