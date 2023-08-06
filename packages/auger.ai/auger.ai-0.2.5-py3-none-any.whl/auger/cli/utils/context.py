import click
import auger.api.utils.context


class Context(auger.api.utils.context.Context):
    """Auger CLI Context."""
    def __init__(self, name=''):
        super(Context, self).__init__(name)
        self.not_reraise_exceptions = True


CONTEXT_SETTINGS = dict(auto_envvar_prefix='AUGER')
pass_context = click.make_pass_decorator(Context, ensure=True)
