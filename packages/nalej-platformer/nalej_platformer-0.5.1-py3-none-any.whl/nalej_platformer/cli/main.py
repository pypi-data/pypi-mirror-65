import sys

import click
import crayons
from vistir.path import normalize_path

from nalej_platformer.exceptions import PlanException, ConfigException, AzureProviderException
from nalej_platformer.config import defaults as cfg_defaults
from nalej_platformer.cli.config import load_configuration
from nalej_platformer.plan import Plan
from nalej_platformer.provider.azure import login


@click.group()
@click.option(
    '--config', default=cfg_defaults.CONFIG_PATH, show_default=True, type=click.Path(file_okay=True, dir_okay=False),
    help='Path to the configuration file')
@click.option('--resources', default="", type=click.Path(file_okay=False, dir_okay=True), help='Path to resources')
@click.option('--debug', default=False, is_flag=True, help='Toggle debug mode')
@click.pass_context
def run(ctx, config, resources, debug):
    """nalej-platformer is a helper utility to simplify the life cycle of a Nalej Platform from a CLI"""

    ctx.ensure_object(dict)
    ctx.obj['CONFIG_PATH'] = normalize_path(config)
    ctx.obj['RESOURCES_PATH'] = normalize_path(resources)
    ctx.obj['DEBUG'] = debug
    try:
        load_configuration(ctx)
        login()
        click.echo("Startup OK\n")
    except (ConfigException, AzureProviderException) as exc:
        click.echo(crayons.red(exc, bold=True))
        sys.exit(1)


@run.command()
@click.argument("plan", type=click.Path(exists=True))
@click.pass_context
def info(ctx, plan):
    """Evaluates a plan and outputs a human readable version of it"""

    ctx.obj['PLAN_PATH'] = normalize_path(plan)
    try:
        plan = Plan.read_plan(ctx.obj['PLAN_PATH'])
        click.echo("############################")
        click.echo("##   PLAN DETAILED VIEW   ##")
        click.echo("############################\n")
        click.echo(plan.info())
    except PlanException as pe:
        click.echo(crayons.red(pe, bold=True))
        sys.exit(1)


@run.command()
@click.argument("plan", type=click.Path(exists=True))
@click.option(
    '--force', '-f', is_flag=True, default=False, help="Force the apply of the plan without user confirmation")
@click.pass_context
def apply(ctx, plan, force):
    """Applies the contents of a plan"""

    ctx.obj['PLAN_PATH'] = normalize_path(plan)
    try:
        plan = Plan.read_plan(ctx.obj['PLAN_PATH'])

        if force or click.confirm('Do you want to continue?', default=True, abort=True):
            plan.apply()
    except PlanException as pe:
        click.echo(crayons.red(pe, bold=True))
        sys.exit(1)
