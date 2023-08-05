# -*- coding: utf-8 -*-
import click
from spell.cli.exceptions import api_client_exception_handler, ExitException


def get_available_instances(provider, region):
    if provider == "aws":
        options = ["cpu", "cpu-big", "cpu-huge", "ram-big", "ram-huge"]
        if region in [
            "ap-northeast-1",
            "ap-northeast-2",
            "ap-southeast-1",
            "ap-southeast-2",
            "ca-central-1",
            "cn-north-1",
            "cn-northwest-1",
            "eu-central-1",
            "eu-west-1",
            "eu-west-2",
            "us-east-1",
            "us-east-2",
            "us-west-2",
        ]:
            options.extend(["K80", "K80x8", "V100", "V100x4", "V100x8", "V100x8-big"])
        return options

    # GCP supports different GPUs in different regions
    options = ["cpu", "cpu-big", "cpu-huge"]
    if region in ["us-west1", "us-central1", "us-east1", "europe-west1", "asia-east1"]:
        options.extend(["K80", "K80x2", "K80x4", "K80x8"])
    if region in ["us-west1", "us-central1", "europe-west4", "asia-east1"]:
        options.extend(["V100", "V100x4", "V100x8"])
    if region in [
        "us-west1",
        "us-central1",
        "us-east1",
        "europe-west1",
        "europe-west4",
        "asia-east1",
        "australia-southeast1",
    ]:
        options.extend(["P100", "P100x2", "P100x4"])
    return options


# Maps the name used by the client to a display name
FRAMEWORKS = {
    "tensorflow2": "TensorFlow 2",
    "caffe": "Caffe",
    "torch": "Torch (Lua)",
    "mxnet": "MXNet",
    "dynet": "DyNet",
    "fastai": "Fast.ai",
}


@click.command(
    name="add",
    short_help="Creates a new machine type for executing Spell Runs and Workspaces",
)
@click.pass_context
@click.option("--name", help="Name to give this machine type", prompt=True)
@click.option(
    "--instance-type",
    help="The type of machine to use e.g. 'CPU', 'K80'. "
    "If you skip this you will be prompted with options",
    default=None,
)
@click.option(
    "--spot",
    is_flag=True,
    default=False,
    help="Spot/Preemptible instances can be significantly cheaper than on demand instances, "
    "however AWS/GCP can terminate them at any time. If your run is terminated prematurely we "
    "will keep all data and save it for you with a final run status of Interrupted.",
)
@click.option("--storage-size", default=80, help="Disk size in GB")
@click.option(
    "--additional-images",
    multiple=True,
    type=click.Choice(FRAMEWORKS.values()),
    help="By default all machines support TensorFlow 1, PyTorch, and Conda. "
    "If you require any additional frameworks (e.g. Caffe, MXNet) you can select them here. "
    "Additional frameworks will increase the time it takes to spin up new machines.",
)
@click.option(
    "--min-machines",
    default=0,
    help="Minimum number of machines to keep available at all times regardless of demand",
)
@click.option(
    "--max-machines", default=2, help="Maximum number of machines of this machine type",
)
@click.option(
    "--idle-timeout",
    default=30,
    help="Grace period to wait before terminating idle machines (minutes)",
)
def add_machine_type(
    ctx,
    name,
    instance_type,
    spot,
    storage_size,
    additional_images,
    min_machines,
    max_machines,
    idle_timeout,
):
    cluster = ctx.obj["cluster"]

    # Prompt for instance type
    provider = cluster["cloud_provider"].lower()
    region = cluster["networking"][provider]["region"]
    instance_types = [i.lower() for i in get_available_instances(provider, region)]
    while not instance_type or instance_type.lower() not in instance_types:
        instance_type = click.prompt(
            "Please select an instance type from: {}".format(instance_types)
        )

    # Map display names to server names
    additional_images = [k for (k, v) in FRAMEWORKS.items() if v in additional_images]

    with api_client_exception_handler():
        ctx.obj["client"].create_machine_type(
            cluster["name"],
            name,
            instance_type.lower(),
            spot,
            storage_size,
            additional_images,
            min_machines,
            max_machines,
            idle_timeout,
        )
    click.echo("Successfully created new machine type {}".format(name))


def get_machine_type(ctx, name):
    machine_types = ctx.obj["cluster"]["machine_types"]
    machine_type_names = [mt["name"] for mt in machine_types]
    if name not in machine_type_names:
        raise ExitException(
            "Unknown machine type {} choose from {}".format(name, machine_type_names)
        )
    matching = [mt for mt in machine_types if mt["name"] == name]
    if len(matching) > 1:
        raise ExitException(
            "Unexpectedly found {} machine types with the name {}".format(
                len(matching), name
            )
        )
    return matching[0]


@click.command(
    name="scale",
    short_help="Change the limits for number of machines of this machine type",
)
@click.argument("name")
@click.option(
    "--min-machines",
    help="Minimum number of machines to keep available at all times regardless of demand. Omit to leave unchanged",
)
@click.option(
    "--max-machines",
    help="Maximum number of machines of this machine type. Omit to leave unchanged",
)
@click.option(
    "--idle-timeout",
    help="Grace period to wait before terminating idle machines (minutes). Omit to leave unchanged",
)
@click.pass_context
def scale_machine_type(ctx, name, min_machines, max_machines, idle_timeout):
    machine_type = get_machine_type(ctx, name)
    if min_machines is None:
        min_machines = click.prompt(
            "Enter new value for minimum machines",
            default=machine_type["min_instances"],
        )
    if max_machines is None:
        max_machines = click.prompt(
            "Enter new value for maximum machines",
            default=machine_type["max_instances"],
        )
    if idle_timeout is None:
        idle_timeout = click.prompt(
            "Enter new value for idle timeout (minutes)",
            default=machine_type["idle_timeout_seconds"] / 60,
        )
    with api_client_exception_handler():
        ctx.obj["client"].scale_machine_type(
            ctx.obj["cluster"]["name"],
            machine_type["id"],
            min_machines,
            max_machines,
            idle_timeout,
        )
    click.echo("Successfully updated {}!".format(name))


@click.command(name="delete", short_help="Delete a machine type")
@click.argument("name")
@click.option("-f", "--force", is_flag=True, help="Do not prompt for confirmation")
@click.pass_context
def delete_machine_type(ctx, name, force):
    machine_type = get_machine_type(ctx, name)
    if not force and not click.confirm(
        "Are you sure you want to delete {}?".format(name)
    ):
        return
    with api_client_exception_handler():
        cluster_name = ctx.obj["cluster"]["name"]
        mt_id = machine_type["id"]
        ctx.obj["client"].delete_machine_type(cluster_name, mt_id)
    click.echo("Successfully deleted {}!".format(name))
