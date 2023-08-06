import logging
import subprocess

import click
from pathlib import Path

from puddl import get_config
from puddl.apps import App
from puddl.conf import Config

log = logging.getLogger(__name__)
LOG_LEVELS = ['CRITICAL', 'FATAL', 'ERROR', 'WARN', 'WARNING', 'INFO', 'DEBUG']


class AppsGroup(click.Group):

    def __init__(self, name=None, commands=None, **attrs):
        self._apps = [App(x) for x in get_config().apps]
        self._name2app = {
            x.cmd_name: x for x in self._apps
        }
        super().__init__(name, commands, **attrs)

    def list_commands(self, ctx):
        core_commands = set(super().list_commands(ctx))
        app_names = set(x for x in self._name2app)
        return sorted(core_commands | app_names)

    def get_command(self, ctx, cmd_name):
        if cmd_name in self._name2app:
            app = self._name2app[cmd_name]
            return app.get_command()
        return super().get_command(ctx, cmd_name)


@click.group(cls=AppsGroup)
@click.option('-l', '--log-level',
              type=click.Choice(LOG_LEVELS, case_sensitive=False),
              default='WARNING')
@click.option('--loggers', default='', help='comma-separated logger names')
@click.version_option()
def root(log_level, loggers):
    logging.basicConfig(level=log_level)
    if loggers:
        for name in loggers.split(','):
            logging.getLogger(name).setLevel(log_level)
    pass


@root.group()
def config():
    pass


@config.command()
def init():
    data = {}
    defaults = Config.get_defaults()
    data.update(defaults)

    dot_env = Path('.env')
    try:
        with dot_env.open() as f:
            contents = f.read()
        for line in contents.strip().split('\n'):
            k, v = line.strip().split('=')
            if k in defaults:
                log.info(f'using {k} from .env')
                data[k] = v
    except FileNotFoundError:
        pass

    conf = Config(data)
    conf.write()


@config.command()
def show():
    conf = get_config()
    print(conf.data)


@root.group()
def app():
    pass


@app.command('add')
@click.argument('package_path')
def app_add(package_path):
    conf = get_config()
    conf.add_app(package_path)
    conf.write()


@app.command('ls')
@click.option('-v', '--verbose', is_flag=True)
def app_ls(verbose):
    conf = get_config()
    apps = sorted(conf['apps'])
    for app_name in apps:
        msg = app_name
        if verbose:
            msg = str(App(app_name))
        click.echo(msg)


@app.command('rm')
@click.argument('package_path')
def app_remove(package_path):
    conf = get_config()
    conf.remove_app(package_path)
    conf.write()


@root.group()
def db():
    pass


@db.command()
def health():
    conf = get_config()

    import psycopg2
    # consumes PG* env vars
    connection = psycopg2.connect(conf.db_url)
    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
    log.info('database available')


@db.command()
def shell():
    conf = get_config(app='db shell')
    # want to see good error handling for this kind of thing?
    # https://github.com/pallets/click/blob/19fdc8509a1b946c088512e0e5e388a8d012f0ce/src/click/_termui_impl.py#L472-L487
    subprocess.Popen('psql', env=conf.db_env).wait()


@db.command()
@click.option('--app')
def url(app):
    """
    print DB URL

    Useful for things like this:

        from sqlalchemy import create_engine
        database_url = 'postgresql://puddl:aey1Ki4oaZohseWod2ri@localhost:13370/puddl'
        engine = create_engine(database_url, echo=False)
        df.to_sql('bp', engine)
    """
    conf = get_config(app=app)
    print(conf.db_url)


@db.command()
def env():
    """
    Prints the database's environment.
    WARNING: This dumps your password. Use it like this:

        source <(puddl db env)
    """
    conf = get_config()
    for k, v in conf.db_env.items():
        print(f'export {k}={v}')


@db.command()
def sessions():
    """
    Lists active sessions.
    """
    conf = get_config(app='db sessions')
    query = """SELECT pid AS process_id,
           usename AS username,
           datname AS database_name,
           client_addr AS client_address,
           application_name,
           backend_start,
           state,
           state_change
    FROM pg_stat_activity;"""
    click.echo(
        subprocess.check_output(['psql', '-c', query], encoding='utf-8', env=conf.db_env))


@db.command()
def queries():
    print('xxx')


def main():
    # this function is referenced in `setup.py`
    root(auto_envvar_prefix='PUDDL')


if __name__ == '__main__':
    # https://click.palletsprojects.com/en/7.x/options/#values-from-environment-variables
    main()
