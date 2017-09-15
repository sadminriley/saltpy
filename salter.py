#!/usr/bin/python
import os
import salt
import shutil
from argparse import ArgumentParser
from subprocess import call
__version__ = 'SaltPY 0.1 Alpha'
__author__ = 'Riley - fasterdevops.github.io'

# Let's set some globals!
PROVIDER = 'digital_ocean'
class Setup(object):

    def __init__(self):
        self.formula_repo = 'git clone https://github.com/sadminriley/saltstack.git'
        self.get_bootstrap = 'curl -L https://bootstrap.saltstack.com -o install_salt.sh'
        self.install_master = 'sh install_salt.sh -P -M'
        self.install_minion = 'sh install_salt.sh -P'
        self.config_dir = '/etc/salt'
        self.formula_dir = '/srv/salt'

    def master_setup(self):
        subprocess.call(self.get_bootstrap, shell=True)
        subprocess.call(self.install_master, shell=True)
        subprocess.call(self.git clone, cwd=self.formula_dir)
        shutil.move('/srv/salt/saltstack/*', self.formula_dir)

    def minion_setup(self):
        subprocess.call(self.get_bootstrap, shell=True)
        subprocess.call(self.install_minion)

class Cloud(object):
    def __init__(self):
        self.list_profiles = ['salt-cloud',
                              '--list-profiles',
                              PROVIDER ]
        self.list_sizes = ['salt-cloud',
                           '--list-sizes',
                           PROVIDER ]
        self.list_images = ['salt-cloud',
                            '--list-images',
                            PROVIDER ]
    def list_pro(self):
        subprocess.call(self.list_profiles)

    def list_sizes(self):
        subprocess.call(self.list_sizes)

    def list_images(self):
        subprocess.call(self.list_images)

class Master(object):

    def __init__(self, command=''):
        MINIONS = "'*'"
        self.ping = ['salt',
                     MINIONS,
                     'test.ping' ]
        self.cmd_run = ['salt',
                        'cmd.run',
                        command ]

    def test_ping(self):
        subprocess.call(self.ping)

    def run_cmd(self):
        command = raw_input('Enter the command you wish to run-:')
        subprocess.call(self.cmd_run)

def main():
    '''
    Main function and argument parse.
    '''
    print __version__
    parser = ArgumentParser(description='A Saltstack utility' +
                            'to make Saltstack easier to' +
                            'use and setup')
    parser.add_argument('--profiles',
                        help='List provider profiles',
                        dest='profiles',
                        action='store_true')
    parser.add_argument('--sizes',
                        help='List' + PROVIDER 'sizes',
                        dest='sizes',
                        action='store_true')

