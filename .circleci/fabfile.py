import json
import sys
import logging

from datetime import datetime
from os import abort

from fabric import Connection, task

from unipath import Path

SETTINGS_FILE_PATH = Path(__file__).ancestor(1).child('project_settings.json')
logger = logging.getLogger(__name__)

with open(SETTINGS_FILE_PATH, 'r') as f:
    # Load settings.
    project_settings = json.loads(f.read())


def get_connection(ctx):
    try:
        with Connection(ctx.host, ctx.user) as conn:
            return conn
    except Exception as e:
        logger.warning(f'Cannot establish connection as to host: {ctx.host} and user: {ctx.user}')
        logger.exception(e)
        return None


def stage_settings(stage='stable'):
    settings = project_settings['stages'][stage]
    return settings


@task
def development(ctx):
    ctx.user = stage_settings().get('user')
    ctx.host = stage_settings().get('host')


@task
def deploy(ctx):
    conn = get_connection(ctx)
    if conn is None:
        sys.exit("Failed to get connection")
    conn.run('cp /home/midhat/.env /home/midhat/confess/confess/')
    with conn.cd(stage_settings().get('code_src_directory')):
        pull_git_repository(conn)
    venv_dir = stage_settings().get("venv_directory")
    conn.run(f'source {venv_dir}bin/activate')
    with conn.cd(stage_settings().get('code_src_directory')):
        install_requirements(conn)
        collect_static(conn)
        migrate_models(conn)
    supervisor_conf(conn)
    celery_log_files(conn)
    restart_application(conn)
    restart_gunicorn(conn)


def print_status(description):
    now = datetime.now().strftime('%H:%M:%S')
    suffix = '...\n'
    print(f'({now}) {description.capitalize()}{suffix}')


@task
def pull_git_repository(ctx):
    print_status('pulling git repository')
    if isinstance(ctx, Connection):
        conn = ctx
    else:
        conn = get_connection(ctx)

    repository = project_settings.get("git_repository")
    branch = stage_settings().get("vcs_branch")
    conn.run(f'git stash')
    conn.run(f'git pull {repository} {branch}')


@task
def collect_static(ctx):
    print_status('collecting static files')
    if isinstance(ctx, Connection):
        conn = ctx
    else:
        conn = get_connection(ctx)
    conn.run('python3 manage.py collectstatic --noinput')


@task
def install_requirements(ctx):
    print_status('installing requirements')
    if isinstance(ctx, Connection):
        conn = ctx
    else:
        conn = get_connection(ctx)
    requirements_file = stage_settings().get("requirements_file")
    conn.run(f'pip install -r {requirements_file}')


@task
def migrate_models(ctx):
    print_status('migrating models')
    if isinstance(ctx, Connection):
        conn = ctx
    else:
        conn = get_connection(ctx)
    conn.run('python3 manage.py migrate --noinput')


@task
def restart_application(ctx):
    print_status('restarting application')
    if isinstance(ctx, Connection):
        conn = ctx
    else:
        conn = get_connection(ctx)

    restart_command = stage_settings().get('restart_command')
    result = conn.sudo(restart_command, shell=False)
    if result.failed:
        abort('Could not restart application.')


def restart_gunicorn(ctx):
    print_status('restarting gunicorn')
    if isinstance(ctx, Connection):
        conn = ctx
    else:
        conn = get_connection(ctx)

    result = conn.sudo('service gunicorn restart', shell=False)
    if result.failed:
        abort('Could not restart gunicorn.')


@task
def supervisor_conf(ctx):
    print_status('copy celery supervisor conf files')
    if isinstance(ctx, Connection):
        conn = ctx
    else:
        conn = get_connection(ctx)

    worker_conf = conn.sudo('cp /home/midhat/confess/celery_set_publish_time_worker.conf /etc/supervisor/conf.d/')
    beat_conf = conn.sudo('cp /home/midhat/confess/celery_set_publish_time_beat.conf /etc/supervisor/conf.d/', shell=False)

    if worker_conf.failed:
        abort('Could not copy worker conf.')
    if beat_conf.failed:
        abort('Could not copy beat conf.')


@task
def celery_log_files(ctx):
    print_status('create supervisor celery log files')
    if isinstance(ctx, Connection):
        conn = ctx
    else:
        conn = get_connection(ctx)

    worker_log = conn.sudo('touch /var/log/celery/confess_worker.log', shell=False)
    beat_log = conn.sudo('touch /var/log/celery/confess_beat.log', shell=False)

    if worker_log.failed:
        abort('Could not create worker log file.')
    if beat_log.failed:
        abort('Could not create beat log file.')
