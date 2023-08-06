import click
from auger.cli.utils.context import pass_context
from .impl.projectcmd import ProjectCmd


@click.group('project', short_help='Auger Cloud Projects management')
@pass_context
def command(ctx):
    """Auger Cloud Project(s) management"""
    ctx.setup_logger(format='')

@click.command(short_help='List Projects')
@pass_context
def list_cmd(ctx):
    """List Projects"""
    ProjectCmd(ctx).list()

@click.command(short_help='Create Project')
@click.argument('name', required=False, type=click.STRING)
@pass_context
def create(ctx, name):
    """Create Project"""
    ProjectCmd(ctx).create(name)

@click.command(short_help='Delete Project')
@click.argument('name', required=False, type=click.STRING)
@pass_context
def delete(ctx, name):
    """Delete Project"""
    ProjectCmd(ctx).delete(name)


@click.command(short_help='Start Project')
@click.argument('name', required=False, type=click.STRING)
@pass_context
def start(ctx, name):
    """Start Project.
       If name is not specified will start Project set in auger.yaml/name
    """
    ProjectCmd(ctx).start(name)


@click.command(short_help='Stop Project')
@click.argument('name', required=False, type=click.STRING)
@pass_context
def stop(ctx, name):
    """Stop Project.
       If name is not specified will stop Project set in auger.yaml/name
    """
    ProjectCmd(ctx).stop(name)


@click.command(short_help='Select Project')
@click.argument('name', required=True, type=click.STRING)
@pass_context
def select(ctx, name):
    """Select Project.
       Name will be set in auger.yaml/name
    """
    ProjectCmd(ctx).select(name)


@pass_context
def add_commands(ctx):
    command.add_command(list_cmd, name='list')
    command.add_command(create)
    command.add_command(delete)
    command.add_command(select)
    command.add_command(start)
    command.add_command(stop)


add_commands()
