import click
from auger.cli.utils.context import pass_context
from .impl.datasetcmd import DataSetCmd


@click.group('dataset', short_help='Auger Cloud dataset(s) management')
@pass_context
def command(ctx):
    """Auger Cloud data sets management"""
    ctx.setup_logger(format='')


@click.command(short_help='List data sets on Auger Cloud')
@pass_context
def list_cmd(ctx):
    """List Auger remote datasets"""
    DataSetCmd(ctx).list()


@click.command(short_help='Create data set on the Auger Cloud')
@click.argument('source', required=False, type=click.STRING)
@pass_context
def create(ctx, source):
    """Create data set on the Auger Cloud.
       If source is not specified, auger.yaml/source
       will be used instead.
    """
    DataSetCmd(ctx).create(source)


@click.command(short_help='Delete data set on the Auger Cloud')
@click.argument('name', required=False, type=click.STRING)
@pass_context
def delete(ctx, name):
    """Delete data set on the Auger Cloud
       If name is not specified, auger.yaml/dataset
       will be used instead.
    """
    DataSetCmd(ctx).delete(name)


@click.command(short_help='Select Data Set')
@click.argument('name', required=True, type=click.STRING)
@pass_context
def select(ctx, name):
    """Select data set.
       Name will be set in auger.yaml/dataset
    """
    DataSetCmd(ctx).select(name)

@click.command(short_help='Downloads source data form Data Set on the Auger Cloud')
@click.argument('path_to_download', required=True, type=click.STRING)
@click.option('--dataset', '-ds', type=click.STRING, required=False,
    help='Data Set name to download.')
@pass_context
def download(ctx, dataset, path_to_download):
    """Downloads source data form Data Set on the Auger Cloud.
       If Data Set name is not specified, auger.yaml/dataset
       will be used instead.
    """
    DataSetCmd(ctx).download(dataset, path_to_download)


@pass_context
def add_commands(ctx):
    command.add_command(list_cmd, name='list')
    command.add_command(create)
    command.add_command(delete)
    command.add_command(select)
    command.add_command(download)


add_commands()
