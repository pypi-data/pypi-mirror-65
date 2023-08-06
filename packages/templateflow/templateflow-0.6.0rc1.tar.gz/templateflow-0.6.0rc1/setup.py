#!/usr/bin/env python
""" templateflow setup script """
import sys
from setuptools import setup
import versioneer
from setuptools.command.install import install
from setuptools.command.develop import develop

# Give setuptools a hint to complain if it's too old a version
# 30.3.0 allows us to put most metadata in setup.cfg
# Should match pyproject.toml
SETUP_REQUIRES = ['setuptools >= 30.3.0']
# This enables setuptools to install wheel on-the-fly
SETUP_REQUIRES += ['wheel'] if 'bdist_wheel' in sys.argv else []


def make_cmdclass(basecmd):
    """Decorate setuptools commands."""
    base_run = basecmd.run

    def new_run(self):
        from templateflow.conf import update_home
        update_home()
        base_run(self)

    basecmd.run = new_run
    return basecmd


@make_cmdclass
class CheckHomeDevCommand(develop):
    pass

@make_cmdclass
class CheckHomeProdCommand(install):
    pass


if __name__ == '__main__':
    """ Install entry-point """
    setup(
        name='templateflow',
        version=versioneer.get_version(),
        setup_requires=SETUP_REQUIRES,
        cmdclass=versioneer.get_cmdclass(cmdclass={
            'develop': CheckHomeDevCommand,
            'install': CheckHomeProdCommand,
        }),
    )
