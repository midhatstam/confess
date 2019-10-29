from fabric import task
from invoke import env, run
from invoke.util import cd

debug = False


if debug:
    import paramiko
    paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG)

env.Environment.venv_name = 'confess'
env.Environment.user = 'midhat'
env.Environment.branch = 'master'
env.Environment.hosts = ['206.189.203.241', ]


@task
def venv(cmd):
    run('workon {0} && {1}'.format(env.Environment.venv_name, cmd))


@task
def deploy():
    with cd('/home/midhat/confess'):
        run(f'git pull origin {env.Environment.branch}')
        venv('pip install -r requirements.txt')
        venv('python manage.py migrate')
        venv('python manage.py collectstatic --noinput')
        run('supervisorctl reread')
        run('supervisorctl update')
        run('supervisorctl restart confess')
