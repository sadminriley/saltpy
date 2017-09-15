#!/usr/bin/python
import salt
import subprocess
import os
from argparse import ArgumentParser

# Let's set some globals!
PROVIDER = 'digital_ocean'

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
        subprocess.Popen(self.list_profiles)

    def list_sizes(self):
        subprocess.Popen(self.list_sizes)

    def list_images(self):
        subprocess.Popen(self.list_images)

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
        subprocess.Popen(self.ping)

    def run_cmd(self):
        command = raw_input('Enter the command you wish to run-:')
        subprocess.Popen(self.cmd_run)

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

