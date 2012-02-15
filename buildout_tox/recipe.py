# Copyright (c) 2011 Simplistix Ltd
#
# See license.txt for more details.

from ConfigParser import RawConfigParser
from contextlib import nested
from shutil import rmtree
from zc.buildout import UserError
from zc.buildout.easy_install import scripts
from zc.recipe.egg import Scripts
import os
import sys

class Recipe(object):

    def __init__(self, buildout, name, options):
        self.name = name
        self.options = options
        options['part_path'] = os.path.join(
            buildout['buildout']['parts-directory'],
            name
            )
        options['buildout_path'] = buildout['buildout']['directory']
        self.scripts = Scripts(buildout, 'buildout-tox', options)

    def install(self):

        tox_path = self.options['part_path']
        default_python = sys.executable
        buildout_path = self.options['buildout_path']

        if os.path.exists(tox_path):
            rmtree(tox_path)
        os.mkdir(tox_path)
        self.options.created(tox_path)

        tox_config = RawConfigParser()
        tox_config.add_section('tox')

        # build command
        build = self.options.get('build')
        if build:
            build = os.path.abspath(os.path.join(buildout_path, build))
        else:
            build = 'bin/buildout setup setup.py sdist'
        tox_config.set('tox', 'build', build)

        # environments
        for env in self.options['environments'].split():
            env_path = os.path.join(self.options['part_path'], env)
            os.mkdir(env_path)
            tox_config.add_section(env)

            # path
            tox_config.set(env, 'path', env_path)
            # python
            tox_config.set(env, 'python', default_python)
            
            # test command
            tox_config.set(env, 'test', 'bin/test')

            # bootstrap.py
            with nested(
                open(os.path.join(os.path.dirname(__file__), 'bootstrap.py'), 'rb'),
                open(os.path.join(env_path, 'bootstrap.py'), 'wb')
                ) as (source, destination):
                destination.write(source.read())

            # build.cfg
            with file(os.path.join(env_path, 'build.cfg'), 'w') as conf_file:
                conf_file.write(self.options['config']+'\n')

            # develop.cfg
            with file(os.path.join(env_path, 'develop.cfg'), 'w') as conf_file:
                conf_file.write("""
[buildout]
extends = build.cfg
develop = ../../..
""")

        with open(os.path.join(tox_path, 'tox.cfg'), 'w') as outfile:
            tox_config.write(outfile)

        # install tox script
        created = self.scripts.install()
        self.options.created(*created)
        
        return self.options.created()

    update = install
