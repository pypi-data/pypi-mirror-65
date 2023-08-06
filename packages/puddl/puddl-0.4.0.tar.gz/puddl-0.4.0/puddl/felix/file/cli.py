import logging
from pathlib import Path

import click
from sqlalchemy.sql import ddl

from puddl.db import get_alchemy_session
from puddl.felix.file.db import get_default_device, File
from puddl.db.alchemy import Upserter
from puddl.felix.file.lib import guess_filetype, get_stat

log = logging.getLogger(__name__)


@click.group(name='file')
def main():
    pass


@main.command()
@click.argument('path', type=click.Path(), nargs=-1)
def index(path):
    """
    Index a file.

    Consume STDIN if no arguments given. This is useful for pipelines like this:

        find . -type f -name '*.py' | puddl file index
    """
    # Using metavar makes things unnecessarily complicated. We want to keep Backus Naur.
    paths = path
    del path

    def _iter_paths():
        if not paths:
            for line in click.get_text_stream('stdin'):
                yield Path(line.rstrip('\n'))
        else:
            for x in paths:
                yield Path(x)

    session = get_alchemy_session()
    device = get_default_device(session)
    ups = Upserter(session, File)
    for path in _iter_paths():
        ups.upsert(
            path=path,
            device_id=device.id,
            filetype=guess_filetype(path),
            stat=get_stat(path)
        )
    session.commit()


@main.command()
@click.option('--limit', default=100)
@click.option('--all', is_flag=True)
def ls(limit, all):
    session = get_alchemy_session()
    query = session.query(File)
    if not all:
        query = query.limit(limit)
    for f in query:
        print(f.path)


@main.command('query')
@click.argument('query_string', type=click.STRING)
def q(query_string):
    """
    query by "path contains"
    """
    session = get_alchemy_session()
    for x in session.query(File).filter(File.path.contains(query_string)):
        print(x.path)


@main.group()
def db():
    pass


@db.command()
def create():
    from puddl.felix.file.db import Base
    logging.getLogger('sqlalchemy').setLevel(log.level)
    engine = get_alchemy_session().bind
    engine.execute(ddl.CreateSchema('file'))
    Base.metadata.create_all(engine)


@db.command()
@click.option('-f', '--force', is_flag=True)
def drop(force):
    statement = ddl.DropSchema('file', cascade=True)
    if not force:
        click.confirm(f'Will run "{statement}"; are you sure?', abort=True)
    logging.getLogger('sqlalchemy').setLevel(log.level)
    engine = get_alchemy_session().bind
    engine.execute(statement)
