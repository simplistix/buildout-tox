# Copyright (c) 2011 Simplistix Ltd
#
# See license.txt for more details.

import os
import sys

from testfixtures import compare, StringComparison as S

from .base import TestCase

class Tests(TestCase):
    
    def test_minimal(self, logged=None):
        ########################################################################
        self.dir.write('buildout.cfg',"""
[buildout]
parts = tox
 
[tox]
recipe = buildout-tox
config =
  [buildout]
  parts = 
environments = env
""")

        self.run_buildout()

        self.dir.check_all(
            'parts/tox',
            'env/',
            'env/bootstrap.py',
            'env/buildout.cfg',
            'tox.cfg',
            )

        compare("""
[tox]
build = bin/buildout setup setup.py sdist

[env]
python = %(py)s
path = %(buildout_path)s/parts/tox/env
test = bin/test

""".lstrip() % dict(py=sys.executable,
                    buildout_path=self.dir.path),
                self.dir.read('parts/tox/tox.cfg'))
        
        compare("""
[buildout]
parts =
""",
                self.dir.read('parts/tox/env/buildout.cfg'))

        with open(os.path.join(os.path.dirname(__file__),
                               os.pardir, 'bootstrap.py'), 'rb') as bs:
            compare(bs.read(), self.dir.read('parts/tox/env/bootstrap.py'))

        tox_bin = self.dir.read('bin/tox')
        self.assertTrue(
            tox_bin.endswith(
                'import buildout_tox.tox\n\n'
                "if __name__ == '__main__':\n"
                '    buildout_tox.tox.main()\n',
                ),repr(tox_bin))

        if logged is None:
            logged = (
                ('zc.buildout', 'INFO', 'Installing tox.'),
                ('zc.buildout.easy_install',
                 'INFO',
                 "Generated script '%s/bin/tox'." % self.dir.path)
                )
        self.log.check(*logged)

        self.output.compare(
            # spurious output, not to worry about...
            "Couldn't find index page for 'zc.recipe.egg' (maybe misspelled?)\n"
            "Couldn't find index page for 'argparse' (maybe misspelled?)"
            )

    def test_rerun(self):
        ########################################################################
        self.test_minimal()
        self.test_minimal(logged=(
            ('zc.buildout', 'INFO', 'Updating tox.'),
            ))
        

    def test_use_existing_parts(self):
        ########################################################################
        pass
    
    def test_parts_and_config(self):
        ########################################################################
        pass
    
    def test_add_to_section(self):
        pass

    def test_add_to_nonexisting_section(self):
        # should create
        pass
    
    def test_add_to_nonexisting_option(self):
        # should create
        pass

    def test_replace(self):
        pass

    def test_replace_nonexsting_section(self):
        # should create
        pass
    
    def test_replace_nonexisting_option(self):
        # should create
        pass

    def test_env_vars(self):
        # should set for each run
        pass
        
    def test_default_envs(self):
        pass

