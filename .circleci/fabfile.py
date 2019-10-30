import json
import sys

from datetime import datetime
from os import abort

from fabric import Connection, task

from unipath import Path

SETTINGS_FILE_PATH = Path(__file__).ancestor(1).child('project_settings.json')

with open(SETTINGS_FILE_PATH, 'r') as f:
    # Load settings.
    project_settings = json.loads(f.read())


def get_connection(ctx):
    try:
        with Connection(ctx.host, ctx.user) as conn:
            return conn
    except Exception as e:
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
    with conn.cd(stage_settings().get('code_src_directory')):
        pull_git_repository(conn)
    venv_dir = stage_settings().get("venv_directory")
    with conn.run(f'source {venv_dir}/bin/activate'):
        collect_static(conn)
        install_requirements()
        migrate_models()
    restart_application(conn)


def print_status(description):
    def print_status_decorator(fn):
        def print_status_wrapper(test):
            now = datetime.now().strftime('%H:%M:%S')
            suffix = '...\n'
            print(f'({now}) {description.capitalize()}{suffix}')
            now = datetime.now().strftime('%H:%M:%S')
            print(f'({now}) {description.capitalize()}{suffix}')
        return print_status_wrapper
    return print_status_decorator


@print_status('pulling git repository')
@task
def pull_git_repository(ctx):
    if isinstance(ctx, Connection):
        conn = ctx
    else:
        conn = get_connection(ctx)

    repository = project_settings.get("git_repository")
    branch = stage_settings().get("vcs_branch")
    conn.run(f'git pull {repository} {branch}')


@print_status('collecting static files')
@task
def collect_static(ctx):
    if isinstance(ctx, Connection):
        conn = ctx
    else:
        conn = get_connection(ctx)
    conn.run('python manage.py collectstatic')


@print_status('installing requirements')
@task
def install_requirements(ctx):
    if isinstance(ctx, Connection):
        conn = ctx
    else:
        conn = get_connection(ctx)
    requirements_file = stage_settings().get("requirements_file")
    conn.run(f'pip install -r {requirements_file}')


@print_status('migrating models')
@task
def migrate_models(ctx):
    if isinstance(ctx, Connection):
        conn = ctx
    else:
        conn = get_connection(ctx)
    conn.run('python manage.py migrate')


@print_status('restarting application')
@task
def restart_application(ctx):
    if isinstance(ctx, Connection):
        conn = ctx
    else:
        conn = get_connection(ctx)

    restart_command = stage_settings().get('restart_command')
    result = conn.sudo(restart_command)
    if result.failed:
        abort('Could not restart application.')
