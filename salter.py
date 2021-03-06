#!/usr/bin/python
import os
import shutil
import subprocess
import time
from argparse import ArgumentParser
from paramiko import SSHClient, AutoAddPolicy

__version__ = 'SaltPY 0.1 Alpha'
__author__ = 'Riley - fasterdevops.github.io'

# This is work in-progress.
# TODO: Finish SSH classes and start testing basic saltstack setups with SaltPY.


class Setup(object):
    '''
    Setup salt master, minions,
    and download formulas from Riley's github.
    Mostly using this to set a bunch of stuff to use later.
    '''
    def __init__(self, host, repo='git clone https://github.com/sadminriley/saltstack.git'):
        self.host = host
        self.repo = repo

    def master_setup(self):
        '''
        Using subprocess.call to execute shell commands via subprocess.call() to
        setup Salt master and download formulas from Riley's git
        '''
        subprocess.call(self.installer)
        subprocess.call(self.install_master)
        subprocess.call(self.formula_repo, cwd=self.formula_dir)
        shutil.move('/srv/salt/saltstack/*', self.formula_dir)


    def minion_setup(self):
        '''
        Setup Salt minions.
        Executing commands to SSH class via paramiko.
        '''
        ssh = SSH(self.host)
        commands = ['curl -L https://bootstrap.saltstack.com -o install_salt.sh','sh install_salt.sh -P -M','systemctl enable salt-minion','systemctl start salt-minion']
        print("Running salt install....this may take a few minutes!")
        ssh.connect(commands)
        time.sleep(35)
        accept_key = ['salt-key', '-A']
        subprocess.call(accept_key)

class SSH(object):
    '''
    Object to establish ssh connection.
    Example usage of ssh object-
    >>> from salter import SSH
    >>> host = 'riley.science'
    >>> ssh = SSH(host)
    >>> ssh.connect()
    '''
    client = SSHClient()

    def __init__(self, host, user='root', port=22, ssh_key='~/.ssh/id_rsa.pub', password=None):
        self.user = user
        self.host = host
        self.port = port
        self.sshkey = ssh_key
        self.password = password

    def connect(self, commands):
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.client.connect(self.host, port=self.port, username=self.user, password=self.password)
        for command in commands:
            stdin, stdout, stderr = self.client.exec_command(command)
            for line in stdout.readlines():
                print line
                self.client.close()

class Cloud(object):
    '''
    Class to setup and utilize
    Salt-Cloud
    '''
    def __init__(self):
        provider = 'digital_ocean'

        self.list_profiles = ['salt-cloud',
                              '--list-profiles',
                              provider]
        self.list_sizes = ['salt-cloud',
                           '--list-sizes',
                           provider]
        self.list_images = ['salt-cloud',
                            '--list-images',
                            provider]

    def list_pro(self):
        subprocess.call(self.list_profiles)

    def list_sizes(self):
        subprocess.call(self.list_sizes)

    def list_images(self):
        subprocess.call(self.list_images)


class Master(object):
    '''
    Class to control minions from the Salt master.
    Trying some things with this one, it's a mess right now!
    '''

    def __init__(self, minions='', ping='test.ping'):
        self.minions = minions
        self.ping = ping

    def test_ping(self, targets):
        ping_command = 'salt '+ targets + ' test.ping'
        os.system(ping_command)


def main():
    '''
    Main function to initialize classes
    and parse user arguments.
    '''
    print __version__
    parser = ArgumentParser(description='A Saltstack utility' +
                            ' to make Saltstack easier to' +
                            ' use and setup')
    parser.add_argument('--profiles',
                        help='List provider profiles',
                        dest='profiles',
                        action='store_true')
    parser.add_argument('--sizes',
                        help='List provider sizes',
                        dest='sizes',
                        action='store_true')
    parser.add_argument('--setupmaster',
                        help='Setup a Salt master',
                        dest='setupmaster',
                        action='store_true')
    args = parser.parse_args()
    return args

main()
