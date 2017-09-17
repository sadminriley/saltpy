#!/usr/bin/python
import shutil
from argparse import ArgumentParser
from subprocess import call as run
from paramiko import SSHClient, AutoAddPolicy

__version__ = 'SaltPY 0.1 Alpha'
__author__ = 'Riley - fasterdevops.github.io'

# Set global for salt-cloud provider
PROVIDER = 'digital_ocean'


class Setup(object):
    '''
    Setup salt master, minions,
    and download formulas from Riley's github
    '''
    def __init__(self):
        self.formula_repo = 'git clone https://github.com/sadminriley/saltstack.git'
        self.get_bootstrap = 'curl -L https://bootstrap.saltstack.com -o install_salt.sh'
        self.install_master = 'sh install_salt.sh -P -M'
        self.install_minion = 'sh install_salt.sh -P'
        self.config_dir = '/etc/salt'       # Default Salt configuration directory
        self.formula_dir = '/srv/salt'      # Default Salt formulas directory
        self.enable_master = 'systemctl enable salt-master'
        self.start_master = 'systemctl start salt-master'
        self.enable_minion = 'systemctl enable salt-minion'
        self.start_minion = 'systemctl start salt-minion'

    def master_setup(self):
        '''
        Using run to execute shell commands via subprocess.call() to
        setup Salt master and download formulas from Riley's git
        '''
        run(self.get_bootstrap)
        run(self.install_master)
        run(self.formula_repo, cwd=self.formula_dir)
        shutil.move('/srv/salt/saltstack/*', self.formula_dir)


    def minion_setup(self):
        '''
        Setup Salt minions
        '''
        run(self.get_bootstrap, shell=True)
        run(self.install_minion)

class SSH(object):
    '''
    Object to establish ssh connection
    '''
    client = SSHClient()

    def __init__(self, host, user='root', port=22, ssh_key='~/.ssh/id_rsa.pub', password=None):
        self.user = user
        self.host = host
        self.port = port
        self.sshkey = ssh_key
        self.password = password

    def connect(self):
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.client.connect(self.host, port=self.port, username=self.user, password=self.password)
        stdin, stdout, stderr = self.client.exec_command("ls")
        for line in stdout.readlines():
            print line
        self.client.close()

class Cloud(object):
    '''
    Class to setup and utilize
    Salt-Cloud
    '''
    def __init__(self):
        self.list_profiles = ['salt-cloud',
                              '--list-profiles',
                              PROVIDER]
        self.list_sizes = ['salt-cloud',
                           '--list-sizes',
                           PROVIDER]
        self.list_images = ['salt-cloud',
                            '--list-images',
                            PROVIDER]

    def list_pro(self):
        run(self.list_profiles)

    def list_sizes(self):
        run(self.list_sizes)

    def list_images(self):
        run(self.list_images)


class Master(object):
    '''
    Class to control minions from the Salt master
    '''
    def __init__(self, command=''):
        self.minions = "'*'"
        self.ping = ['salt',
                     self.minions,
                     'test.ping']
        self.cmd_run = ['salt',
                        'cmd.run',
                        command]

    def test_ping(self):
        run(self.ping)

    def run_cmd(self):
        command = raw_input('Enter the command you wish to run-:')
        run(self.cmd_run)


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
                        help='List' + PROVIDER + 'sizes',
                        dest='sizes',
                        action='store_true')
    parser.add_argument('--setupmaster',
                        help='Setup a Salt master',
                        dest='setupmaster',
                        action='store_true')
    args = parser.parse_args()
    return args

main()
