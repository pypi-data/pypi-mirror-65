import json
import logging
import os
from collections import UserDict
from pathlib import Path
from urllib.parse import urlencode

from puddl.apps import App

log = logging.getLogger(__name__)


class ConfigError(Exception):
    pass


class Config(UserDict):
    PUDDLRC = Path.home() / '.puddlrc'

    DB_DEFAULTS = {
        'PGUSER': os.environ.get('PGUSER'),
        'PGPASSWORD': os.environ.get('PGPASSWORD'),
        'PGHOST': os.environ.get('PGHOST'),
        'PGPORT': os.environ.get('PGPORT'),
        'PGDATABASE': os.environ.get('PGDATABASE'),
        'PGAPPNAME': os.environ.get('PGAPPNAME', 'puddl'),
    }

    @classmethod
    def get_defaults(cls):
        defaults = cls.DB_DEFAULTS.copy()
        defaults['apps'] = []
        return defaults

    def write(self):
        # serialize first, write next
        x = json.dumps(self.data, indent=2, sort_keys=True)
        with self.PUDDLRC.open('w') as f:
            f.write(x)

    @property
    def apps(self):
        return self['apps']

    @property
    def db_url(self) -> str:
        db_params = {
            'application_name': self['PGAPPNAME']
        }
        return 'postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}' \
               '/{PGDATABASE}?{params}'.format(**self, params=urlencode(db_params))

    @property
    def db_env(self):
        return {k: v for k, v in self.items() if k in self.DB_DEFAULTS.keys()}

    def add_app(self, name):
        p = App(name)
        p.validate()
        self['apps'].append(p.pkg_name)

    def remove_app(self, name):
        ps = self['apps']
        try:
            del ps[ps.index(name)]
        except ValueError:
            log.warning(f'app {name} was not installed')


def get_config(app=None):
    if app is None:
        app = 'puddl'

    try:
        with Config.PUDDLRC.open() as f:
            data = json.load(f)
    except FileNotFoundError:
        data = Config.get_defaults()
    except json.decoder.JSONDecodeError as e:
        raise ConfigError(
            f'{Config.PUDDLRC}:{e.lineno} column {e.colno} char {e.pos}: {e.msg}'
        )
    data['PGAPPNAME'] = app
    return Config(**data)
