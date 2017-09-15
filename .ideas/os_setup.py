class SetupMaster(object):
    def check_os():
        if 'CentOS Linux' in platform.linux_distribution():
            redhat_setup()
        else:
            debian_setup()

