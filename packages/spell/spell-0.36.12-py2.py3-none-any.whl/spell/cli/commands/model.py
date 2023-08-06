# -*- coding: utf-8 -*-
import click

from spell.cli.exceptions import api_client_exception_handler


@click.group(
    name="model",
    short_help="Manage Spell models",
    help="""Spell models are a way for you to track your progress as you work on training models.
    As you run new training runs you can push those outputs to existing model names, and we will
    track those over time for you or create new models. You can take any model version and serve it""",
    hidden=True,
    invoke_without_command=True,
)
@click.pass_context
def model(ctx):
    if ctx.invoked_subcommand:
        return

    click.echo("TODO(ian) print models")


# TODO ian add files option
@model.command(
    name="create",
    short_help="Create a new model",
    help="""Specify a name for the model, if you use an existing model name a new version
    will be created for you, otherwise a new model will be created. Resource should be a path
    to a top level resource such as 'runs/168'.""",
)
@click.pass_context
@click.argument("name")
@click.argument("resource")
@click.option(
    "--version",
    "-v",
    help="You can specify any string you want as a version, or if omitted "
    "it will be given an integer version, autoincremented from the current highest integer version",
)
def create(ctx, name, resource, version):
    client = ctx.obj["client"]
    with api_client_exception_handler():
        client.new_model(ctx.obj["owner"], name, resource, version)
    # TODO(ian) get created model and echo version
    click.echo("Successfully created model: {}".format(name))
