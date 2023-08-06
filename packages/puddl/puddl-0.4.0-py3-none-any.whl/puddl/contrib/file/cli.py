import logging
from pathlib import Path

import click

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
    # The path argument could use a better name, but the help text needs to be sane.
    # Using metavar makes things unnecessarily complicated. We want to keep backus naur.
    def _iter_paths():
        if not path:
            for line in click.get_text_stream('stdin'):
                yield Path(line.rstrip('\n'))
        else:
            for x in path:
                yield x

    from puddl.models import Device
    from .models import File
    for p in _iter_paths():
        log.info(f'indexing {p}')
        File.objects.upsert(
            device=Device.objects.me(),
            path=p
        )


@main.command()
def ls():
    from .models import File
    for f in File.objects.all():
        print(f.path)


@main.command('query')
@click.argument('query_string', type=click.STRING)
def q(query_string):
    """
    query by "path contains"
    """
    from puddl.contrib.file.models import File
    for x in File.objects.filter(path__contains=query_string):
        print(x.path)
