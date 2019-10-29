#!/usr/bin/python2

from fabric.api import env, run, cd, task

debug = False

"""
Fabric deploy script

This is a Fabric (python 2.7) deployment script to be used by CircleCI to
deploy this project automatically to either production or staging.
"""

if debug:
    import paramiko
    paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG)

env.venv_name = 'confess'
env.path = '/home/midhat/confess'
env.user = 'midhat'


@task
def production():
    env.branch = 'master'
    env.hosts = ['itiraf.cf', ]


@task
def staging():
    env.branch = 'develop'
    env.hosts = ['itiraf.cf', ]


@task
def venv(cmd):
    run('workon {0} && {1}'.format(env.venv_name, cmd))


@task
def deploy():
    with cd(env.path):
        run('git pull origin {0}'.format(env.branch))
        venv('pip install -r requirements.txt')
        venv('python manage.py migrate')
        venv('python manage.py collectstatic --noinput')
        run('supervisorctl reread')
        run('supervisorctl update')
        run('supervisorctl restart confess')
