import click
from auger.cli.utils.context import pass_context
from .impl.newcmd import NewCmd


@click.command('new', short_help='Create new AugerAI project.')
@click.argument('project-name', required=True, type=click.STRING)
@click.option(
    '--source', '-s',  default='', type=click.STRING,
    help='Data source local file or remote url.')
@click.option(
    '--model-type', '-mt', default='classification',
    type=click.Choice(['classification', 'regression', 'timeseries']),
    help='Model Type.')
@click.option(
    '--target', '-t',  default='', type=click.STRING,
    help='Target column name in data source.')
@pass_context
def command(ctx, project_name, source, model_type, target):
    """Create new AugerAi project."""
    ctx.setup_logger(format='')
    NewCmd(ctx, project_name, target, source, model_type).create_project()
