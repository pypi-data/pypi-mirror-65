# -*- coding: utf-8 -*-

"""
    Command line interface for core object
"""


import sys
from .core import Gcpm
import fire


class CliObject(object):
    """HTCondor pool manager for Google Cloud Platform."""

    def __init__(self, config="", test=False, oneshot=False):
        self.config = config
        self.test = test
        self.oneshot = oneshot

    def help(self):
        """Show help."""
        Gcpm.help()

    def version(self):
        """Show version."""
        Gcpm.version()

    def show_config(self):
        """Show configurations."""
        Gcpm(config=self.config).show_config()

    def install(self):
        """Install service related files."""
        Gcpm(config=self.config, service=True).install()

    def uninstall(self):
        """Uninstall service related files."""
        Gcpm(config=self.config, service=True).uninstall()

    def run(self):
        """Main function to run the loop."""
        Gcpm(config=self.config, test=self.test).run(oneshot=self.oneshot)

    def service(self):
        """Run the loop as service."""
        Gcpm(config=self.config, test=self.test, service=True).run()

    def set_pool_password(self, pool_password):
        """Set pool_password file in google storage."""
        Gcpm(config=self.config).set_pool_password(path=pool_password,
                                                   is_warn_exist=True)


def cli():
    """Main command line tool function."""
    if len(sys.argv) <= 1 or sys.argv[1] in ["-h", "--help"]:
        Gcpm.help()
    else:
        fire.Fire(CliObject)
