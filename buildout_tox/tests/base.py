# Copyright (c) 2011 Simplistix Ltd
#
# See license.txt for more details.
from logging import INFO
from testfixtures import TempDirectory, Replacer, OutputCapture, LogCapture
from unittest import TestCase as BaseTestCase
from zc.buildout import testing as buildout_testing
from zc.buildout.buildout import Buildout

import os
import sys

def setUp(test):
    buildout_testing.buildoutSetUp(test)
    # do a develop install of the recipe
    buildout_testing.install_develop('buildout-tox', test)
    # required by the recipe
    #buildout_testing.install('zc.recipe.egg', test)
    # setup the tempdir for testfixtures.manuel
    test.globs['dir'] = td = TempDirectory(path=os.getcwd())
    test.globs['r'] = r = Replacer()
    r.replace('os.environ', {})
    r.replace('sys.path', sys.path[:])

def tearDown(test):
    test.globs['r'].restore()
    buildout_testing.buildoutTearDown(test)

class Adapter(object):
    def __init__(self, test):
        self.globs = test.__dict__
        
class TestCase(BaseTestCase):

    def setUp(self):
        self.adapter = Adapter(self)
        setUp(self.adapter)
        
    def tearDown(self):
        tearDown(self.adapter)

    def run_buildout(self):
        with OutputCapture() as output:
            buildout = Buildout('buildout.cfg', [], command='install')
            with LogCapture('zc.buildout', level=INFO) as log:
                buildout.install([])
        self.output = output
        self.log = log
        
        
