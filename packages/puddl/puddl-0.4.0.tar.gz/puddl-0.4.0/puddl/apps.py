from importlib import import_module


class AppError(Exception):
    pass


class App:
    """
    Must be a package that contains a click.Command object called "main".
    """

    def __init__(self, pkg_name: str):
        self.pkg_name = pkg_name
        # use the package name as cmd_name
        self.cmd_name = self.pkg_name.split('.')[-1]
        self.pkg = import_module(pkg_name)

    @property
    def version(self):
        return self.pkg.__version__

    def __str__(self):
        return f'{self.pkg_name}=={self.version}'

    def get_command(self):
        cmd = self.pkg.main
        # The app's command might have define a different name by mistake, e.g.
        # @click.command(name='something-completely-different')
        # Let's force it into compliance.
        cmd.name = self.cmd_name
        return cmd

    def validate(self):
        """
        Currently just checks if the app can be imported.
        """
        try:
            self.get_command()
        except ImportError:
            raise AppError(f'Not found: {self}')
