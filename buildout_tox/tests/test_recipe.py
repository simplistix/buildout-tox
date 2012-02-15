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
            'env/build.cfg',
            'env/develop.cfg',
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
                self.dir.read('parts/tox/env/build.cfg'))

        compare("""
[buildout]
extends = build.cfg
develop = ../../..
""",
                self.dir.read('parts/tox/env/develop.cfg'))

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
        return
        ########################################################################
        self.dir.write('buildout.cfg',"""
[buildout]
parts = tox

[py]
recipe = zc.recipe.egg
eggs =
   some_package
   another_package
interpreter = py

[test]
recipe = zc.recipe.testrunner
eggs = some_package

[tox]
recipe = buildout-tox
parts = py test
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
parts = py test

[py]
recipe = zc.recipe.egg
eggs =
   some_package
   another_package
interpreter = py

[test]
recipe = zc.recipe.testrunner
eggs = some_package

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

        self.log.check(
                ('zc.buildout', 'INFO', 'Installing tox.'),
                ('zc.buildout.easy_install',
                 'INFO',
                 "Generated script '%s/bin/tox'." % self.dir.path)
            )

        self.output.compare(
            # spurious output, not to worry about...
            "Couldn't find index page for 'zc.recipe.egg' (maybe misspelled?)"
            )

    def test_parts_and_config(self):
        ########################################################################
        return
        self.dir.write('buildout.cfg',"""
[buildout]
parts = tox

[py]
recipe = zc.recipe.egg
eggs =
   some_package
   another_package
interpreter = py

[test]
recipe = zc.recipe.testrunner
eggs = some_package

[tox]
recipe = buildout-tox
parts = py test
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
parts = py test

[py]
recipe = zc.recipe.egg
eggs =
   some_package
   another_package
interpreter = py

[test]
recipe = zc.recipe.testrunner
eggs = some_package

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

        self.log.check(
                ('zc.buildout', 'INFO', 'Installing tox.'),
                ('zc.buildout.easy_install',
                 'INFO',
                 "Generated script '%s/bin/tox'." % self.dir.path)
            )

        self.output.compare(
            # spurious output, not to worry about...
            "Couldn't find index page for 'zc.recipe.egg' (maybe misspelled?)"
            )
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

    def test_basic(self):
        return
        self.dir.write('buildout.cfg',"""
[buildout]
parts = tox
 
[test]

[tox]
recipe = buildout-tox
config =
  [buildout]
  parts = test

  [test]
  recipe = zc.recipe.testrunner
  eggs = mypackage[test]
environments = env1, env2
build = bin/docpy setup.py sdist
test = bin/test

[env1]
python = python2.6
add:test:eggs = foo
add =
  [test]
  eggs = foo
replace =
  [test]
  eggs = bar

[env2]
python = python2.7
""")

        self.run_buildout()

        # check files
        # check bin/tox exists

    def test_part(self):
        return
        self.dir.write('buildout.cfg',"""
[buildout]
parts = tox
 
[test]
recipe = zc.recipe.testrunner
eggs = testfixtures[test]

[tox]
recipe = buildout-tox
config_parts = test docs
environment = env1, env2
build = bin/docpy setup.py sdist
test = bin/test
""")

        self.run_buildout()
