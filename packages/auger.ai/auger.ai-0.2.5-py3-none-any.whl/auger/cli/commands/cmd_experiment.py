import click
from auger.cli.utils.context import pass_context
from .impl.experimentcmd import ExperimentCmd


@click.group('experiment', short_help='Auger experiment management')
@pass_context
def command(ctx):
    """Auger experiment management"""
    ctx.setup_logger(format='')


@click.command(short_help='List Experiments for selected DataSet')
@pass_context
def list_cmd(ctx):
    """List Experiments for selected DataSet"""
    ExperimentCmd(ctx).list()


@click.command(short_help='Start Experiment')
@pass_context
def start(ctx):
    """Start Experiment.
       If Experiment is not selected, new Experiment will be created.
    """
    ExperimentCmd(ctx).start()


@click.command(short_help='Stop Experiment')
@pass_context
def stop(ctx):
    """Stop Experiment"""
    ExperimentCmd(ctx).stop()


@click.command(short_help='Show Experiment leaderboard')
@click.argument('run-id', required=False, type=click.STRING)
@pass_context
def leaderboard(ctx, run_id):
    """Show Experiment leaderboard for specified run id.
       If run id is not provided, latest experiment run
       leaderboard will be shown.
    """
    ExperimentCmd(ctx).leaderboard(run_id)

@click.command(short_help='Show Experiment history')
@pass_context
def history(ctx):
    """Show Experiment history"""
    ExperimentCmd(ctx).history()


@pass_context
def add_commands(ctx):
    command.add_command(list_cmd, name='list')
    command.add_command(start)
    command.add_command(stop)
    command.add_command(leaderboard)
    command.add_command(history)


add_commands()
