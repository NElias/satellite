from fabric.context_managers import prefix

from fabric.api import run, cd
from fabric.contrib.files import exists

from satellite import *


### Dependencies:
def update_deps(path):
    if not exists(settings.main.root_venv):
        run("virtualenv %s --system-site-packages" % settings.main.root_venv)
    with cd(path):
        with prefix(settings.main.venv_activate):
            run('pip install -r requirements.txt')


### Git stuff
def install_repo(dest):
    run('git clone %s %s' % (settings.git.repo, dest))

    with cd(dest):
        run('git submodule init')
        run('git submodule update')


def update_repo(path):
    with cd(path):
        run('git pull')
        run('git submodule update')


def adduser():
    sudo('adduser --disabled-password %s' % settings.fabric.user)


def ssh_keygen():
    usersudo('ssh-keygen', settings.fabric.user)


def add_access(key):
    from fabric.context_managers import settings as fabric_settings
    with fabric_settings(user=settings.satellite.sudo_user):
        run('echo "%s" | sudo -u %s tee /home/%s/.ssh/authorized_keys' % (key, settings.fabric.user, settings.fabric.user))
    #TODO run as user
    usersudo('chmod og-rw /home/%s/.ssh/authorized_keys' % settings.fabric.user, settings.fabric.user)


def get_revision(*args):
    cmd = 'git ls-remote %s | head -n 1 | cut -f 1,1' % settings.git.repo
    # because `run` will return the _full_ i/o log
    # including the password prompt
    return run(cmd).strip().split('\n')[-1]
